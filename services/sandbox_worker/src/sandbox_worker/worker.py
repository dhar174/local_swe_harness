"""FastAPI app for the sandbox worker service."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException

app = FastAPI(title="local_swe_harness sandbox worker")


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/execute", tags=["sandbox"])
async def execute() -> None:
    raise HTTPException(status_code=501, detail="Sandbox execution not implemented yet")
