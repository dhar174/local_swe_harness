"""Routing accuracy scorer."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RoutingAccuracyResult:
    correct: int
    total: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0


def score_routing(
    predictions: list[str],
    ground_truth: list[str],
) -> RoutingAccuracyResult:
    correct = sum(p == g for p, g in zip(predictions, ground_truth))
    return RoutingAccuracyResult(correct=correct, total=len(ground_truth))
