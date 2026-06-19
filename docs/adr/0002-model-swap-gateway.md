# ADR 0002: Model Swap via Configuration Gateway

## Status: Accepted

## Context

Model names must not be hardcoded in agent code. The best model for a role
changes frequently as new models are released.

## Decision

All model assignments go through `ModelRegistry` loaded from `config/models.yaml`.
Graph nodes receive a model name from the registry, not from hardcoded strings.
The `model_gateway` service provides a unified HTTP API over all backends.

## Consequences

- Model swaps require only a YAML config change, not a code change
- Adds a gateway service that must be kept healthy
