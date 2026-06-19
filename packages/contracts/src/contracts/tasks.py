"""Task request and task data contracts."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    """Incoming task request from an external caller."""

    repository_url: str
    issue_number: int | None = None
    title: str
    description: str
    base_branch: str = "main"
    labels: list[str] = Field(default_factory=list)
    priority: int = Field(default=5, ge=1, le=10)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Task(BaseModel):
    """Resolved task with internal identifiers."""

    task_id: str
    request: TaskRequest
    repository_path: str | None = None
    worktree_path: str | None = None
    schema_version: int = Field(default=1, ge=1)
