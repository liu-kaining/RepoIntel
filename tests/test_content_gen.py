from __future__ import annotations

from datetime import UTC, datetime

from conftest import CODE_SETTINGS_KWARGS
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
        min_stars=300,
        min_stars_week=100,
        max_repo_age_days=30,
        require_recent_push_hours=48,
        dry_run=False,
        **CODE_SETTINGS_KWARGS,
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
        code_files_reviewed=("src/main.rs", "Cargo.toml"),
        code_source="git",
        code_chars_analyzed=12_000,
    )
    published = ContentGenerator(settings).publish([audit], now=datetime(2026, 5, 23, tzinfo=UTC))
    assert len(published) == 1
    assert (tmp_path / "content" / "2026-05-23-owner-repo.md").exists()
    assert "owner/repo" in (tmp_path / "output" / "wechat_digest.txt").read_text(encoding="utf-8")

    post = (tmp_path / "content" / "2026-05-23-owner-repo.md").read_text(encoding="utf-8")
    assert "path-chip" in post
    assert "content-panel--audit" in post


def test_audit_prose_splits_sections_and_paths() -> None:
    from repointel.content_gen import _format_audit_prose

    text = (
        "架构与核心链路：入口在 cmd/bumblebee/main.go。\n"
        "亮点1：`internal/walk/walk.go` 设计清晰。\n"
        "疑点1：internal/walk/dirkey_unix.go :10 可能有问题。\n"
        "落地建议：先跑 baseline。"
    )
    rendered = _format_audit_prose(text)
    assert "audit-callout--intro" in rendered
    assert "audit-callout--highlight" in rendered
    assert "audit-callout--doubt" in rendered
    assert "dirkey_unix.go:10" in rendered
    assert "internal/wa</code>" not in rendered
