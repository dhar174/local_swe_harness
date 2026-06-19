"""Path allowlist enforcement."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class PathPolicy:
    """Ensure file access stays within allowed directory subtrees."""

    def __init__(self, allowed_roots: list[str]) -> None:
        self._roots = [Path(r).resolve() for r in allowed_roots]

    @classmethod
    def from_yaml(cls, path: str | Path) -> "PathPolicy":
        data: dict[str, Any] = yaml.safe_load(Path(path).read_text())
        return cls(data.get("allowed_paths", []))

    def is_allowed(self, target: str | Path) -> bool:
        resolved = Path(target).resolve()
        return any(resolved.is_relative_to(root) for root in self._roots)

    def assert_allowed(self, target: str | Path) -> None:
        if not self.is_allowed(target):
            raise PermissionError(f"Path not in allowlist: {target!r}")
