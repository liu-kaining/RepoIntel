from __future__ import annotations

from repointel.ai_engine import _audit_from_payload, _extract_json
from repointel.models import RepoCandidate


def test_extract_json_from_markdown_code_block() -> None:
    payload = _extract_json('```json\n{"selected": ["a/b"]}\n```')
    assert payload == {"selected": ["a/b"]}


def test_extract_json_ignores_leading_and_trailing_text() -> None:
    payload = _extract_json('Here is the result:\n{"selected": ["a/b"]}\nThanks.')
    assert payload == {"selected": ["a/b"]}


def test_extract_json_handles_nested_objects() -> None:
    payload = _extract_json('{"selected": ["a/b"], "meta": {"count": 1}}')
    assert payload["meta"]["count"] == 1


def test_audit_total_score_is_recomputed_locally() -> None:
    repo = RepoCandidate.from_github_api(
        {
            "full_name": "owner/repo",
            "html_url": "https://github.com/owner/repo",
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
            "owner": {"login": "owner"},
            "name": "repo",
        }
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
            "technical_review": "Detailed review.",
            "commercial_value": "Value.",
            "hidden_risks": ["Risk."],
        },
    )
    assert audit.total_score == 77.5
