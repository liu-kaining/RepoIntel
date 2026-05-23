from __future__ import annotations

from datetime import UTC, datetime, timedelta

from repointel.models import RepoCandidate, Scores
from repointel.scoring import calibrate_scores, review_quality_issues


def _repo(**kwargs) -> RepoCandidate:
    readme = str(kwargs.pop("readme", "x" * 400))
    recent_commit_count = int(kwargs.pop("recent_commit_count", 5))
    now = datetime.now(UTC)
    base = {
        "full_name": "owner/repo",
        "html_url": "https://github.com/owner/repo",
        "description": "Tool",
        "stargazers_count": 1200,
        "forks_count": 24,
        "watchers_count": 1200,
        "open_issues_count": 3,
        "language": "Rust",
        "topics": ["ai"],
        "created_at": (now - timedelta(days=10)).isoformat().replace("+00:00", "Z"),
        "pushed_at": now.isoformat().replace("+00:00", "Z"),
        "updated_at": now.isoformat().replace("+00:00", "Z"),
        "default_branch": "main",
        "archived": False,
        "disabled": False,
        "owner": {"login": "owner"},
        "name": "repo",
    }
    base.update(kwargs)
    return RepoCandidate.from_github_api(base).with_enrichment(
        readme_excerpt=readme,
        recent_commit_count=recent_commit_count,
    )


def test_calibrate_scores_caps_short_readme() -> None:
    repo = _repo(readme="short")
    raw = Scores(innovation=92, utility=90, engineering=88, health=85)
    calibrated = calibrate_scores(repo, raw)
    assert calibrated.engineering <= 58
    assert calibrated.innovation <= 62
    assert calibrated.total_score < 75


def test_calibrate_scores_penalizes_grade_inflation() -> None:
    repo = _repo(readme="x" * 2000)
    raw = Scores(innovation=88, utility=87, engineering=86, health=85)
    calibrated = calibrate_scores(repo, raw)
    assert calibrated.innovation <= 84
    assert calibrated.utility <= 84


def test_review_quality_flags_missing_structure() -> None:
    repo = _repo(readme="x" * 50)
    issues = review_quality_issues(repo, "很好很强大。", "一个很好的项目。")
    assert any("结构" in issue or "过短" in issue or "信息不足" in issue for issue in issues)
