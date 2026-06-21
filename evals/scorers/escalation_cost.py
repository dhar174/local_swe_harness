"""Cloud escalation cost scorer stub."""
from __future__ import annotations


def score_escalation_rate(escalated: int, total: int) -> float:
    """Return fraction of tasks that were escalated to cloud. Lower is better."""
    return escalated / total if total else 0.0
