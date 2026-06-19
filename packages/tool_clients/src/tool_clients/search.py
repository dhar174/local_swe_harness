"""Code search client interface."""
from __future__ import annotations

from pydantic import BaseModel


class SearchResult(BaseModel):
    file_path: str
    line: int
    snippet: str
    score: float = 1.0


class SearchClient:
    """Client for querying the repository indexer search API."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    async def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        import httpx

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base_url}/search",
                json={"query": query, "top_k": top_k},
            )
            resp.raise_for_status()
            return [SearchResult.model_validate(r) for r in resp.json()["results"]]
