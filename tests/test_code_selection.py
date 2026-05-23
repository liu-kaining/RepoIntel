from __future__ import annotations

from repointel.code_selection import TreeEntry, select_paths_for_audit


def test_select_paths_prioritizes_manifests_and_src() -> None:
    entries = [
        TreeEntry("node_modules/foo/index.js", 1000),
        TreeEntry("package.json", 400),
        TreeEntry("src/core/engine.rs", 2200),
        TreeEntry("src/main.rs", 800),
        TreeEntry(".github/workflows/ci.yml", 300),
        TreeEntry("README.md", 5000),
    ]
    selected = select_paths_for_audit(entries, max_files=10, max_file_bytes=50_000)
    paths = [item.path for item in selected]
    assert "package.json" in paths
    assert "src/core/engine.rs" in paths
    assert all("node_modules" not in path for path in paths)
