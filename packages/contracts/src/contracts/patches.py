"""Patch and diff contracts."""
from __future__ import annotations

from pydantic import BaseModel, Field


class FilePatch(BaseModel):
    """A unified diff for a single file."""

    file_path: str
    diff: str
    is_new_file: bool = False
    is_deleted: bool = False


class PatchSet(BaseModel):
    """Collection of file patches produced by the coder agent."""

    task_id: str
    patches: list[FilePatch]
    schema_version: int = Field(default=1, ge=1)
