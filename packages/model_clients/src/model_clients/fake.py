"""Deterministic fake model client for unit and graph tests.

All responses are configured at construction time so tests are
fully reproducible without any network calls or real LLMs.
"""
from __future__ import annotations

from collections import deque
from typing import Any


class FakeModelClient:
    """Fake model client that returns pre-configured responses.

    Examples::

        client = FakeModelClient(responses=["Hello!", "Done."])
        resp = await client.complete("fake-model", [{"role": "user", "content": "hi"}])
        assert resp["choices"][0]["message"]["content"] == "Hello!"
    """

    def __init__(
        self,
        responses: list[str] | None = None,
        *,
        default_response: str = "fake response",
        raise_on_call: Exception | None = None,
    ) -> None:
        self._queue: deque[str] = deque(responses or [])
        self._default = default_response
        self._raise = raise_on_call
        self.call_count = 0
        self.call_log: list[dict[str, Any]] = []

    async def complete(
        self,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        self.call_count += 1
        self.call_log.append({"model": model, "messages": messages, **kwargs})

        if self._raise is not None:
            raise self._raise

        content = self._queue.popleft() if self._queue else self._default
        return {
            "id": f"fake-{self.call_count}",
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": len(content.split()),
                "total_tokens": 10 + len(content.split()),
            },
        }

    def reset(self) -> None:
        """Reset call count and log for reuse across tests."""
        self.call_count = 0
        self.call_log.clear()
        self._queue.clear()
