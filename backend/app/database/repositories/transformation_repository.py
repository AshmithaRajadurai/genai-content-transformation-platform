import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from backend.app.database.connection import db, check_connection
from backend.app.modules.history.schemas import (
    TransformationRecord,
    HistoryItemSummary,
    HistoryListResponse,
    StorageHealthResponse,
)

logger = logging.getLogger("transformation_repository")


class TransformationRepository:
    """Repository handling persistence for Transformation records in MongoDB with session fallback."""

    COLLECTION_NAME = "transformations"
    _in_memory_records: List[Dict[str, Any]] = []

    @classmethod
    def get_collection(cls):
        return db[cls.COLLECTION_NAME]

    @classmethod
    def save(cls, record: TransformationRecord, is_online: bool) -> TransformationRecord:
        doc = record.model_dump()
        cls._in_memory_records.insert(0, dict(doc))
        if len(cls._in_memory_records) > 100:
            cls._in_memory_records = cls._in_memory_records[:100]

        if is_online:
            try:
                collection = cls.get_collection()
                mongo_doc = dict(doc)
                collection.replace_one(
                    {"transformation_id": record.transformation_id},
                    mongo_doc,
                    upsert=True
                )
                logger.info("Successfully persisted transformation %s to MongoDB", record.transformation_id)
            except Exception as exc:
                logger.warning(
                    "MongoDB write unavailable (%s). Cached transformation %s in memory session.",
                    str(exc),
                    record.transformation_id
                )
        return record

    @classmethod
    def list_history(cls, limit: int = 20, skip: int = 0, is_online: bool = True) -> HistoryListResponse:
        if is_online:
            try:
                collection = cls.get_collection()
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
                logger.warning("MongoDB read unavailable (%s). Falling back to session buffer.", str(exc))

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
    def get_by_id(cls, transformation_id: str, is_online: bool = True) -> Optional[TransformationRecord]:
        if is_online:
            try:
                collection = cls.get_collection()
                doc = collection.find_one({"transformation_id": transformation_id}, {"_id": 0})
                if doc:
                    return TransformationRecord(**doc)
            except Exception as exc:
                logger.warning("MongoDB fetch error (%s). Checking session buffer.", str(exc))

        for item in cls._in_memory_records:
            if item.get("transformation_id") == transformation_id:
                clean_item = {k: v for k, v in item.items() if k != "_id"}
                return TransformationRecord(**clean_item)

        return None

    @classmethod
    def delete(cls, transformation_id: str, is_online: bool = True) -> bool:
        deleted_from_memory = any(
            item.get("transformation_id") == transformation_id
            for item in cls._in_memory_records
        )
        cls._in_memory_records = [
            item for item in cls._in_memory_records
            if item.get("transformation_id") != transformation_id
        ]

        if is_online:
            try:
                collection = cls.get_collection()
                res = collection.delete_one({"transformation_id": transformation_id})
                return res.deleted_count > 0 or deleted_from_memory
            except Exception as exc:
                logger.warning("MongoDB delete failed (%s). Removed from memory session.", str(exc))

        return deleted_from_memory

    @classmethod
    def get_health(cls, is_online: bool = True) -> StorageHealthResponse:
        conn = check_connection()
        record_count = 0
        if conn.get("status") == "connected" and is_online:
            try:
                record_count = cls.get_collection().count_documents({})
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
    def clear_memory(cls):
        cls._in_memory_records = []
