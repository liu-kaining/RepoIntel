from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from typing import Any

from .config import Settings
from .exceptions import LLMResponseError
from .models import RepoAudit, RepoCandidate, Scores

LOGGER = logging.getLogger(__name__)

ROUGH_SYSTEM_PROMPT = """你是 RepoIntel 的第一轮技术情报筛选官。你的职责不是营销推荐，而是快速剔除噪音。

筛选原则：
1. 只保留有真实工程量、明确技术痛点、可复用价值的仓库。
2. 降权纯演示、玩具项目、资料合集、Awesome 列表、换壳 UI、标题党项目。
3. 优先选择：基础设施、开发者工具、AI 工程化、数据库/编译器/安全/自动化/云原生等硬核项目。
4. 不要被 Star 数迷惑，必须结合 Fork、语言、README、近期活跃度判断。

只返回 JSON，不要 Markdown，不要解释。格式：
{"selected": ["owner/repo", "owner/repo"], "rejected_notes": {"owner/repo": "简短原因"}}
"""

DEEP_AUDIT_SYSTEM_PROMPT = """你是 RepoIntel（开源情报局）的首席架构审计官，风格是资深、克制、挑剔、技术上诚实。

你的任务是审计一个 GitHub 仓库是否值得进入“开源米其林指南”。你必须基于给定的仓库元数据、语言分布、README 摘要和硬指标判断，不能编造未提供的事实。

审计标准：
- 创新度 innovation：是否创造新范式、新抽象、新工程路径；还是常见轮子的第 N 次重复。
- 实用性 utility：是否解决真实、高频、昂贵的工程痛点；是否能被开发者直接采用。
- 工程质量 engineering：架构清晰度、代码组织、测试/CI 迹象、边界条件、可维护性、依赖复杂度、文档可信度。
- 社区健康 health：Fork/Star 合理性、Issue 压力、维护活跃度、生态外溢、单点维护风险。

打分要求：
- 每项 0-100，严禁全员高分。
- 75 是“值得进入候选报道”的最低线，85+ 必须有明显硬核优势。
- 如果信息不足，要在 hidden_risks 里说明，而不是脑补。
- technical_review 必须像 CTO code/architecture review：具体、可执行、指出亮点和雷点，不能空泛吹捧。
- summary 要短、狠、准确。

只返回 raw JSON，不要 Markdown code block，不要额外解释。字段必须完全符合：
{
  "repo_name": "owner/repo",
  "category": "Theme classification string",
  "tags": ["array", "of", "strings"],
  "scores": {"innovation": 0, "utility": 0, "engineering": 0, "health": 0},
  "summary": "一句话情报解密。",
  "pain_point": "它解决的具体工程痛点。",
  "technical_review": "深入、挑剔、具体的架构与工程审计。",
  "commercial_value": "潜在生态价值或商业影响。",
  "hidden_risks": ["风险1", "风险2"]
}
"""


@dataclass(frozen=True)
class LLMMessage:
    system: str
    user: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 4096


class AIEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
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
                audits.append(self.deep_audit(repo))
            except LLMResponseError as exc:
                LOGGER.error("Deep audit failed for %s: %s", repo.full_name, exc)
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
        LOGGER.debug(
            "Top rough candidates by signal: %s",
            [repo.full_name for repo in ordered_by_signal[:8]],
        )
        prompt = {
            "instruction": f"从候选仓库中挑出最多 {self.settings.rough_screen_limit} 个最值得深度审计的项目。",
            "repos": [repo.to_llm_context() for repo in ordered_by_signal],
        }
        try:
            raw = self._complete(
                LLMMessage(
                    system=ROUGH_SYSTEM_PROMPT,
                    user=json.dumps(prompt, ensure_ascii=False),
                    model=self.settings.rough_llm_model or self.settings.llm_model,
                    temperature=0.1,
                    max_tokens=3000,
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
        if self.settings.dry_run:
            return _heuristic_audit(repo)

        LOGGER.info("Deep auditing %s with model %s", repo.full_name, self.settings.llm_model)
        LOGGER.debug(
            "Deep audit context for %s: stars=%d, forks=%d, language=%s, topics=%s",
            repo.full_name,
            repo.stargazers_count,
            repo.forks_count,
            repo.primary_language,
            repo.topics[:8],
        )
        prompt = {
            "repo": repo.to_llm_context(),
            "local_scoring_formula": "total_score = 0.30*innovation + 0.30*utility + 0.25*engineering + 0.15*health; final total is recomputed by RepoIntel, do not optimize for vanity.",
            "review_depth_requirement": "technical_review 至少指出一个技术亮点和一个可能风险；如果 README 或元数据不足，必须明确说信息不足。",
        }
        raw = self._complete(
            LLMMessage(
                system=DEEP_AUDIT_SYSTEM_PROMPT,
                user=json.dumps(prompt, ensure_ascii=False),
                model=self.settings.llm_model,
                temperature=0.15,
                max_tokens=5000,
            )
        )
        payload = _extract_json(raw)
        audit = _audit_from_payload(repo, payload)
        LOGGER.info("Deep audit completed for %s -> score=%s", repo.full_name, audit.total_score)
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


def _audit_from_payload(repo: RepoCandidate, payload: dict[str, Any]) -> RepoAudit:
    scores_payload = payload.get("scores")
    if not isinstance(scores_payload, dict):
        raise LLMResponseError("Deep audit response missing scores object.")
    try:
        scores = Scores(
            innovation=_to_score(scores_payload.get("innovation")),
            utility=_to_score(scores_payload.get("utility")),
            engineering=_to_score(scores_payload.get("engineering")),
            health=_to_score(scores_payload.get("health")),
        )
    except (TypeError, ValueError) as exc:
        raise LLMResponseError(f"Invalid score payload for {repo.full_name}.") from exc

    tags = payload.get("tags")
    risks = payload.get("hidden_risks")
    return RepoAudit(
        repo_name=_non_empty_string(payload.get("repo_name"), repo.full_name),
        repo_link=repo.html_url,
        category=_non_empty_string(payload.get("category"), "Open Source Infrastructure"),
        tags=[str(tag).strip() for tag in tags if str(tag).strip()][:8]
        if isinstance(tags, list)
        else [repo.primary_language],
        scores=scores,
        summary=_non_empty_string(payload.get("summary"), repo.description or repo.full_name),
        pain_point=_non_empty_string(payload.get("pain_point"), "未提供足够信息判断具体痛点。"),
        technical_review=_non_empty_string(
            payload.get("technical_review"), "信息不足，无法做负责任的架构审计。"
        ),
        commercial_value=_non_empty_string(payload.get("commercial_value"), "生态影响仍需观察。"),
        hidden_risks=[str(risk).strip() for risk in risks if str(risk).strip()][:8]
        if isinstance(risks, list)
        else ["模型未返回明确风险，需人工复核。"],
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


def _heuristic_audit(repo: RepoCandidate) -> RepoAudit:
    engineering = 72
    if repo.readme_excerpt:
        engineering += 5
    if repo.recent_commit_count and repo.recent_commit_count >= 3:
        engineering += 5
    health = min(90, 58 + int(repo.fork_star_ratio * 600) + min(repo.recent_commit_count or 0, 10))
    innovation = 78 if any(topic in {"ai", "agent", "llm"} for topic in repo.topics) else 72
    utility = 82 if repo.stargazers_count >= 1000 else 74
    scores = Scores(
        innovation=min(innovation, 92),
        utility=min(utility, 92),
        engineering=min(engineering, 88),
        health=min(health, 90),
    )
    return RepoAudit(
        repo_name=repo.full_name,
        repo_link=repo.html_url,
        category="Developer Tooling",
        tags=[repo.primary_language, *repo.topics[:5]],
        scores=scores,
        summary=f"{repo.full_name} 展现出明确工程工具属性，但仍需人工复核真实代码质量。",
        pain_point=repo.description or "帮助开发者处理具体工程自动化与效率问题。",
        technical_review=(
            "Dry-run 启发式审计：该项目的 Star/Fork 与近期提交信号较健康，README 信息可用于初步判断。"
            "正式运行时应由大模型结合 README、语言分布和硬指标输出更深入的架构审计。"
        ),
        commercial_value="如果工程实现扎实，具备进入开发者工具链或自动化工作流的生态价值。",
        hidden_risks=["当前为 dry-run 启发式结果，不能替代正式 LLM 深度审计。"],
    )
