"""Repository management client interface."""
from __future__ import annotations

import subprocess
from pathlib import Path


class RepositoryClient:
    """Thin wrapper around git operations for a local repository."""

    def __init__(self, repo_path: str | Path) -> None:
        self.repo_path = Path(repo_path)

    def _run(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def current_branch(self) -> str:
        return self._run("rev-parse", "--abbrev-ref", "HEAD")

    def file_content(self, path: str) -> str:
        return (self.repo_path / path).read_text()

def apply_patch(self, patch: str) -> None:
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".patch", delete=False, mode="w") as f:
        f.write(patch)
        f.flush()
        patch_path = f.name

    try:
        self._run("apply", patch_path)
    finally:
        os.unlink(patch_path)
