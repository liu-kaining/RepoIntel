"""Block legacy megaprojects and encyclopedia-style audits from publication."""

from __future__ import annotations

import re

from .models import RepoAudit, RepoCandidate

# Public infrastructure repos that must never appear in a "fresh signals" digest.
LEGACY_REPO_BLOCKLIST: frozenset[str] = frozenset(
    {
        "torvalds/linux",
        "kubernetes/kubernetes",
        "nodejs/node",
        "denoland/deno",
        "golang/go",
        "microsoft/vscode",
        "vercel/next.js",
        "facebook/react",
        "tensorflow/tensorflow",
        "pytorch/pytorch",
        "apple/swift",
        "rust-lang/rust",
        "microsoft/typescript",
        "apache/spark",
        "apache/kafka",
        "redis/redis",
        "postgres/postgres",
        "ollama/ollama",
        "ggml-org/llama.cpp",
        "tauri-apps/tauri",
        "helm/helm",
        "hashicorp/terraform",
        "moby/moby",
        "docker/docker",
    }
)

# Essay templates models regurgitate for famous stacks (not acceptable as audits).
GENERIC_ESSAY_PHRASES: tuple[str, ...] = (
    "事实标准",
    "工业标准",
    "生态巨头",
    "护城河",
    "定义了",
    "毋庸置疑",
    "基石",
    "标杆",
    "教科书",
    "云原生时代",
    "React生态",
    "全栈开发",
    "统治力",
    "商业生态的核心",
    "影响整个",
    "全球数字基础设施",
)

# Buzzwords often hallucinated for famous repos without README evidence.
FAMOUS_STACK_BUZZWORDS: tuple[str, ...] = (
    "turbopack",
    "app router",
    "server components",
    "react server",
    "pages router",
    "vercel",
    "swc",
    "rsc",
    "middleware",
    "edge functions",
)


def is_legacy_megaproject(repo: RepoCandidate) -> bool:
    name = repo.full_name.lower()
    if name in LEGACY_REPO_BLOCKLIST:
        return True
    age = repo.repo_age_days
    stars = repo.stargazers_count
    if age is not None and age > 30:
        return True
    if stars >= 10_000:
        return True
    if stars >= 3_000 and age is not None and age > 14:
        return True
    return False


def legacy_rejection_reason(repo: RepoCandidate) -> str:
    if repo.full_name.lower() in LEGACY_REPO_BLOCKLIST:
        return "blocklisted legacy megaproject"
    if repo.repo_age_days is not None and repo.repo_age_days > 30:
        return f"repository age {repo.repo_age_days}d exceeds fresh-signal window"
    if repo.stargazers_count >= 10_000:
        return "star count indicates established megaproject"
    return "legacy megaproject heuristics"


def is_blocked_repo_name(repo_name: str) -> bool:
    return repo_name.lower() in LEGACY_REPO_BLOCKLIST


def should_reject_publication(repo: RepoCandidate, audit: RepoAudit) -> tuple[bool, str]:
    if audit.code_chars_analyzed <= 0:
        return True, "no source code was analyzed"
    if is_legacy_megaproject(repo):
        return True, legacy_rejection_reason(repo)
    combined = f"{audit.summary}\n{audit.technical_review}\n{audit.pain_point}"
    essay_hits = sum(1 for phrase in GENERIC_ESSAY_PHRASES if phrase in combined)
    if essay_hits >= 2:
        return True, "encyclopedia-style generic essay (not README-grounded audit)"
    grounding_issues = readme_grounding_issues(repo, combined)
    if grounding_issues:
        return True, grounding_issues[0]
    if audit.code_files_reviewed and len(audit.code_files_reviewed) < 3:
        return True, "insufficient source files in code audit"
    return False, ""


def readme_grounding_issues(repo: RepoCandidate, text: str) -> list[str]:
    readme = repo.readme_excerpt.strip()
    if len(readme) < 80:
        return ["README 过短，无法做锚定审计"]
    issues: list[str] = []
    readme_lower = readme.lower()
    text_lower = text.lower()

    leak_hits = [
        term for term in FAMOUS_STACK_BUZZWORDS if term in text_lower and term not in readme_lower
    ]
    if leak_hits:
        issues.append(f"审计疑似套用知名项目先验而非 README: {', '.join(leak_hits[:4])}")

    readme_tokens = _significant_tokens(readme_lower)
    review_tokens = _significant_tokens(text_lower)
    if not readme_tokens:
        return issues
    overlap = len(readme_tokens & review_tokens)
    if len(readme_tokens) >= 12 and overlap < 3:
        issues.append("审计与 README 关键词重叠过低，属于百科式空话")
    if not _has_readme_quote_cue(text):
        issues.append("未引用 README 原文依据（缺「」或 README/文档 指称）")
    return issues


def _significant_tokens(text: str) -> set[str]:
    tokens = re.findall(r"[a-z][a-z0-9_-]{3,}|[\u4e00-\u9fff]{2,}", text)
    stop = {
        "the",
        "and",
        "for",
        "with",
        "this",
        "that",
        "from",
        "have",
        "project",
        "github",
        "readme",
        "repo",
        "开源",
        "项目",
        "框架",
        "工具",
        "技术",
        "工程",
        "社区",
        "版本",
        "支持",
        "使用",
        "提供",
        "实现",
        "应用",
        "开发",
        "服务",
        "系统",
        "平台",
        "一个",
        "可以",
        "通过",
        "进行",
        "主要",
        "相关",
        "以及",
        "具有",
        "目前",
        "已经",
        "作为",
    }
    return {token for token in tokens if token not in stop}


def _has_readme_quote_cue(text: str) -> bool:
    if "README" in text or "readme" in text or "文档" in text:
        return True
    if "「" in text and "」" in text:
        return True
    if '"' in text or "'" in text:
        return True
    return False
