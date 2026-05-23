from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from typing import Any

from .code_intel import CodeIntelGatherer
from .config import Settings
from .exceptions import LLMResponseError
from .github_client import GitHubClient
from .legacy_guard import should_reject_publication
from .models import RepoAudit, RepoCandidate, RepoCodeBundle, Scores
from .prompts import (
    DEEP_AUDIT_SYSTEM_PROMPT,
    ROUGH_SYSTEM_PROMPT,
    build_deep_audit_user_payload,
    build_rough_screen_user_payload,
)
from .scoring import calibrate_scores, merge_quality_risks, review_quality_issues

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class LLMMessage:
    system: str
    user: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 4096


class AIEngine:
    def __init__(self, settings: Settings, github: GitHubClient) -> None:
        self.settings = settings
        self.github = github
        self.code_intel = CodeIntelGatherer(settings, github)
        self._openai_client: Any | None = None
        self._claude_client: Any | None = None

    def analyze_repos(self, eligible_repos: list[RepoCandidate]) -> list[RepoAudit]:
        if not eligible_repos:
            return []
        screened = self.rough_screen(eligible_repos)
        LOGGER.info("Rough screen kept %d/%d repos", len(screened), len(eligible_repos))
        audits: list[RepoAudit] = []
        for repo in screened:
            try:
                audit = self.deep_audit(repo)
            except LLMResponseError as exc:
                LOGGER.error("Deep audit failed for %s: %s", repo.full_name, exc)
                continue
            reject, reason = should_reject_publication(repo, audit)
            if reject:
                LOGGER.warning(
                    "Audit rejected for publication: %s (%s); score was %s",
                    repo.full_name,
                    reason,
                    audit.total_score,
                )
                continue
            audits.append(audit)
        return sorted(audits, key=lambda audit: audit.total_score, reverse=True)

    def rough_screen(self, repos: list[RepoCandidate]) -> list[RepoCandidate]:
        ordered_by_signal = sorted(
            repos,
            key=lambda repo: (
                repo.fork_star_ratio,
                repo.recent_commit_count or 0,
                repo.stargazers_count,
            ),
            reverse=True,
        )
        if self.settings.dry_run:
            return ordered_by_signal[: self.settings.rough_screen_limit]

        LOGGER.info(
            "Rough screen submitting %d candidates to model %s",
            len(ordered_by_signal),
            self.settings.rough_llm_model or self.settings.llm_model,
        )
        user_payload = build_rough_screen_user_payload(
            [repo.to_llm_context() for repo in ordered_by_signal],
            select_limit=self.settings.rough_screen_limit,
        )
        try:
            raw = self._complete(
                LLMMessage(
                    system=ROUGH_SYSTEM_PROMPT,
                    user=json.dumps(user_payload, ensure_ascii=False),
                    model=self.settings.rough_llm_model or self.settings.llm_model,
                    temperature=0.05,
                    max_tokens=3500,
                )
            )
            payload = _extract_json(raw)
        except LLMResponseError as exc:
            LOGGER.error("LLM rough screen failed: %s; falling back to metric ordering", exc)
            return ordered_by_signal[: self.settings.rough_screen_limit]
        selected = payload.get("selected")
        if not isinstance(selected, list):
            raise LLMResponseError("Rough screen response must contain selected list.")
        by_name = {repo.full_name: repo for repo in ordered_by_signal}
        chosen = [by_name[name] for name in selected if isinstance(name, str) and name in by_name]
        if not chosen:
            LOGGER.warning(
                "LLM rough screen returned no valid repos; falling back to metric ordering"
            )
            return ordered_by_signal[: self.settings.rough_screen_limit]
        return chosen[: self.settings.rough_screen_limit]

    def deep_audit(self, repo: RepoCandidate) -> RepoAudit:
        code_bundle = self.code_intel.gather(repo)
        if len(code_bundle.files) < self.settings.min_code_files_for_audit:
            raise LLMResponseError(
                f"Only read {len(code_bundle.files)} source files for {repo.full_name}; "
                f"minimum required is {self.settings.min_code_files_for_audit}."
            )

        if self.settings.dry_run:
            return _heuristic_audit(repo, code_bundle)

        LOGGER.info(
            "Deep code audit %s: %d files, %d chars via %s",
            repo.full_name,
            len(code_bundle.files),
            code_bundle.total_chars,
            code_bundle.source,
        )
        user_payload = build_deep_audit_user_payload(
            repo.to_llm_context(),
            code_bundle.to_llm_payload(),
        )
        raw = self._complete(
            LLMMessage(
                system=DEEP_AUDIT_SYSTEM_PROMPT,
                user=json.dumps(user_payload, ensure_ascii=False),
                model=self.settings.llm_model,
                temperature=0.1,
                max_tokens=16_000,
            )
        )
        payload = _extract_json(raw)
        audit = _audit_from_payload(repo, payload, code_bundle)
        LOGGER.info(
            "Deep audit completed for %s -> score=%s (raw LLM dims: I=%s U=%s E=%s H=%s)",
            repo.full_name,
            audit.total_score,
            audit.scores.innovation,
            audit.scores.utility,
            audit.scores.engineering,
            audit.scores.health,
        )
        return audit

    def _complete(self, message: LLMMessage) -> str:
        last_error: LLMResponseError | None = None
        for attempt in range(3):
            try:
                if self.settings.llm_provider == "openai":
                    return self._complete_openai(message)
                return self._complete_claude(message)
            except LLMResponseError as exc:
                last_error = exc
                if attempt < 2:
                    delay = 1.5 * (attempt + 1)
                    LOGGER.warning(
                        "LLM request failed (attempt %d/3): %s; retrying in %.1fs",
                        attempt + 1,
                        exc,
                        delay,
                    )
                    time.sleep(delay)
        assert last_error is not None
        LOGGER.error("LLM request failed after retries: %s", last_error)
        raise last_error

    def _complete_openai(self, message: LLMMessage) -> str:
        if self._openai_client is None:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise LLMResponseError(
                    "The openai package is required for LLM_PROVIDER=openai."
                ) from exc
            kwargs: dict[str, Any] = {"api_key": self.settings.llm_api_key}
            if self.settings.llm_base_url:
                kwargs["base_url"] = self.settings.llm_base_url
            self._openai_client = OpenAI(**kwargs)
        try:
            response = self._openai_client.chat.completions.create(
                model=message.model,
                messages=[
                    {"role": "system", "content": message.system},
                    {"role": "user", "content": message.user},
                ],
                temperature=message.temperature,
                max_tokens=message.max_tokens,
                response_format={"type": "json_object"},
            )
        except Exception as exc:
            raise LLMResponseError(f"OpenAI-compatible request failed: {exc}") from exc
        content = response.choices[0].message.content
        if not content:
            raise LLMResponseError("OpenAI-compatible model returned empty content.")
        return content

    def _complete_claude(self, message: LLMMessage) -> str:
        if self._claude_client is None:
            try:
                from anthropic import Anthropic
            except ImportError as exc:
                raise LLMResponseError(
                    "The anthropic package is required for LLM_PROVIDER=claude."
                ) from exc
            kwargs: dict[str, Any] = {"api_key": self.settings.llm_api_key}
            if self.settings.llm_base_url:
                kwargs["base_url"] = self.settings.llm_base_url
            self._claude_client = Anthropic(**kwargs)
        try:
            response = self._claude_client.messages.create(
                model=message.model,
                system=message.system,
                messages=[{"role": "user", "content": message.user}],
                temperature=message.temperature,
                max_tokens=message.max_tokens,
            )
        except Exception as exc:
            raise LLMResponseError(f"Claude request failed: {exc}") from exc
        chunks: list[str] = []
        for block in response.content:
            text = getattr(block, "text", None)
            if text:
                chunks.append(text)
        content = "".join(chunks).strip()
        if not content:
            raise LLMResponseError("Claude model returned empty content.")
        return content


def _extract_json(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text).strip()
    decoder = json.JSONDecoder()
    for candidate in (text, text[text.find("{") :] if "{" in text else ""):
        if not candidate:
            continue
        try:
            payload, _ = decoder.raw_decode(candidate)
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            continue
    raise LLMResponseError("LLM response does not contain a valid JSON object.")


def _audit_from_payload(
    repo: RepoCandidate, payload: dict[str, Any], code_bundle: RepoCodeBundle
) -> RepoAudit:
    scores_payload = payload.get("scores")
    if not isinstance(scores_payload, dict):
        raise LLMResponseError("Deep audit response missing scores object.")
    try:
        raw_scores = Scores(
            innovation=_to_score(scores_payload.get("innovation")),
            utility=_to_score(scores_payload.get("utility")),
            engineering=_to_score(scores_payload.get("engineering")),
            health=_to_score(scores_payload.get("health")),
        )
    except (TypeError, ValueError) as exc:
        raise LLMResponseError(f"Invalid score payload for {repo.full_name}.") from exc

    scores = calibrate_scores(repo, raw_scores)
    if scores != raw_scores:
        LOGGER.info(
            "Score calibration adjusted %s: %s -> %s",
            repo.full_name,
            raw_scores.as_dict(),
            scores.as_dict(),
        )

    summary = _non_empty_string(payload.get("summary"), repo.description or repo.full_name)
    technical_review = _non_empty_string(
        payload.get("technical_review"), "信息不足，无法做负责任的架构审计。"
    )
    quality_issues = review_quality_issues(
        repo, technical_review, summary, code_paths=code_bundle.selected_paths
    )
    if quality_issues:
        LOGGER.warning("Audit quality issues for %s: %s", repo.full_name, "; ".join(quality_issues))

    tags = payload.get("tags")
    risks = payload.get("hidden_risks")
    hidden_risks = (
        [str(risk).strip() for risk in risks if str(risk).strip()][:8]
        if isinstance(risks, list)
        else ["模型未返回明确风险，需人工复核。"]
    )
    hidden_risks = merge_quality_risks(hidden_risks, quality_issues)

    return RepoAudit(
        repo_name=_non_empty_string(payload.get("repo_name"), repo.full_name),
        repo_link=repo.html_url,
        category=_non_empty_string(payload.get("category"), "Open Source Infrastructure"),
        tags=[str(tag).strip() for tag in tags if str(tag).strip()][:8]
        if isinstance(tags, list)
        else [repo.primary_language],
        scores=scores,
        summary=summary,
        pain_point=_non_empty_string(payload.get("pain_point"), "未提供足够信息判断具体痛点。"),
        technical_review=technical_review,
        commercial_value=_non_empty_string(payload.get("commercial_value"), "生态影响仍需观察。"),
        hidden_risks=hidden_risks,
        code_files_reviewed=tuple(file.path for file in code_bundle.files),
        code_source=code_bundle.source,
        code_chars_analyzed=code_bundle.total_chars,
    )


def _to_score(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError("boolean is not a score")
    score = round(float(value))
    if not 0 <= score <= 100:
        raise ValueError("score out of range")
    return score


def _non_empty_string(value: Any, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def _heuristic_audit(repo: RepoCandidate, code_bundle: RepoCodeBundle) -> RepoAudit:
    readme_len = len(repo.readme_excerpt.strip())
    engineering = 58
    if readme_len > 500:
        engineering += 8
    if repo.recent_commit_count and repo.recent_commit_count >= 3:
        engineering += 6
    health = min(78, 52 + int(repo.fork_star_ratio * 500) + min(repo.recent_commit_count or 0, 8))
    innovation = 68
    utility = 70
    if any(topic in {"ai", "agent", "llm", "mcp"} for topic in repo.topics):
        innovation += 6
    scores = calibrate_scores(
        repo,
        Scores(
            innovation=min(innovation, 76),
            utility=min(utility, 78),
            engineering=min(engineering, 74),
            health=min(health, 76),
        ),
    )
    return RepoAudit(
        repo_name=repo.full_name,
        repo_link=repo.html_url,
        category="Developer Tooling",
        tags=[repo.primary_language, *repo.topics[:5]],
        scores=scores,
        summary=f"{repo.full_name} 需正式 LLM 审计；dry-run 仅基于 README 与指标的保守估计。",
        pain_point=repo.description or "待深度审计确认具体工程痛点。",
        technical_review=(
            "【架构】基于 sample 源码 `src/agent/runtime.rs:12`，`execute` 先走 `sandbox.verify` 再解析 handler。"
            "【亮点】`AgentRuntime` 将 sandbox 与 `ToolRegistry` 分离，边界清楚。"
            "【疑点】dry-run 未跑完整仓库，仅抽样文件。"
            "【建议】正式流水线将浅克隆全仓并审阅 tests/ 与 CI。"
        ),
        commercial_value="待正式审计评估生态位与替代方案关系。",
        hidden_risks=[
            "当前为 dry-run 启发式结果，不能替代正式 LLM 深度审计。",
            "README 信息可能不完整，评分已做保守校准。",
        ],
        code_files_reviewed=tuple(file.path for file in code_bundle.files),
        code_source=code_bundle.source,
        code_chars_analyzed=code_bundle.total_chars,
    )
