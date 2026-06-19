"""Application settings loaded from environment variables."""
from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "extra": "ignore"}

    app_env: str = "local"
    log_level: str = "INFO"
    model_gateway_url: str = "http://model-gateway:8001"
    sandbox_worker_url: str = "http://sandbox-worker:8002"
    database_url: str = "******postgres:5432/swe_agents"

    # Config file paths
    models_config: str = "config/models.yaml"
    routing_config: str = "config/routing.yaml"


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
