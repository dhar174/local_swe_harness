"""In-memory model registry loaded from configuration.

Usage::

    registry = ModelRegistry.from_yaml("config/models.yaml")
    spec = registry.get_for_role(ModelRole.CODER, tier=ModelTier.TIER1_FAST)
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from model_clients.capabilities import ModelRole, ModelSpec, ModelTier


class ModelRegistry:
    """Configuration-driven registry of available model specs."""

    def __init__(self, specs: list[ModelSpec]) -> None:
        self._specs = specs

    # ── Factory ───────────────────────────────────────────────────────────

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ModelRegistry":
        data: dict[str, Any] = yaml.safe_load(Path(path).read_text())
        specs = [ModelSpec.model_validate(m) for m in data.get("models", [])]
        return cls(specs)

    # ── Queries ───────────────────────────────────────────────────────────

    def get_for_role(
        self,
        role: ModelRole,
        tier: ModelTier | None = None,
    ) -> ModelSpec:
        """Return the first model spec matching *role* (and optionally *tier*).

        Raises :class:`KeyError` if no model is configured for the combination.
        """
        for spec in self._specs:
            if role in spec.roles:
                if tier is None or spec.tier == tier:
                    return spec
        raise KeyError(f"No model configured for role={role!r} tier={tier!r}")

    def all_specs(self) -> list[ModelSpec]:
        return list(self._specs)
