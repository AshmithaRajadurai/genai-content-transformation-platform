import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

logger = logging.getLogger("database")

MONGO_URI = (
    os.getenv("MONGODB_URI") or
    os.getenv("MONGO_URI") or
    "mongodb://localhost:27017"
)
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "genai_content_platform")
MONGO_TIMEOUT_MS = int(os.getenv("MONGO_TIMEOUT_MS", "4000"))

_client: Optional[MongoClient] = None


def get_client() -> Optional[MongoClient]:
    """Lazily initializes and caches the MongoClient instance."""
    global _client
    if _client is not None:
        return _client
    try:
        _client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=MONGO_TIMEOUT_MS,
            connectTimeoutMS=MONGO_TIMEOUT_MS,
            connect=False
        )
        return _client
    except Exception as exc:
        logger.warning("MongoDB client initialization failed: %s", exc)
        return None


class LazyDatabaseProxy:
    """Proxy object so `from backend.app.database import db` works seamlessly without import-time crashes."""
    def __getitem__(self, collection_name: str):
        c = get_client()
        if c is None:
            raise RuntimeError("MongoDB client is unavailable")
        return c[MONGO_DB_NAME][collection_name]

    def __getattr__(self, name: str):
        c = get_client()
        if c is None:
            raise RuntimeError("MongoDB client is unavailable")
        return getattr(c[MONGO_DB_NAME], name)


db = LazyDatabaseProxy()


def check_connection() -> Dict[str, Any]:
    """Checks MongoDB connection health and ping latency."""
    try:
        c = get_client()
        if c is None:
            return {
                "status": "disconnected",
                "database": MONGO_DB_NAME,
                "error": "MongoClient initialization failed"
            }
        c.admin.command("ping")
        return {
            "status": "connected",
            "database": MONGO_DB_NAME,
            "type": "atlas_cloud" if "mongodb.net" in MONGO_URI else "local"
        }
    except Exception as exc:
        return {
            "status": "disconnected",
            "database": MONGO_DB_NAME,
            "error": str(exc)
        }