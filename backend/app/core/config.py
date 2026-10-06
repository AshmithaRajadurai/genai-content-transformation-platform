import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central application configuration reading from environment variables."""

    PROJECT_NAME: str = "GenAI Content Transformation Platform"
    PROJECT_VERSION: str = "0.4.0"
    API_V1_PREFIX: str = "/api/v1"

    # MongoDB Settings
    MONGO_URI: str = (
        os.getenv("MONGODB_URI") or
        os.getenv("MONGO_URI") or
        "mongodb://localhost:27017"
    )
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "genai_content_platform")
    MONGO_TIMEOUT_MS: int = int(os.getenv("MONGO_TIMEOUT_MS", "4000"))

    # LLM API Keys
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # n8n Workflow Orchestration
    N8N_WEBHOOK_URL: Optional[str] = os.getenv("N8N_WEBHOOK_URL")


settings = Settings()
