"""Patch correctness scorer stub."""
from __future__ import annotations


def score_patch(predicted_patch: str, expected_patch: str) -> float:
    """Return similarity score in [0, 1] between two patches. Stub."""
    if predicted_patch.strip() == expected_patch.strip():
        return 1.0
    return 0.0
