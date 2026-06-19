.DEFAULT_GOAL := help
PYTHON        := python3
UV            := uv
PYTEST_ARGS   ?= -x

.PHONY: help install sync lint fmt typecheck test test-unit test-graph test-integration \
        coverage build clean docker-up docker-down pre-commit-install pre-commit-run \
        evals docs

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'

# ── Setup ─────────────────────────────────────────────────────────────────────

install: ## Install all workspace dependencies with uv
	$(UV) sync --all-packages --all-extras

sync: ## Sync workspace (fast, no extras)
	$(UV) sync --all-packages

pre-commit-install: ## Install pre-commit hooks
	$(UV) run pre-commit install

# ── Quality ───────────────────────────────────────────────────────────────────

lint: ## Run Ruff linter
	$(UV) run ruff check .

fmt: ## Run Ruff formatter
	$(UV) run ruff format .

fmt-check: ## Check formatting without writing (CI mode)
	$(UV) run ruff format --check .

typecheck: ## Run strict Mypy
	$(UV) run mypy .

pre-commit-run: ## Run all pre-commit hooks
	$(UV) run pre-commit run --all-files

# ── Tests ─────────────────────────────────────────────────────────────────────

test: ## Run all non-LLM tests
	$(UV) run pytest $(PYTEST_ARGS) -m "not llm and not integration"

test-unit: ## Run unit tests only
	$(UV) run pytest $(PYTEST_ARGS) -m unit

test-graph: ## Run graph routing tests
	$(UV) run pytest $(PYTEST_ARGS) -m graph

test-integration: ## Run integration tests (requires services)
	$(UV) run pytest $(PYTEST_ARGS) -m integration

test-e2e: ## Run end-to-end tests (requires full stack)
	$(UV) run pytest $(PYTEST_ARGS) -m e2e

coverage: ## Run tests with coverage report
	$(UV) run pytest --cov --cov-report=html --cov-report=term-missing \
		-m "not llm and not integration"

# ── Evaluations ───────────────────────────────────────────────────────────────

evals: ## Run evaluation harness (fake models only)
	$(UV) run python evals/run_evals.py --fake-models

# ── Build ─────────────────────────────────────────────────────────────────────

build: ## Build all workspace packages
	$(UV) build --all-packages

# ── Docker ────────────────────────────────────────────────────────────────────

docker-up: ## Start development stack
	docker compose up -d

docker-down: ## Stop development stack
	docker compose down

docker-logs: ## Tail all service logs
	docker compose logs -f

docker-build: ## Build all service images
	docker compose build

# ── Docs ──────────────────────────────────────────────────────────────────────

docs: ## Build documentation
	$(UV) run mkdocs build

docs-serve: ## Serve docs locally
	$(UV) run mkdocs serve

# ── Utilities ─────────────────────────────────────────────────────────────────

clean: ## Remove build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null; true
	rm -rf htmlcov .coverage coverage.xml dist build

ci: fmt-check lint typecheck test coverage ## Run full CI quality suite locally
