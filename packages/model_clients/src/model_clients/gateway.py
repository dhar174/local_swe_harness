"""HTTP client that talks to the model gateway service."""
from __future__ import annotations

from typing import Any

import httpx

from model_clients.errors import ModelClientError, ModelNotAvailableError


class GatewayModelClient:
    """Thin async HTTP client for the model gateway."""

    def __init__(self, base_url: str, timeout: float = 120.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def complete(
        self,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                resp = await client.post(
                    f"{self._base_url}/v1/chat/completions",
                    json={"model": model, "messages": messages, **kwargs},
                )
                resp.raise_for_status()
                return resp.json()  # type: ignore[no-any-return]
            except httpx.ConnectError as exc:
                raise ModelNotAvailableError(model) from exc
            except httpx.HTTPStatusError as exc:
                raise ModelClientError(str(exc)) from exc
