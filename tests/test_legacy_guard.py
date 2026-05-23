from __future__ import annotations

from datetime import UTC, datetime, timedelta

from repointel.legacy_guard import (
    is_legacy_megaproject,
    readme_grounding_issues,
    should_reject_publication,
)
from repointel.models import RepoAudit, RepoCandidate, Scores


def _repo(full_name: str, *, stars: int = 500, age_days: int = 10) -> RepoCandidate:
    now = datetime.now(UTC)
    owner, name = full_name.split("/", 1)
    return RepoCandidate.from_github_api(
        {
            "full_name": full_name,
            "html_url": f"https://github.com/{full_name}",
            "description": "A new tool",
            "stargazers_count": stars,
            "forks_count": max(stars // 20, 5),
            "watchers_count": stars,
            "open_issues_count": 3,
            "language": "Rust",
            "topics": ["ai"],
            "created_at": (now - timedelta(days=age_days)).isoformat().replace("+00:00", "Z"),
            "pushed_at": now.isoformat().replace("+00:00", "Z"),
            "updated_at": now.isoformat().replace("+00:00", "Z"),
            "default_branch": "main",
            "archived": False,
            "disabled": False,
            "owner": {"login": owner},
            "name": name,
        }
    ).with_enrichment(
        readme_excerpt=(
            "Install with `cargo install foo`. Provides a CLI for batch indexing local repos. "
            "Supports plugins and config files documented in docs/guide.md."
        ),
        recent_commit_count=5,
    )


def test_nextjs_is_legacy_blocklisted() -> None:
    repo = _repo("vercel/next.js", stars=130000, age_days=3000)
    assert is_legacy_megaproject(repo)


def test_encyclopedia_audit_rejected() -> None:
    repo = _repo("acme/new-tool", stars=800, age_days=12)
    audit = RepoAudit(
        repo_name=repo.full_name,
        repo_link=repo.html_url,
        category="Web",
        tags=["TypeScript"],
        scores=Scores(85, 90, 80, 70),
        summary="React生态的事实标准框架，构建了强大的商业护城河。",
        pain_point="解决全栈复杂度。",
        technical_review=(
            "亮点：Turbopack 与 App Router 代表未来。疑点：架构复杂。"
            "建议：团队可评估。未引用任何 README 内容。"
        ),
        commercial_value="影响前端生态。",
        hidden_risks=["厂商锁定"],
        code_files_reviewed=("src/main.rs",),
        code_source="git",
        code_chars_analyzed=5000,
    )
    reject, reason = should_reject_publication(repo, audit)
    assert reject
    assert "百科" in reason or "先验" in reason or "README" in reason


def test_readme_grounding_flags_hallucinated_stack_terms() -> None:
    repo = _repo("acme/new-tool", stars=500, age_days=8)
    issues = readme_grounding_issues(
        repo,
        "该项目使用 Turbopack 与 App Router，是 React 生态事实标准。",
    )
    assert issues
    assert any("先验" in issue for issue in issues)
