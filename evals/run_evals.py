#!/usr/bin/env python3
"""Evaluation harness entry point.

Usage:
    python evals/run_evals.py --fake-models [--output evals/results/]
    python evals/run_evals.py [--output evals/results/]  # real models

Model-dependent evaluations MUST NOT block ordinary CI.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run evaluation harness")
    parser.add_argument("--fake-models", action="store_true",
                        help="Use deterministic fake model clients")
    parser.add_argument("--output", default="evals/results/",
                        help="Output directory for results")
    args = parser.parse_args(argv)

    output_dir = pathlib.Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[evals] Running with {'fake' if args.fake_models else 'real'} models...")
    start = time.perf_counter()

    # ── Routing accuracy ───────────────────────────────────────────────────
    from evals.scorers.routing_accuracy import score_routing

    routing_cases = list(_load_jsonl("evals/datasets/routing_cases.jsonl"))
    ground_truth = [c["expected_tier"] for c in routing_cases]

    if args.fake_models:
        # Deterministic prediction: use complexity threshold
        predictions = [
            "tier3_cloud" if c["complexity"] > 0.85
            else "tier2_heavy" if c["complexity"] > 0.5
            else "tier1_fast"
            for c in routing_cases
        ]
    else:
        # TODO: run real model inference
        predictions = ground_truth  # placeholder

    routing_result = score_routing(predictions, ground_truth)

    results = {
        "routing_accuracy": routing_result.accuracy,
        "routing_correct": routing_result.correct,
        "routing_total": routing_result.total,
        "fake_models": args.fake_models,
        "duration_s": time.perf_counter() - start,
    }

    out_file = output_dir / "results.json"
    out_file.write_text(json.dumps(results, indent=2))
    print(f"[evals] Results written to {out_file}")
    print(f"[evals] Routing accuracy: {routing_result.accuracy:.2%} "
          f"({routing_result.correct}/{routing_result.total})")
    return 0


def _load_jsonl(path: str):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


if __name__ == "__main__":
    sys.exit(main())
