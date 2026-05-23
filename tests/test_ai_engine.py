from __future__ import annotations

from repointel.ai_engine import AIEngine, _audit_from_payload, _extract_json
from repointel.config import Settings
from repointel.exceptions import LLMResponseError
from repointel.github_client import GitHubClient
from repointel.models import RepoCandidate, RepoCodeBundle, SourceFile


def test_extract_json_from_markdown_code_block() -> None:
    payload = _extract_json('```json\n{"selected": ["a/b"]}\n```')
    assert payload == {"selected": ["a/b"]}


def test_extract_json_ignores_leading_and_trailing_text() -> None:
    payload = _extract_json('Here is the result:\n{"selected": ["a/b"]}\nThanks.')
    assert payload == {"selected": ["a/b"]}


def test_extract_json_handles_nested_objects() -> None:
    payload = _extract_json('{"selected": ["a/b"], "meta": {"count": 1}}')
    assert payload["meta"]["count"] == 1


def _repo_candidate(name: str = "owner/repo") -> RepoCandidate:
    owner, repo = name.split("/", 1)
    return RepoCandidate.from_github_api(
        {
            "full_name": name,
            "html_url": f"https://github.com/{name}",
            "description": "Useful infra tool",
            "stargazers_count": 1000,
            "forks_count": 50,
            "watchers_count": 1000,
            "open_issues_count": 5,
            "language": "Rust",
            "topics": ["infra"],
            "pushed_at": "2026-05-23T00:00:00Z",
            "updated_at": "2026-05-23T00:00:00Z",
            "default_branch": "main",
            "archived": False,
            "disabled": False,
            "owner": {"login": owner},
            "name": repo,
        }
    )


def test_audit_total_score_is_recomputed_locally() -> None:
    repo = _repo_candidate().with_enrichment(
        readme_excerpt="x" * 1200,
        recent_commit_count=6,
    )
    code_bundle = RepoCodeBundle(
        repo_name="owner/repo",
        source="test",
        default_branch="main",
        tree_file_count=20,
        selected_paths=("src/main.rs",),
        files=(
            SourceFile(
                path="src/main.rs",
                content="fn main() { println!(\"ok\"); }",
                size_bytes=32,
                category="source",
                truncated=False,
            ),
        ),
        skipped=[],
        gather_note="unit-test",
    )
    audit = _audit_from_payload(
        repo,
        {
            "repo_name": "owner/repo",
            "category": "Infrastructure",
            "tags": ["Rust"],
            "scores": {
                "innovation": 80,
                "utility": 90,
                "engineering": 70,
                "health": 60,
                "total_score": 100,
            },
            "summary": "Strong tool.",
            "pain_point": "Pain point.",
            "technical_review": (
                "亮点：`src/main.rs:1` 提供可执行入口。"
                "疑点：`src/main.rs` 尚未看到错误处理。"
                "建议：补充 tests/ 后再评估工程分。"
            ),
        },
        code_bundle,
    )
    assert audit.total_score == 77.5


def test_rough_screen_falls_back_to_metric_ordering(monkeypatch) -> None:
    monkeypatch.setenv("REPOINTEL_STATE_BACKEND", "local")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    settings = Settings.from_env()

    class FailingAIEngine(AIEngine):
        def _complete(self, _message):  # type: ignore[no-untyped-def]
            raise LLMResponseError("model unavailable")

    repos = [_repo_candidate("owner/a"), _repo_candidate("owner/b")]
    github = GitHubClient(settings)
    selected = FailingAIEngine(settings, github).rough_screen(repos)
    assert [repo.full_name for repo in selected] == ["owner/a", "owner/b"]
