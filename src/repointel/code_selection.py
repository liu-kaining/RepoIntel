"""Select which repository files to read for deep code audit."""

from __future__ import annotations

from dataclasses import dataclass

# Directories we never descend into for source review.
SKIP_DIR_PARTS = frozenset(
    {
        ".git",
        "node_modules",
        "vendor",
        "dist",
        "build",
        "out",
        "target",
        "__pycache__",
        ".venv",
        "venv",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".next",
        ".nuxt",
        "coverage",
        "htmlcov",
        "site-packages",
        "third_party",
        "extern",
        "testdata/fixtures",
    }
)

SKIP_EXTENSIONS = frozenset(
    {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".ico",
        ".svg",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".mp4",
        ".mp3",
        ".wasm",
        ".so",
        ".dylib",
        ".dll",
        ".exe",
        ".bin",
        ".dat",
        ".lock",
        ".sum",
        ".min.js",
        ".min.css",
        ".map",
    }
)

PRIORITY_MANIFESTS = (
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "go.sum",
    "requirements.txt",
    "setup.py",
    "Makefile",
    "docker-compose.yml",
    "Dockerfile",
    "CMakeLists.txt",
    "build.gradle",
    "build.gradle.kts",
    "pom.xml",
)

PRIORITY_ENTRY_NAMES = (
    "main.rs",
    "lib.rs",
    "main.go",
    "main.py",
    "index.ts",
    "index.tsx",
    "index.js",
    "app.py",
    "mod.rs",
    "__init__.py",
)

SOURCE_EXTENSIONS = frozenset(
    {
        ".py",
        ".rs",
        ".go",
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        ".java",
        ".kt",
        ".kts",
        ".c",
        ".cc",
        ".cpp",
        ".h",
        ".hpp",
        ".cs",
        ".rb",
        ".php",
        ".swift",
        ".m",
        ".mm",
        ".lua",
        ".zig",
        ".toml",
        ".yaml",
        ".yml",
        ".json",
        ".md",
        ".sh",
        ".bash",
        ".zsh",
        ".sql",
        ".proto",
    }
)

SOURCE_DIR_PREFIXES = (
    "src/",
    "lib/",
    "pkg/",
    "internal/",
    "cmd/",
    "crates/",
    "apps/",
    "packages/",
    "core/",
    "server/",
    "cli/",
    "api/",
)

TEST_DIR_MARKERS = ("/tests/", "/test/", "/__tests__/", "/spec/", "/testing/")


@dataclass(frozen=True)
class TreeEntry:
    path: str
    size: int


@dataclass(frozen=True)
class SelectedPath:
    path: str
    size: int
    priority: int
    category: str


def select_paths_for_audit(
    entries: list[TreeEntry],
    *,
    max_files: int,
    max_file_bytes: int,
) -> list[SelectedPath]:
    candidates: list[SelectedPath] = []
    for entry in entries:
        if entry.size > max_file_bytes:
            continue
        if not _is_reviewable_path(entry.path):
            continue
        priority, category = _score_path(entry.path)
        if priority <= 0:
            continue
        candidates.append(
            SelectedPath(
                path=entry.path,
                size=entry.size,
                priority=priority,
                category=category,
            )
        )

    candidates.sort(key=lambda item: (-item.priority, item.size, item.path))
    chosen: list[SelectedPath] = []
    seen: set[str] = set()
    category_counts: dict[str, int] = {}

    for item in candidates:
        if item.path in seen:
            continue
        cap = _category_cap(item.category, max_files)
        if category_counts.get(item.category, 0) >= cap:
            continue
        chosen.append(item)
        seen.add(item.path)
        category_counts[item.category] = category_counts.get(item.category, 0) + 1
        if len(chosen) >= max_files:
            break

    return chosen


def _category_cap(category: str, max_files: int) -> int:
    if category == "manifest":
        return max(6, max_files // 8)
    if category == "ci":
        return max(4, max_files // 10)
    if category == "test":
        return max(6, max_files // 6)
    if category == "entry":
        return max(8, max_files // 5)
    return max_files


def _is_reviewable_path(path: str) -> bool:
    normalized = path.replace("\\", "/").lstrip("./")
    lower = normalized.lower()
    parts = lower.split("/")
    if any(part in SKIP_DIR_PARTS for part in parts):
        return False
    if any(lower.endswith(ext) for ext in SKIP_EXTENSIONS):
        return False
    if normalized.count("/") > 12:
        return False
    return True


def _score_path(path: str) -> tuple[int, str]:
    name = path.rsplit("/", 1)[-1]
    lower = path.lower()

    if name in PRIORITY_MANIFESTS:
        return 100, "manifest"
    if lower.startswith(".github/workflows/") and lower.endswith((".yml", ".yaml")):
        return 95, "ci"
    if name in PRIORITY_ENTRY_NAMES:
        return 92, "entry"
    if any(marker in lower for marker in TEST_DIR_MARKERS) and _is_source_file(path):
        return 78, "test"
    if any(lower.startswith(prefix) for prefix in SOURCE_DIR_PREFIXES) and _is_source_file(path):
        depth = lower.count("/")
        return max(70, 88 - depth * 4), "source"
    if _is_source_file(path):
        return 60, "source"
    if lower.endswith(".md") and name.lower() in {
        "architecture.md",
        "design.md",
        "contributing.md",
    }:
        return 55, "docs"
    return 0, "skip"


def _is_source_file(path: str) -> bool:
    lower = path.lower()
    return any(lower.endswith(ext) for ext in SOURCE_EXTENSIONS)
