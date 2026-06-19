"""Sandbox execution client interface."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ExecResult(BaseModel):
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False


class SandboxClient:
    """HTTP client for the sandbox worker service."""

    def __init__(self, base_url: str, timeout: float = 60.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def execute(
        self,
        command: list[str],
        *,
        working_dir: str | None = None,
        env: dict[str, str] | None = None,
    ) -> ExecResult:
        import httpx

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(
                f"{self._base_url}/execute",
                json={"command": command, "working_dir": working_dir, "env": env or {}},
            )
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()
            return ExecResult.model_validate(data)
