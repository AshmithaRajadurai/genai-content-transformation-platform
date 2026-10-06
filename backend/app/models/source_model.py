"""Compatibility re-export layer for source ingestion models."""
from backend.app.modules.ingestion.schemas import SourceTextInput, IngestionResponse

__all__ = ["SourceTextInput", "IngestionResponse"]
