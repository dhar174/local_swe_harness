"""Command allowlist enforcement.

Only commands that appear in the configured allowlist may be executed by the
sandbox worker. All others are denied with a SecurityError.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class CommandPolicy:
    """Enforce the command allowlist loaded from config/security.yaml."""

    def __init__(self, allowed_prefixes: list[str]) -> None:
        self._allowed = [tuple(p.split()) for p in allowed_prefixes]

    @classmethod
    def from_yaml(cls, path: str | Path) -> "CommandPolicy":
        data: dict[str, Any] = yaml.safe_load(Path(path).read_text())
        return cls(data.get("allowed_commands", []))

    def is_allowed(self, command: list[str]) -> bool:
        for prefix in self._allowed:
            if tuple(command[: len(prefix)]) == prefix:
                return True
        return False

    def assert_allowed(self, command: list[str]) -> None:
        if not self.is_allowed(command):
            raise PermissionError(f"Command not in allowlist: {command!r}")
