"""Model client interfaces, capability registry, and fake clients."""

from model_clients.capabilities import ModelCapability, ModelRole, ModelSpec, ModelTier
from model_clients.errors import ModelClientError, ModelNotAvailableError
from model_clients.fake import FakeModelClient
from model_clients.gateway import GatewayModelClient
from model_clients.registry import ModelRegistry

__all__ = [
    "FakeModelClient",
    "GatewayModelClient",
    "ModelCapability",
    "ModelClientError",
    "ModelNotAvailableError",
    "ModelRegistry",
    "ModelRole",
    "ModelSpec",
    "ModelTier",
]
