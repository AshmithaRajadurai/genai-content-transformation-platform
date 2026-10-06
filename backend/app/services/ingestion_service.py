"""Compatibility re-export layer for ingestion service."""
from backend.app.modules.ingestion.service import (
    IngestionService,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_BYTES,
)

__all__ = ["IngestionService", "ALLOWED_EXTENSIONS", "MAX_FILE_SIZE_BYTES"]
