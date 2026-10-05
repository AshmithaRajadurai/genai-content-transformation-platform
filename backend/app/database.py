import os
from typing import Dict, Any
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = (
    os.getenv("MONGODB_URI") or
    os.getenv("MONGO_URI") or
    "mongodb://localhost:27017"
)
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "genai_content_platform")

# Connect with 5-second server selection timeout to prevent hanging on connection issues
client: MongoClient = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000
)

db = client[MONGO_DB_NAME]


def check_connection() -> Dict[str, Any]:
    """Checks MongoDB connection health and ping latency."""
    try:
        client.admin.command("ping")
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