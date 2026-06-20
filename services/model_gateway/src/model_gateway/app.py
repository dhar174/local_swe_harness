"""FastAPI app for the model gateway service."""
from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="local_swe_harness model gateway")


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
