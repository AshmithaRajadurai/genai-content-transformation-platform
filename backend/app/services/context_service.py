"""Compatibility re-export layer for context service."""
from backend.app.modules.context.service import (
    ContextService,
    CHANNEL_DEFINITIONS,
)

__all__ = ["ContextService", "CHANNEL_DEFINITIONS"]
