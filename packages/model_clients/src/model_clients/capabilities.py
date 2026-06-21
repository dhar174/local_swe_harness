"""Typed model capability registry.

Model assignments are configuration-driven. They must NOT be hardcoded in
graph nodes. Load :class:`ModelRegistry` from ``config/models.yaml`` instead.
"""
from __future__ import annotations

import enum
from typing import Any

from pydantic import BaseModel, Field


class ModelTier(str, enum.Enum):
    TIER1_FAST = "tier1_fast"
    TIER2_HEAVY = "tier2_heavy"
    TIER3_CLOUD = "tier3_cloud"


class ModelRole(str, enum.Enum):
    """Logical agent roles that consume models."""

    ROUTER = "router"
    NAVIGATOR = "navigator"
    CODER = "coder"
    ARCHITECT = "architect"
    REVIEWER = "reviewer"
    CRITIC = "critic"
    CLOUD_ENGINEER = "cloud_engineer"


class ModelCapability(str, enum.Enum):
    """Feature flags that a model may support."""

    CHAT = "chat"
    FUNCTION_CALLING = "function_calling"
    CODE_COMPLETION = "code_completion"
    LONG_CONTEXT = "long_context"       # >32k tokens
    STRUCTURED_OUTPUT = "structured_output"


class ModelSpec(BaseModel):
    """Complete specification for a single model entry in the registry."""

    name: str
    tier: ModelTier
    roles: list[ModelRole]
    capabilities: list[ModelCapability]
    context_window: int = Field(default=8192, ge=512)
    max_output_tokens: int = Field(default=4096, ge=64)
    backend: str = "llamacpp"           # llamacpp | lmstudio | ollama | cloud
    endpoint: str | None = None         # override gateway default
    cost_per_1k_input: float = 0.0      # USD; 0 for local models
    cost_per_1k_output: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)
    schema_version: int = Field(default=1, ge=1)
