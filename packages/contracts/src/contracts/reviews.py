"""Review result contracts."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ReviewComment(BaseModel):
    file_path: str
    line: int | None = None
    severity: str = "info"  # info | warning | error
    message: str


class ReviewResult(BaseModel):
    task_id: str
    approved: bool
    comments: list[ReviewComment] = Field(default_factory=list)
    requires_revision: bool = False
    schema_version: int = Field(default=1, ge=1)
