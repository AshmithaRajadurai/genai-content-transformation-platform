"""Compatibility re-export layer for storage service."""
from backend.app.modules.history.service import HistoryService as StorageService

__all__ = ["StorageService"]
