"""Tool efficiency scorer stub."""
from __future__ import annotations


def score_tool_efficiency(tool_calls: int, optimal_calls: int) -> float:
    """Return efficiency ratio. Stub."""
    if optimal_calls == 0:
        return 1.0
    return min(1.0, optimal_calls / max(tool_calls, 1))
