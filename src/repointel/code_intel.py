"""Gather real source code from repositories for deep audit."""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .code_selection import TreeEntry, select_paths_for_audit
from .config import Settings
from .exceptions import ExternalServiceError
from .github_client import GitHubClient
from .models import RepoCandidate, RepoCodeBundle, SourceFile

LOGGER = logging.getLogger(__name__)

TEXT_DECODE_ERRORS = "replace"


@dataclass(frozen=True)
class CodeIntelGatherer:
    settings: Settings
    github: GitHubClient

    def gather(self, repo: RepoCandidate) -> RepoCodeBundle:
        if self.settings.dry_run:
            return self._dry_run_bundle(repo)

        mode = self.settings.code_source
        if mode in {"auto", "git"}:
            try:
                bundle = self._gather_via_git(repo)
                LOGGER.info(
                    "Code intel via git for %s: %d files, %d chars",
                    repo.full_name,
                    len(bundle.files),
                    bundle.total_chars,
                )
                return bundle
            except Exception as exc:
                if mode == "git":
                    raise ExternalServiceError(f"Git code gather failed for {repo.full_name}: {exc}") from exc
                LOGGER.warning("Git gather failed for %s, falling back to API: %s", repo.full_name, exc)

        bundle = self._gather_via_api(repo)
        LOGGER.info(
            "Code intel via API for %s: %d files, %d chars",
            repo.full_name,
            len(bundle.files),
            bundle.total_chars,
        )
        return bundle

    def _gather_via_git(self, repo: RepoCandidate) -> RepoCodeBundle:
        tmp_dir = Path(tempfile.mkdtemp(prefix="repointel-clone-"))
        try:
            clone_url = f"https://github.com/{repo.full_name}.git"
            cmd = [
                "git",
                "clone",
                "--depth",
                "1",
                "--single-branch",
                "--branch",
                repo.default_branch,
                clone_url,
                str(tmp_dir / "repo"),
            ]
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                timeout=self.settings.git_clone_timeout_seconds,
            )
            repo_root = tmp_dir / "repo"
            entries = self._walk_local_tree(repo_root)
            return self._build_bundle(
                repo,
                entries,
                source="git",
                root_note=f"shallow clone branch={repo.default_branch}",
                reader=lambda path: self._read_local_file(repo_root / path),
            )
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def _gather_via_api(self, repo: RepoCandidate) -> RepoCodeBundle:
        entries = self._fetch_tree_via_api(repo)
        return self._build_bundle(
            repo,
            entries,
            source="api",
            root_note="GitHub Trees/Contents API",
            reader=lambda path: self.github.fetch_repository_file(repo, path),
        )

    def _build_bundle(
        self,
        repo: RepoCandidate,
        entries: list[TreeEntry],
        *,
        source: str,
        root_note: str,
        reader,
    ) -> RepoCodeBundle:
        selected = select_paths_for_audit(
            entries,
            max_files=self.settings.max_code_files,
            max_file_bytes=self.settings.max_file_bytes,
        )
        files: list[SourceFile] = []
        total_chars = 0
        skipped: list[str] = []

        for item in selected:
            if total_chars >= self.settings.max_total_code_chars:
                skipped.append(f"budget:{item.path}")
                continue
            try:
                raw = reader(item.path)
            except Exception as exc:
                skipped.append(f"read_error:{item.path}:{exc}")
                continue
            if not raw.strip():
                skipped.append(f"empty:{item.path}")
                continue

            remaining = self.settings.max_total_code_chars - total_chars
            per_file_cap = min(self.settings.max_file_bytes, remaining)
            truncated = len(raw) > per_file_cap
            content = raw[:per_file_cap]
            if truncated:
                content += (
                    f"\n\n/* RepoIntel: truncated at {per_file_cap} bytes; "
                    f"original size {len(raw)} bytes */\n"
                )

            files.append(
                SourceFile(
                    path=item.path,
                    content=content,
                    size_bytes=item.size,
                    category=item.category,
                    truncated=truncated,
                )
            )
            total_chars += len(content)

        return RepoCodeBundle(
            repo_name=repo.full_name,
            source=source,
            default_branch=repo.default_branch,
            tree_file_count=len(entries),
            selected_paths=tuple(item.path for item in selected),
            files=tuple(files),
            skipped=skipped,
            gather_note=root_note,
        )

    def _walk_local_tree(self, root: Path) -> list[TreeEntry]:
        entries: list[TreeEntry] = []
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            try:
                size = path.stat().st_size
            except OSError:
                continue
            entries.append(TreeEntry(path=rel, size=size))
        return entries

    @staticmethod
    def _read_local_file(path: Path) -> str:
        data = path.read_bytes()
        if b"\x00" in data[:1024]:
            raise ValueError("binary file")
        return data.decode("utf-8", errors=TEXT_DECODE_ERRORS)

    def _fetch_tree_via_api(self, repo: RepoCandidate) -> list[TreeEntry]:
        return self.github.fetch_repository_tree_entries(repo)

    def _dry_run_bundle(self, repo: RepoCandidate) -> RepoCodeBundle:
        sample_code = '''pub mod agent;

pub struct AgentRuntime {
    sandbox: Sandbox,
    tools: ToolRegistry,
}

impl AgentRuntime {
    /// Execute a tool call inside the sandbox with policy checks.
    pub fn execute(&mut self, call: ToolCall) -> Result<ToolOutput, RuntimeError> {
        self.sandbox.verify(&call)?;
        let handler = self.tools.resolve(call.name())?;
        handler.invoke(call)
    }
}
'''
        files = (
            SourceFile(
                path="src/agent/runtime.rs",
                content=sample_code,
                size_bytes=len(sample_code),
                category="source",
                truncated=False,
            ),
            SourceFile(
                path="Cargo.toml",
                content='[package]\nname = "flux-agent"\nversion = "0.3.1"\n',
                size_bytes=40,
                category="manifest",
                truncated=False,
            ),
            SourceFile(
                path=".github/workflows/ci.yml",
                content="name: ci\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n",
                size_bytes=60,
                category="ci",
                truncated=False,
            ),
        )
        return RepoCodeBundle(
            repo_name=repo.full_name,
            source="dry-run",
            default_branch=repo.default_branch,
            tree_file_count=120,
            selected_paths=tuple(f.path for f in files),
            files=files,
            skipped=[],
            gather_note="synthetic code bundle for dry-run",
        )
