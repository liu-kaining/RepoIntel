from __future__ import annotations

import base64
import logging
import time
from datetime import UTC, datetime, timedelta
from typing import Any

import requests

from .config import Settings
from .exceptions import ExternalServiceError
from .legacy_guard import is_legacy_megaproject, legacy_rejection_reason
from .models import FilterDecision, ProcessedState, RepoCandidate, cutoff_datetime

LOGGER = logging.getLogger(__name__)
NON_CODE_PRIMARY_LANGUAGES = {"markdown", "html", "css"}
NON_CODE_LANGUAGE_BYTES = {"markdown", "html"}


class GitHubClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "RepoIntel/0.1",
            }
        )
        if settings.github_token:
            self.session.headers["Authorization"] = f"Bearer {settings.github_token}"

    def discover_candidates(self) -> list[RepoCandidate]:
        if self.settings.dry_run:
            return self._dry_run_candidates()

        now = datetime.now(UTC)
        created_month = (now - timedelta(days=self.settings.max_repo_age_days)).date().isoformat()
        created_week = (now - timedelta(days=7)).date().isoformat()
        pushed_recent = (now - timedelta(days=3)).date().isoformat()

        # Only surface repos created within the freshness window — never decade-old giants
        # that merely had a recent push (linux, kubernetes, node, etc.).
        search_plans = [
            {
                "label": "week-hot",
                "query": (
                    f"stars:>={self.settings.min_stars_week} "
                    f"created:>={created_week} "
                    f"pushed:>={pushed_recent} "
                    "archived:false fork:false"
                ),
                "sort": "stars",
            },
            {
                "label": "month-hot",
                "query": (
                    f"stars:>={self.settings.min_stars} "
                    f"created:>={created_month} "
                    f"pushed:>={pushed_recent} "
                    "archived:false fork:false"
                ),
                "sort": "stars",
            },
        ]

        seen: set[str] = set()
        repos: list[RepoCandidate] = []
        for plan in search_plans:
            fetched = self._search_repositories(
                plan["query"],
                sort=plan["sort"],
                limit=self.settings.max_candidates - len(repos),
            )
            LOGGER.info(
                "Discovery [%s] returned %d repos (query=%s)",
                plan["label"],
                len(fetched),
                plan["query"],
            )
            for repo in fetched:
                if repo.full_name in seen:
                    continue
                seen.add(repo.full_name)
                repos.append(repo)
                if len(repos) >= self.settings.max_candidates:
                    break
            if len(repos) >= self.settings.max_candidates:
                break

        LOGGER.info(
            "Discovered %d fresh GitHub candidates (max age %d days)",
            len(repos),
            self.settings.max_repo_age_days,
        )
        return repos

    def _search_repositories(self, query: str, *, sort: str, limit: int) -> list[RepoCandidate]:
        if limit <= 0:
            return []
        repos: list[RepoCandidate] = []
        page = 1
        while len(repos) < limit:
            per_page = min(100, limit - len(repos))
            params = {
                "q": query,
                "sort": sort,
                "order": "desc",
                "per_page": per_page,
                "page": page,
            }
            payload = self._request_json(
                "GET", "https://api.github.com/search/repositories", params=params
            )
            items = payload.get("items", [])
            if not isinstance(items, list):
                raise ExternalServiceError("GitHub Search API returned an invalid items payload.")
            if not items:
                break
            repos.extend(RepoCandidate.from_github_api(item) for item in items)
            if len(items) < per_page:
                break
            page += 1
        return repos

    def enrich_candidates(
        self, repos: list[RepoCandidate], limit: int | None = None
    ) -> list[RepoCandidate]:
        if self.settings.dry_run:
            return repos
        work = repos
        if limit is not None:
            work = repos[:limit]
        LOGGER.info("Starting repository enrichment for %d candidates (limit=%s)", len(work), limit)
        enriched: list[RepoCandidate] = []
        since = cutoff_datetime(self.settings.require_recent_push_hours)
        for repo in work:
            languages: dict[str, int] | None = None
            readme = ""
            commit_count: int | None = None
            enrichment_failed = False
            try:
                languages = self.fetch_languages(repo)
                readme = self.fetch_readme_excerpt(repo)
                commit_count = self.fetch_recent_commit_count(repo, since)
                LOGGER.debug(
                    "Enriched %s: languages=%d, readme_len=%d, commit_count=%s",
                    repo.full_name,
                    len(languages),
                    len(readme),
                    commit_count,
                )
            except ExternalServiceError as exc:
                enrichment_failed = True
                LOGGER.warning("Failed to enrich %s: %s", repo.full_name, exc)
            enriched.append(
                repo.with_enrichment(
                    languages=languages or {},
                    readme_excerpt=readme,
                    recent_commit_count=commit_count,
                    enrichment_failed=enrichment_failed,
                )
            )
        return enriched

    def fetch_languages(self, repo: RepoCandidate) -> dict[str, int]:
        payload = self._request_json(
            "GET", f"https://api.github.com/repos/{repo.full_name}/languages"
        )
        return {
            str(k): int(v)
            for k, v in payload.items()
            if isinstance(v, int | float) and not isinstance(v, bool)
        }

    def fetch_readme_excerpt(self, repo: RepoCandidate, limit: int = 8000) -> str:
        try:
            payload = self._request_json(
                "GET", f"https://api.github.com/repos/{repo.full_name}/readme"
            )
        except ExternalServiceError:
            return ""
        if payload.get("encoding") == "base64" and payload.get("content"):
            try:
                max_b64_chars = (limit * 4 // 3) + 8
                content_b64 = str(payload["content"]).replace("\n", "")
                # Pad base64 so truncated content still decodes safely.
                content_b64 = content_b64[:max_b64_chars]
                padding = 4 - len(content_b64) % 4 if len(content_b64) % 4 else 0
                content_b64 = content_b64 + ("=" * padding)
                decoded = base64.b64decode(content_b64, validate=False)
                return decoded.decode("utf-8", errors="replace")[:limit]
            except (ValueError, TypeError):
                return ""
        text = payload.get("content")
        if isinstance(text, str) and text:
            return text[:limit]
        return ""

    def fetch_branch_head_sha(self, repo: RepoCandidate) -> str:
        payload = self._request_json(
            "GET",
            f"https://api.github.com/repos/{repo.full_name}/git/ref/heads/{repo.default_branch}",
        )
        object_info = payload.get("object")
        if not isinstance(object_info, dict) or not object_info.get("sha"):
            raise ExternalServiceError(f"Could not resolve branch head for {repo.full_name}")
        return str(object_info["sha"])

    def fetch_repository_tree_entries(self, repo: RepoCandidate) -> list:
        from .code_selection import TreeEntry

        ref = self.fetch_branch_head_sha(repo)
        payload = self._request_json(
            "GET",
            f"https://api.github.com/repos/{repo.full_name}/git/trees/{ref}",
            params={"recursive": "1"},
        )
        tree = payload.get("tree", [])
        if not isinstance(tree, list):
            raise ExternalServiceError(f"Invalid tree payload for {repo.full_name}")
        entries: list[TreeEntry] = []
        for item in tree:
            if not isinstance(item, dict):
                continue
            if item.get("type") != "blob":
                continue
            path = str(item.get("path", ""))
            if not path:
                continue
            size = int(item.get("size") or 0)
            entries.append(TreeEntry(path=path, size=size))
        return entries

    def fetch_repository_file(self, repo: RepoCandidate, path: str) -> str:
        from urllib.parse import quote

        encoded = quote(path, safe="/")
        payload = self._request_json(
            "GET",
            f"https://api.github.com/repos/{repo.full_name}/contents/{encoded}",
            params={"ref": repo.default_branch},
        )
        if isinstance(payload, list):
            raise ExternalServiceError(f"Path is a directory, not a file: {path}")
        if payload.get("encoding") == "base64" and payload.get("content"):
            raw = base64.b64decode(str(payload["content"]).replace("\n", ""), validate=False)
            if b"\x00" in raw[:2048]:
                raise ValueError("binary file")
            return raw.decode("utf-8", errors="replace")
        content = payload.get("content")
        if isinstance(content, str):
            return content
        raise ExternalServiceError(f"Unable to decode file content for {path}")

    def fetch_recent_commit_count(self, repo: RepoCandidate, since: datetime) -> int:
        params = {"since": since.isoformat().replace("+00:00", "Z"), "per_page": 30}
        payload = self._request_json(
            "GET", f"https://api.github.com/repos/{repo.full_name}/commits", params=params
        )
        return len(payload) if isinstance(payload, list) else 0

    def _request_json(self, method: str, url: str, **kwargs: Any) -> Any:
        for attempt in range(3):
            response = self.session.request(method, url, timeout=30, **kwargs)
            if response.status_code == 403:
                retry_after = response.headers.get("Retry-After")
                remaining = response.headers.get("X-RateLimit-Remaining")
                reset_at = response.headers.get("X-RateLimit-Reset")
                if retry_after:
                    delay = min(int(retry_after), 60)
                    LOGGER.warning("GitHub rate limited request to %s; sleeping %ss", url, delay)
                    time.sleep(delay)
                    continue
                if remaining == "0" and reset_at:
                    delay = max(int(reset_at) - int(time.time()), 1)
                    delay = min(delay, 60)
                    LOGGER.warning(
                        "GitHub rate limit exhausted for %s; sleeping %ss until reset",
                        url,
                        delay,
                    )
                    time.sleep(delay)
                    continue
            if response.status_code in {502, 503, 504} and attempt < 2:
                time.sleep(1.5 * (attempt + 1))
                continue
            if not response.ok:
                raise ExternalServiceError(
                    f"GitHub API request failed: {response.status_code} {response.text[:300]}"
                )
            try:
                return response.json()
            except ValueError as exc:
                raise ExternalServiceError("GitHub API returned non-JSON response.") from exc
        raise ExternalServiceError(f"GitHub API request failed after retries: {url}")

    def _dry_run_candidates(self) -> list[RepoCandidate]:
        now = datetime.now(UTC)
        created = now - timedelta(days=5)
        samples = [
            (
                "nova-labs/flux-agent",
                "Rust",
                "Autonomous coding agent with sandboxed tool execution.",
                4200,
                210,
            ),
            (
                "pixelmind-ai/rag-pipeline-kit",
                "Python",
                "Production RAG pipeline with eval harness and observability.",
                3100,
                180,
            ),
            (
                "edgeforge/mcp-gateway",
                "Go",
                "Unified MCP gateway for multi-model agent orchestration.",
                2800,
                150,
            ),
            (
                "tensorlite/onnx-runner",
                "C++",
                "Cross-platform ONNX inference runtime for edge devices.",
                2500,
                120,
            ),
            (
                "cloudnative-kit/helm-gen",
                "TypeScript",
                "AI-assisted Helm chart generator with policy checks.",
                2200,
                95,
            ),
            (
                "devscribe/cli-audit",
                "Python",
                "CLI that audits repo health, CI gaps, and supply-chain risk.",
                1900,
                88,
            ),
            (
                "openmesh/sync-engine",
                "Rust",
                "CRDT-based real-time sync engine for local-first apps.",
                1700,
                76,
            ),
            (
                "promptworks/eval-bench",
                "Python",
                "Benchmark suite for LLM prompt quality and regression.",
                1500,
                70,
            ),
            (
                "byteflow/wasm-runtime-lite",
                "Rust",
                "Lightweight WASM runtime for serverless edge functions.",
                1300,
                65,
            ),
            (
                "agentkit/observability",
                "Go",
                "OpenTelemetry-native tracing for AI agent workflows.",
                1100,
                58,
            ),
            (
                "codewave/lsp-bridge",
                "TypeScript",
                "Bridge LSP servers into agent toolchains with caching.",
                980,
                52,
            ),
            (
                "modelhub/quant-kit",
                "Python",
                "Post-training quantization toolkit with accuracy reports.",
                870,
                48,
            ),
            (
                "infraops/gitops-ai",
                "Go",
                "GitOps controller with AI-generated rollout plans.",
                760,
                42,
            ),
            (
                "datasync/vector-store-lite",
                "Rust",
                "Embedded vector DB for on-device RAG.",
                650,
                38,
            ),
            (
                "buildkit/sbom-scanner",
                "Python",
                "SBOM generator and vulnerability scanner for CI.",
                540,
                32,
            ),
            (
                "neuralpipe/stream-llm",
                "C++",
                "Streaming LLM inference server with batching.",
                480,
                28,
            ),
            (
                "toolforge/mcp-tools",
                "Python",
                "Composable MCP tool library for developer agents.",
                420,
                25,
            ),
        ]
        repos: list[RepoCandidate] = []
        for index, (full_name, language, description, stars, forks) in enumerate(samples, start=1):
            owner, name = full_name.split("/", 1)
            item = {
                "full_name": full_name,
                "html_url": f"https://github.com/{full_name}",
                "description": description,
                "stargazers_count": stars,
                "forks_count": forks,
                "watchers_count": stars,
                "open_issues_count": 12 + index,
                "language": language,
                "topics": ["ai", "developer-tools", "automation"],
                "created_at": (created - timedelta(days=index)).isoformat().replace("+00:00", "Z"),
                "pushed_at": now.isoformat().replace("+00:00", "Z"),
                "updated_at": now.isoformat().replace("+00:00", "Z"),
                "default_branch": "main",
                "archived": False,
                "disabled": False,
                "owner": {"login": owner},
                "name": name,
                "license": {"spdx_id": "MIT"},
            }
            repos.append(
                RepoCandidate.from_github_api(item).with_enrichment(
                    languages={language: 120000, "Shell": 5000},
                    readme_excerpt=f"{description} Includes tests, CI, architecture docs, and deployment examples.",
                    recent_commit_count=5,
                )
            )
        return repos


class HardMetricFilter:
    def __init__(self, settings: Settings, processed_state: ProcessedState) -> None:
        self.settings = settings
        self.processed_state = processed_state
        self._recent_processed = self._recent_processed_names()

    def apply(self, repos: list[RepoCandidate]) -> list[FilterDecision]:
        return [self._decide(repo) for repo in repos]

    def accepted(self, repos: list[RepoCandidate]) -> list[RepoCandidate]:
        decisions = self.apply(repos)
        for decision in decisions:
            if not decision.accepted:
                LOGGER.debug("Filtered %s: %s", decision.repo.full_name, decision.reason)
        accepted = [decision.repo for decision in decisions if decision.accepted]
        if len(accepted) < len(repos):
            reason_counts: dict[str, int] = {}
            for decision in decisions:
                if not decision.accepted:
                    reason_counts[decision.reason] = reason_counts.get(decision.reason, 0) + 1
            top_reasons = ", ".join(f"{reason}={count}" for reason, count in reason_counts.items())
            LOGGER.info(
                "Hard metric filter summary: accepted %d/%d repos; top reasons: %s",
                len(accepted),
                len(repos),
                top_reasons,
            )
        return accepted

    def _decide(self, repo: RepoCandidate) -> FilterDecision:
        if is_legacy_megaproject(repo):
            return FilterDecision(repo, False, legacy_rejection_reason(repo))
        if repo.full_name in self._recent_processed:
            return FilterDecision(repo, False, "already audited within cache TTL")
        if repo.archived or repo.disabled:
            return FilterDecision(repo, False, "repository is archived or disabled")
        if repo.stargazers_count < self._min_stars_for_repo(repo):
            return FilterDecision(repo, False, "insufficient stars")
        if repo.created_at and repo.created_at < cutoff_datetime(
            self.settings.max_repo_age_days * 24
        ):
            return FilterDecision(repo, False, "repository older than freshness window")
        if not repo.created_at:
            return FilterDecision(repo, False, "missing repository creation date")
        if repo.fork_star_ratio < self.settings.min_fork_star_ratio:
            return FilterDecision(repo, False, "fork/star ratio below trust threshold")
        if repo.primary_language.lower() in NON_CODE_PRIMARY_LANGUAGES:
            return FilterDecision(repo, False, "primary language is non-code content")
        if repo.enrichment_failed:
            return FilterDecision(repo, False, "failed to verify repository activity signals")
        if repo.pushed_at and repo.pushed_at < cutoff_datetime(
            self.settings.require_recent_push_hours
        ):
            return FilterDecision(repo, False, "no recent push activity")
        if repo.recent_commit_count is not None and repo.recent_commit_count <= 0:
            return FilterDecision(repo, False, "no recent commits")
        if self._non_code_language_ratio(repo) > 0.80:
            return FilterDecision(repo, False, "Markdown/HTML dominates repository bytes")
        return FilterDecision(repo, True, "accepted")

    def _recent_processed_names(self) -> set[str]:
        cutoff = datetime.now(UTC).date() - timedelta(days=self.settings.cache_ttl_days)
        names: set[str] = set()
        for repo_name, record in self.processed_state.items():
            audited_at = str(record.get("audited_at", ""))
            try:
                if datetime.fromisoformat(audited_at).date() >= cutoff:
                    names.add(repo_name)
            except ValueError:
                continue
        return names

    @staticmethod
    def _non_code_language_ratio(repo: RepoCandidate) -> float:
        ratios = repo.code_language_ratio
        return sum(
            ratio
            for language, ratio in ratios.items()
            if language.lower() in NON_CODE_LANGUAGE_BYTES
        )

    def _min_stars_for_repo(self, repo: RepoCandidate) -> int:
        if repo.created_at and repo.created_at >= cutoff_datetime(7 * 24):
            return self.settings.min_stars_week
        return self.settings.min_stars
