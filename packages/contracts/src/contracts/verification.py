"""Verification result contracts."""
from __future__ import annotations

from pydantic import BaseModel, Field


class VerificationResult(BaseModel):
    task_id: str
    tests_passed: bool
    lint_passed: bool
    typecheck_passed: bool
    coverage_pct: float | None = None
    errors: list[str] = Field(default_factory=list)
    schema_version: int = Field(default=1, ge=1)
