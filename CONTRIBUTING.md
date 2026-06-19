# Contributing to tiered-swe-agents

## Getting Started

```bash
# 1. Clone and enter the repository
git clone https://github.com/dhar174/local_swe_harness.git
cd local_swe_harness

# 2. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install workspace dependencies
uv sync --all-packages --all-extras

# 4. Install pre-commit hooks
make pre-commit-install

# 5. Copy environment template
cp .env.example .env  # edit as needed
```

## Development Workflow

1. Create a feature branch: `git checkout -b feat/my-change`
2. Make changes following the conventions in `AGENTS.md`
3. Run `make ci` to verify locally
4. Open a pull request using the provided template

## Architecture Rules

See `AGENTS.md` for the full list of architecture constraints, model assignment
rules, safety requirements, and coding conventions.

## Running Tests

```bash
make test-unit     # fast unit tests
make test-graph    # graph routing tests (fake models)
make coverage      # coverage report
make evals         # evaluation harness (fake models)
```

## Code Style

- Ruff for linting and formatting
- Strict Mypy for type checking
- All public functions must have full type annotations
