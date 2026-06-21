#!/usr/bin/env bash
# Bootstrap the development environment.
set -euo pipefail

echo "[bootstrap] Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "[bootstrap] Syncing workspace dependencies..."
uv sync --all-packages --all-extras

echo "[bootstrap] Installing pre-commit hooks..."
uv run pre-commit install

echo "[bootstrap] Copying .env.example → .env (if not present)..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "[bootstrap] Edit .env with your credentials."
fi

echo "[bootstrap] Done! Run 'make ci' to verify your setup."
