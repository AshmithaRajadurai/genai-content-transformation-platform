import logging
import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from backend.app.database.connection import db, check_connection
from backend.app.modules.history.schemas import (
    TransformationRecord,
    HistoryItemSummary,
    HistoryListResponse,
    StorageHealthResponse,
)

logger = logging.getLogger("history_service")


class HistoryService:
    """
    MongoDB Storage & History Layer:
    Persists transformed multi-channel intelligence artefacts, NLP metadata,
    and execution metrics to MongoDB Atlas with resilient in-memory session fallback.
    """

    _in_memory_records: List[Dict[str, Any]] = []
    _mongo_online: Optional[bool] = None
    _last_online_check: float = 0.0
    _CHECK_INTERVAL_SEC: float = 15.0
    COLLECTION_NAME = "transformations"

    @classmethod
    def _is_atlas_reachable(cls) -> bool:
        """Checks if MongoDB Atlas is reachable with circuit-breaker caching."""
        now = time.time()
        if cls._mongo_online is False and (now - cls._last_online_check) < cls._CHECK_INTERVAL_SEC:
            return False

        res = check_connection()
        cls._last_online_check = now
        cls._mongo_online = (res.get("status") == "connected")
        return cls._mongo_online

    @classmethod
    def _get_collection(cls):
        return db[cls.COLLECTION_NAME]

    @classmethod
    def save_transformation(cls, record: TransformationRecord) -> TransformationRecord:
        """
        Persists a transformation record to MongoDB Atlas.
        Falls back to in-memory session buffer if Atlas connection is unavailable.
        """
        doc = record.model_dump()

        # Always keep in in-memory session buffer (capped at 100)
        cls._in_memory_records.insert(0, dict(doc))
        if len(cls._in_memory_records) > 100:
            cls._in_memory_records = cls._in_memory_records[:100]

        if cls._is_atlas_reachable():
            try:
                collection = cls._get_collection()
                mongo_doc = dict(doc)
                collection.replace_one(
                    {"transformation_id": record.transformation_id},
                    mongo_doc,
                    upsert=True
                )
                logger.info("Successfully persisted transformation %s to MongoDB", record.transformation_id)
            except Exception as exc:
                cls._mongo_online = False
                logger.warning(
                    "MongoDB write unavailable (%s). Cached transformation %s in memory session.",
                    str(exc),
                    record.transformation_id
                )

        return record

    @classmethod
    def list_history(cls, limit: int = 20, skip: int = 0) -> HistoryListResponse:
        """
        Retrieves recent transformation summaries from MongoDB or fallback cache.
        """
        if cls._is_atlas_reachable():
            try:
                collection = cls._get_collection()
                total = collection.count_documents({})
                cursor = collection.find(
                    {},
                    {
                        "_id": 0,
                        "transformation_id": 1,
                        "source_title": 1,
                        "detected_topic": 1,
                        "selected_channels": 1,
                        "created_at": 1,
                        "total_tokens": 1
                    }
                ).sort("created_at", -1).skip(skip).limit(limit)

                items: List[HistoryItemSummary] = []
                for doc in cursor:
                    items.append(HistoryItemSummary(
                        transformation_id=doc.get("transformation_id", ""),
                        source_title=doc.get("source_title", "Untitled Document"),
                        detected_topic=doc.get("detected_topic", "General"),
                        channels=doc.get("selected_channels", []),
                        created_at=doc.get("created_at", datetime.now(timezone.utc).isoformat()),
                        total_tokens=doc.get("total_tokens", 0)
                    ))

                return HistoryListResponse(
                    total=total,
                    database_status="connected",
                    items=items
                )
            except Exception as exc:
                cls._mongo_online = False
                logger.warning("MongoDB read unavailable (%s). Falling back to session buffer.", str(exc))

        # Fallback to in-memory buffer
        paged = cls._in_memory_records[skip:skip + limit]
        items = [
            HistoryItemSummary(
                transformation_id=doc.get("transformation_id", ""),
                source_title=doc.get("source_title", "Untitled Document"),
                detected_topic=doc.get("detected_topic", "General"),
                channels=doc.get("selected_channels", []),
                created_at=doc.get("created_at", datetime.now(timezone.utc).isoformat()),
                total_tokens=doc.get("total_tokens", 0)
            )
            for doc in paged
        ]
        return HistoryListResponse(
            total=len(cls._in_memory_records),
            database_status="offline_fallback",
            items=items
        )

    @classmethod
    def get_transformation(cls, transformation_id: str) -> Optional[TransformationRecord]:
        """
        Fetches full transformation record by UUID from MongoDB or fallback buffer.
        """
        if cls._is_atlas_reachable():
            try:
                collection = cls._get_collection()
                doc = collection.find_one({"transformation_id": transformation_id}, {"_id": 0})
                if doc:
                    return TransformationRecord(**doc)
            except Exception as exc:
                cls._mongo_online = False
                logger.warning("MongoDB fetch error (%s). Checking session buffer.", str(exc))

        # Check in-memory fallback
        for item in cls._in_memory_records:
            if item.get("transformation_id") == transformation_id:
                clean_item = {k: v for k, v in item.items() if k != "_id"}
                return TransformationRecord(**clean_item)

        return None

    @classmethod
    def delete_transformation(cls, transformation_id: str) -> bool:
        """
        Deletes a transformation from MongoDB and in-memory cache.
        """
        deleted_from_memory = any(
            item.get("transformation_id") == transformation_id
            for item in cls._in_memory_records
        )
        cls._in_memory_records = [
            item for item in cls._in_memory_records
            if item.get("transformation_id") != transformation_id
        ]

        if cls._is_atlas_reachable():
            try:
                collection = cls._get_collection()
                res = collection.delete_one({"transformation_id": transformation_id})
                return res.deleted_count > 0 or deleted_from_memory
            except Exception as exc:
                cls._mongo_online = False
                logger.warning("MongoDB delete failed (%s). Removed from memory session.", str(exc))

        return deleted_from_memory

    @classmethod
    def get_health(cls) -> StorageHealthResponse:
        """
        Checks connection status to MongoDB and counts stored transformations.
        """
        conn = check_connection()
        record_count = 0
        if conn.get("status") == "connected":
            try:
                record_count = cls._get_collection().count_documents({})
            except Exception:
                record_count = len(cls._in_memory_records)
        else:
            record_count = len(cls._in_memory_records)

        return StorageHealthResponse(
            status=conn.get("status", "disconnected"),
            database=conn.get("database", "genai_content_platform"),
            type=conn.get("type", "atlas_cloud"),
            record_count=record_count,
            error=conn.get("error")
        )

    @classmethod
    def clear_memory_buffer(cls):
        """Helper for test cleanup."""
        cls._in_memory_records = []
        cls._mongo_online = None
        cls._last_online_check = 0.0
