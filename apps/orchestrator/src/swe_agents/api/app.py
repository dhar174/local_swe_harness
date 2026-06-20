"""FastAPI app for the orchestrator service."""
from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="local_swe_harness orchestrator")


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
