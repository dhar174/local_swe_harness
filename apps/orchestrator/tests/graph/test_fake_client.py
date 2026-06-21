"""Graph tests using fake model clients – no real LLMs required."""
from __future__ import annotations

import asyncio

import pytest

from model_clients.fake import FakeModelClient
from model_clients.errors import ModelNotAvailableError


pytestmark = pytest.mark.graph


@pytest.fixture
def client() -> FakeModelClient:
    return FakeModelClient(responses=["step1", "step2"])


def test_fake_client_returns_queued_responses(client: FakeModelClient) -> None:
    async def run() -> None:
        resp = await client.complete("fake-model", [{"role": "user", "content": "hi"}])
        assert resp["choices"][0]["message"]["content"] == "step1"
        resp2 = await client.complete("fake-model", [{"role": "user", "content": "next"}])
        assert resp2["choices"][0]["message"]["content"] == "step2"

    asyncio.run(run())


def test_fake_client_default_response() -> None:
    client = FakeModelClient()

    async def run() -> str:
        resp = await client.complete("fake", [])
        return resp["choices"][0]["message"]["content"]  # type: ignore[no-any-return]

    result = asyncio.run(run())
    assert result == "fake response"


def test_fake_client_raise_on_call() -> None:
    client = FakeModelClient(raise_on_call=ModelNotAvailableError("fake"))

    async def run() -> None:
        await client.complete("fake", [])

    with pytest.raises(ModelNotAvailableError):
        asyncio.run(run())


def test_fake_client_call_count() -> None:
    client = FakeModelClient(responses=["a", "b", "c"])

    async def run() -> None:
        for _ in range(3):
            await client.complete("fake", [])

    asyncio.run(run())
    assert client.call_count == 3


def test_fake_client_reset() -> None:
    client = FakeModelClient(responses=["x"])

    async def run() -> None:
        await client.complete("fake", [])

    asyncio.run(run())
    client.reset()
    assert client.call_count == 0
    assert len(client.call_log) == 0
