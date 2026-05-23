from __future__ import annotations

from datetime import UTC, datetime

from repointel.config import Settings
from repointel.content_gen import ContentGenerator
from repointel.models import RepoAudit, Scores


def test_content_generator_filters_and_writes(tmp_path) -> None:
    settings = Settings(
        github_token=None,
        llm_provider="openai",
        llm_base_url=None,
        llm_model="test",
        llm_api_key="key",
        rough_llm_model=None,
        r2_endpoint_url=None,
        r2_access_key_id=None,
        r2_secret_access_key=None,
        r2_bucket_name=None,
        r2_cache_key="processed_repos.json",
        state_backend="local",
        local_state_path=tmp_path / "state.json",
        hugo_content_dir=tmp_path / "content",
        output_dir=tmp_path / "output",
        max_candidates=100,
        rough_screen_limit=15,
        final_publish_limit=10,
        score_threshold=75,
        cache_ttl_days=14,
        min_fork_star_ratio=0.01,
        min_stars=50,
        require_recent_push_hours=48,
        dry_run=False,
    )
    audit = RepoAudit(
        repo_name="owner/repo",
        repo_link="https://github.com/owner/repo",
        category="Infrastructure",
        tags=["Rust"],
        scores=Scores(80, 90, 70, 60),
        summary="Summary.",
        pain_point="Pain.",
        technical_review="Review.",
        commercial_value="Value.",
        hidden_risks=["Risk."],
    )
    published = ContentGenerator(settings).publish([audit], now=datetime(2026, 5, 23, tzinfo=UTC))
    assert len(published) == 1
    assert (tmp_path / "content" / "2026-05-23-owner-repo.md").exists()
    assert "owner/repo" in (tmp_path / "output" / "wechat_digest.txt").read_text(encoding="utf-8")
