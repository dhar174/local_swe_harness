"""Routing policy definitions loaded from configuration."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class RoutingPolicy:
    tier1_complexity_ceiling: float = 0.5
    tier2_complexity_ceiling: float = 0.85
    max_retries_per_tier: int = 3
    escalation_on_test_failure: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "RoutingPolicy":
        data: dict[str, Any] = yaml.safe_load(Path(path).read_text())
        policy_data = data.get("policy", {})
        return cls(**{k: v for k, v in policy_data.items() if k in cls.__dataclass_fields__})
