from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any


@dataclass(frozen=True)
class RepoCandidate:
    full_name: str
    html_url: str
    description: str
    stargazers_count: int
    forks_count: int
    watchers_count: int
    open_issues_count: int
    language: str | None
    topics: list[str]
    created_at: datetime | None
    pushed_at: datetime | None
    updated_at: datetime | None
    default_branch: str
    archived: bool
    disabled: bool
    owner: str
    name: str
    license_name: str | None = None
    languages: dict[str, int] = field(default_factory=dict)
    readme_excerpt: str = ""
    recent_commit_count: int | None = None
    enrichment_failed: bool = False

    @classmethod
    def from_github_api(cls, item: dict[str, Any]) -> RepoCandidate:
        owner = item.get("owner") or {}
        license_info = item.get("license") or {}
        return cls(
            full_name=str(item["full_name"]),
            html_url=str(item["html_url"]),
            description=item.get("description") or "",
            stargazers_count=int(item.get("stargazers_count") or 0),
            forks_count=int(item.get("forks_count") or 0),
            watchers_count=int(item.get("watchers_count") or 0),
            open_issues_count=int(item.get("open_issues_count") or 0),
            language=item.get("language"),
            topics=list(item.get("topics") or []),
            created_at=parse_github_datetime(item.get("created_at")),
            pushed_at=parse_github_datetime(item.get("pushed_at")),
            updated_at=parse_github_datetime(item.get("updated_at")),
            default_branch=item.get("default_branch") or "main",
            archived=bool(item.get("archived")),
            disabled=bool(item.get("disabled")),
            owner=owner.get("login") or str(item["full_name"]).split("/", 1)[0],
            name=str(item.get("name") or str(item["full_name"]).split("/", 1)[-1]),
            license_name=license_info.get("spdx_id") or license_info.get("name"),
        )

    @property
    def fork_star_ratio(self) -> float:
        if self.stargazers_count <= 0:
            return 0.0
        return self.forks_count / self.stargazers_count

    @property
    def primary_language(self) -> str:
        return (self.language or "Unknown").strip() or "Unknown"

    @property
    def code_language_ratio(self) -> dict[str, float]:
        total = sum(max(v, 0) for v in self.languages.values())
        if total <= 0:
            return {}
        return {language: bytes_count / total for language, bytes_count in self.languages.items()}

    def with_enrichment(
        self,
        *,
        languages: dict[str, int] | None = None,
        readme_excerpt: str | None = None,
        recent_commit_count: int | None = None,
        enrichment_failed: bool | None = None,
    ) -> RepoCandidate:
        return RepoCandidate(
            full_name=self.full_name,
            html_url=self.html_url,
            description=self.description,
            stargazers_count=self.stargazers_count,
            forks_count=self.forks_count,
            watchers_count=self.watchers_count,
            open_issues_count=self.open_issues_count,
            language=self.language,
            topics=self.topics,
            created_at=self.created_at,
            pushed_at=self.pushed_at,
            updated_at=self.updated_at,
            default_branch=self.default_branch,
            archived=self.archived,
            disabled=self.disabled,
            owner=self.owner,
            name=self.name,
            license_name=self.license_name,
            languages=languages if languages is not None else self.languages,
            readme_excerpt=readme_excerpt if readme_excerpt is not None else self.readme_excerpt,
            recent_commit_count=(
                recent_commit_count if recent_commit_count is not None else self.recent_commit_count
            ),
            enrichment_failed=(
                enrichment_failed if enrichment_failed is not None else self.enrichment_failed
            ),
        )

    @property
    def repo_age_days(self) -> int | None:
        if not self.created_at:
            return None
        delta = datetime.now(UTC) - self.created_at
        return max(delta.days, 0)

    def to_llm_context(self) -> dict[str, Any]:
        non_code_ratio = sum(
            ratio
            for lang, ratio in self.code_language_ratio.items()
            if lang.lower() in {"markdown", "html"}
        )
        return {
            "full_name": self.full_name,
            "url": self.html_url,
            "description": self.description,
            "stars": self.stargazers_count,
            "forks": self.forks_count,
            "fork_star_ratio": round(self.fork_star_ratio, 4),
            "open_issues": self.open_issues_count,
            "primary_language": self.primary_language,
            "topics": self.topics,
            "license": self.license_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "repo_age_days": self.repo_age_days,
            "pushed_at": self.pushed_at.isoformat() if self.pushed_at else None,
            "recent_commit_count": self.recent_commit_count,
            "readme_length": len(self.readme_excerpt.strip()),
            "non_code_byte_ratio": round(non_code_ratio, 3) if non_code_ratio else None,
            "language_bytes": self.languages,
            "readme_excerpt": self.readme_excerpt[:6000],
        }


@dataclass(frozen=True)
class Scores:
    innovation: int
    utility: int
    engineering: int
    health: int

    def __post_init__(self) -> None:
        for name, value in self.as_dict().items():
            if not 0 <= value <= 100:
                raise ValueError(f"{name} score must be between 0 and 100, got {value}.")

    @property
    def total_score(self) -> float:
        return round(
            0.30 * self.innovation
            + 0.30 * self.utility
            + 0.25 * self.engineering
            + 0.15 * self.health,
            2,
        )

    def as_dict(self) -> dict[str, int]:
        return {
            "innovation": self.innovation,
            "utility": self.utility,
            "engineering": self.engineering,
            "health": self.health,
        }


@dataclass(frozen=True)
class SourceFile:
    path: str
    content: str
    size_bytes: int
    category: str
    truncated: bool = False


@dataclass(frozen=True)
class RepoCodeBundle:
    repo_name: str
    source: str
    default_branch: str
    tree_file_count: int
    selected_paths: tuple[str, ...]
    files: tuple[SourceFile, ...]
    skipped: list[str]
    gather_note: str

    @property
    def total_chars(self) -> int:
        return sum(len(file.content) for file in self.files)

    def to_llm_payload(self) -> dict[str, Any]:
        return {
            "gather": {
                "source": self.source,
                "branch": self.default_branch,
                "tree_file_count": self.tree_file_count,
                "files_included": len(self.files),
                "total_chars": self.total_chars,
                "note": self.gather_note,
                "skipped": self.skipped[:20],
            },
            "files": [
                {
                    "path": file.path,
                    "category": file.category,
                    "truncated": file.truncated,
                    "size_bytes": file.size_bytes,
                    "content": file.content,
                }
                for file in self.files
            ],
        }


@dataclass(frozen=True)
class RepoAudit:
    repo_name: str
    repo_link: str
    category: str
    tags: list[str]
    scores: Scores
    summary: str
    pain_point: str
    technical_review: str
    commercial_value: str
    hidden_risks: list[str]
    code_files_reviewed: tuple[str, ...] = ()
    code_source: str = ""
    code_chars_analyzed: int = 0

    @property
    def total_score(self) -> float:
        return self.scores.total_score

    def to_front_matter(self, published_at: datetime) -> dict[str, Any]:
        return {
            "title": f"[Score: {self.total_score}] {self.repo_name}",
            "date": published_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "categories": [self.category],
            "tags": self.tags,
            "intel_score": self.total_score,
            "repo_name": self.repo_name,
            "repo_link": self.repo_link,
            "summary": self.summary,
            "code_source": self.code_source,
            "code_files_reviewed": list(self.code_files_reviewed),
            "code_chars_analyzed": self.code_chars_analyzed,
        }

    def to_cache_record(self, audited_at: datetime) -> dict[str, Any]:
        return {
            "repo_name": self.repo_name,
            "repo_link": self.repo_link,
            "audited_at": audited_at.date().isoformat(),
            "score": self.total_score,
        }


@dataclass(frozen=True)
class FilterDecision:
    repo: RepoCandidate
    accepted: bool
    reason: str


ProcessedState = dict[str, dict[str, Any]]


def parse_github_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def cutoff_datetime(hours: int) -> datetime:
    return datetime.now(UTC) - timedelta(hours=hours)
