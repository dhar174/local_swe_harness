FROM python:3.14-slim

# Drop all capabilities; only allow execution within /tmp/worktrees
RUN useradd --create-home --shell /bin/bash sandbox

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
COPY services/sandbox_worker/pyproject.toml services/sandbox_worker/
COPY packages/ packages/
COPY services/sandbox_worker/src/ services/sandbox_worker/src/

RUN uv sync --no-dev
USER sandbox

CMD ["uv", "run", "uvicorn", "sandbox_worker.worker:app", "--host", "0.0.0.0", "--port", "8002"]
