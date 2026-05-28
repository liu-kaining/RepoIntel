from __future__ import annotations

from datetime import UTC, datetime, timedelta

from conftest import CODE_SETTINGS_KWARGS
from repointel.config import Settings
from repointel.github_client import HardMetricFilter
from repointel.models import RepoAudit, RepoCandidate, Scores
from repointel.r2_manager import merge_audits_into_state


def _settings(tmp_path) -> Settings:
    return Settings(
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


def _repo(**overrides) -> RepoCandidate:
    now = datetime.now(UTC)
    created_at = (now - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    pushed_at = (now - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
    item = {
        "full_name": "owner/repo",
        "html_url": "https://github.com/owner/repo",
        "description": "Useful infra tool",
        "stargazers_count": 1000,
        "forks_count": 30,
        "watchers_count": 1000,
        "open_issues_count": 5,
        "language": "Go",
        "topics": ["infra"],
        "created_at": created_at,
        "pushed_at": pushed_at,
        "updated_at": pushed_at,
        "default_branch": "main",
        "archived": False,
        "disabled": False,
        "owner": {"login": "owner"},
        "name": "repo",
    }
    item.update(overrides)
    return RepoCandidate.from_github_api(item).with_enrichment(
        languages={"Go": 1000}, recent_commit_count=3
    )


def test_hard_filter_rejects_low_fork_star_ratio(tmp_path) -> None:
    settings = _settings(tmp_path)
    repo = _repo(forks_count=1)
    decision = HardMetricFilter(settings, {}).apply([repo])[0]
    assert not decision.accepted
    assert "fork/star" in decision.reason


def test_hard_filter_rejects_failed_enrichment(tmp_path) -> None:
    settings = _settings(tmp_path)
    repo = _repo().with_enrichment(enrichment_failed=True)
    decision = HardMetricFilter(settings, {}).apply([repo])[0]
    assert not decision.accepted
    assert "failed to verify" in decision.reason


def test_hard_filter_rejects_stale_repository(tmp_path) -> None:
    settings = _settings(tmp_path)
    repo = _repo(created_at="2024-01-01T00:00:00Z")
    decision = HardMetricFilter(settings, {}).apply([repo])[0]
    assert not decision.accepted
    assert "fresh-signal" in decision.reason or "older than" in decision.reason


def test_state_merge_prunes_old_records_and_adds_audits() -> None:
    audit = RepoAudit(
        repo_name="owner/new",
        repo_link="https://github.com/owner/new",
        category="Infrastructure",
        tags=["Go"],
        scores=Scores(80, 80, 80, 80),
        summary="Summary.",
        pain_point="Pain.",
        technical_review="Review.",
        commercial_value="Value.",
        hidden_risks=["Risk."],
    )
    merged = merge_audits_into_state(
        {
            "owner/old": {"repo_name": "owner/old", "audited_at": "2026-04-01"},
            "owner/recent": {"repo_name": "owner/recent", "audited_at": "2026-05-20"},
        },
        [audit],
        now=datetime(2026, 5, 23, tzinfo=UTC),
        ttl_days=14,
    )
    assert "owner/old" not in merged
    assert "owner/recent" in merged
    assert merged["owner/new"]["score"] == 80.0
