"""Post-LLM score calibration — enforce conservative scoring when evidence is thin."""

from __future__ import annotations

from .legacy_guard import is_legacy_megaproject, readme_grounding_issues
from .models import RepoCandidate, Scores

# Marketing fluff that should not appear without substance in technical_review.
HYPE_PHRASES = (
    "全球首创",
    "颠覆",
    "划时代",
    "天花板",
    "革命性",
    "game-changer",
    "revolutionary",
    "改变世界",
    "最强",
    "遥遥领先",
)


def calibrate_scores(repo: RepoCandidate, scores: Scores) -> Scores:
    """Apply deterministic caps so LLM grade inflation cannot bypass evidence limits."""
    if is_legacy_megaproject(repo):
        return Scores(innovation=40, utility=42, engineering=45, health=40)

    innovation = scores.innovation
    utility = scores.utility
    engineering = scores.engineering
    health = scores.health

    readme_len = len(repo.readme_excerpt.strip())

    if readme_len < 150:
        innovation = min(innovation, 62)
        utility = min(utility, 65)
        engineering = min(engineering, 58)
    elif readme_len < 500:
        innovation = min(innovation, 72)
        utility = min(utility, 75)
        engineering = min(engineering, 68)
    elif readme_len < 1200:
        innovation = min(innovation, 82)
        utility = min(utility, 84)
        engineering = min(engineering, 78)

    commits = repo.recent_commit_count
    if commits is None or commits < 2:
        health = min(health, 66)
    elif commits < 5:
        health = min(health, 74)

    if repo.fork_star_ratio < 0.012:
        health = min(health, 70)
    elif repo.fork_star_ratio < 0.02:
        health = min(health, 76)

    # High stars but weak fork adoption — common astroturf / hype pattern
    if repo.stargazers_count >= 800 and repo.fork_star_ratio < 0.018:
        health = min(health, 72)
        utility = min(utility, 78)

    dims = (innovation, utility, engineering, health)
    if all(value >= 78 for value in dims):
        innovation = max(0, innovation - 4)
        utility = max(0, utility - 4)
    if all(value >= 85 for value in dims):
        innovation = min(innovation, 82)
        utility = min(utility, 82)
        engineering = min(engineering, 80)
        health = min(health, 80)

    return Scores(
        innovation=_clamp(innovation),
        utility=_clamp(utility),
        engineering=_clamp(engineering),
        health=_clamp(health),
    )


def review_quality_issues(
    repo: RepoCandidate,
    technical_review: str,
    summary: str,
    *,
    code_paths: tuple[str, ...] | list[str] = (),
) -> list[str]:
    """Return human-readable quality flags (logged; also useful for risk injection)."""
    issues: list[str] = []
    review = technical_review.strip()
    if len(review) < 120:
        issues.append("technical_review 过短，审计深度不足")
    if len(summary.strip()) > 60:
        issues.append("summary 过长，可能含废话")
    hype_hits = [phrase for phrase in HYPE_PHRASES if phrase.lower() in review.lower() or phrase in review]
    if hype_hits and len(review) < 220:
        issues.append(f"审计文案含营销用语且缺乏展开: {', '.join(hype_hits[:3])}")
    if len(repo.readme_excerpt.strip()) < 200 and "信息不足" not in review:
        issues.append("README 信息不足但审计未明确声明保守评分")
    if not _has_audit_structure(review):
        issues.append("technical_review 缺少亮点/疑点/建议结构")
    issues.extend(readme_grounding_issues(repo, review))
    if code_paths and not _cites_code_paths(technical_review, code_paths):
        issues.append("technical_review 未引用任何已审阅源码路径（path 级证据缺失）")
    return issues


def _cites_code_paths(text: str, code_paths: tuple[str, ...] | list[str]) -> bool:
    for path in code_paths:
        if path in text:
            return True
    return False


def merge_quality_risks(existing: list[str], issues: list[str], *, max_items: int = 8) -> list[str]:
    merged = list(existing)
    for issue in issues:
        if issue not in merged:
            merged.append(issue)
    return merged[:max_items]


def _has_audit_structure(text: str) -> bool:
    cues = ("亮点", "疑点", "雷点", "建议", "风险", "落地", "不足", "限制")
    hits = sum(1 for cue in cues if cue in text)
    return hits >= 2


def _clamp(value: int) -> int:
    return max(0, min(100, value))
