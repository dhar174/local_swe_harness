# ADR 0001: Tiered Model Routing

## Status: Accepted

## Context

SWE tasks vary widely in complexity. Using cloud models for every task is
expensive and slow. Pure local models may fail on complex tasks.

## Decision

Implement a three-tier routing strategy:
1. Fast local models for simple tasks (≤ 0.50 complexity)
2. Heavy local models for complex tasks (≤ 0.85 complexity)
3. Cloud models for high-risk or repeatedly failing tasks

## Consequences

- Cost savings: most tasks resolved locally
- Latency savings: no network round-trip for tier 1/2
- Complexity: requires a routing/scoring subsystem and escalation logic
