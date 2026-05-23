from __future__ import annotations

import logging
from datetime import UTC, datetime

from .ai_engine import AIEngine
from .config import Settings
from .content_gen import ContentGenerator
from .exceptions import RepoIntelError
from .github_client import GitHubClient, HardMetricFilter
from .logging_utils import configure_logging
from .r2_manager import build_state_store, merge_audits_into_state

LOGGER = logging.getLogger(__name__)


class RepoIntelPipeline:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.github = GitHubClient(settings)
        self.ai = AIEngine(settings)
        self.content = ContentGenerator(settings)
        self.state_store = build_state_store(settings)

    def run(self) -> int:
        now = datetime.now(UTC)
        state = self.state_store.load()
        LOGGER.info("Loaded %d processed repo records", len(state))

        candidates = self.github.discover_candidates()
        enriched = self.github.enrich_candidates(candidates)
        eligible = HardMetricFilter(self.settings, state).accepted(enriched)
        LOGGER.info("Hard metric filter accepted %d/%d repos", len(eligible), len(enriched))

        audits = self.ai.analyze_repos(eligible)
        published = self.content.publish(audits, now=now)
        LOGGER.info("Published %d RepoIntel entries", len(published))

        # Cache every deep-audited repo, not only published ones, to avoid
        # re-spending LLM tokens on sub-threshold repos within the TTL window.
        updated_state = merge_audits_into_state(
            state,
            audits,
            now=now,
            ttl_days=self.settings.cache_ttl_days,
        )
        self.state_store.save(updated_state)
        LOGGER.info("Saved %d processed repo records", len(updated_state))
        return 0


def main() -> None:
    configure_logging()
    try:
        settings = Settings.from_env()
        exit_code = RepoIntelPipeline(settings).run()
    except RepoIntelError as exc:
        LOGGER.error("RepoIntel failed: %s", exc)
        raise SystemExit(1) from exc
    raise SystemExit(exit_code)
