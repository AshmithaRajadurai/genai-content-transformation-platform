from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field


class TransformationRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Internal database ID")
    transformation_id: str = Field(..., description="Unique transformation UUID")
    source_title: str = Field(..., description="Document title")
    source_type: str = Field(default="text", description="Source format: text, pdf, docx, advisory")
    source_text: str = Field(..., description="Raw or normalized source content")
    selected_channels: List[str] = Field(default_factory=list, description="Target generated formats")
    audience: str = Field(default="General Enterprise", description="Target audience persona")
    tone: str = Field(default="Professional", description="Target communication tone")
    language: str = Field(default="English", description="Target language")
    detail_level: str = Field(default="Balanced", description="Detail level")
    detected_topic: str = Field(default="General", description="Topic identified by NLP")
    keywords: List[str] = Field(default_factory=list, description="Top extracted keywords")
    entities_count: int = Field(default=0, description="Total recognized entities")
    key_facts_count: int = Field(default=0, description="Total verified facts")
    artefacts: Dict[str, Any] = Field(default_factory=dict, description="Generated multi-channel artefacts")
    total_tokens: int = Field(default=0, description="Total tokens consumed")
    execution_time_ms: float = Field(default=0.0, description="Processing latency")
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO creation timestamp"
    )


class HistoryItemSummary(BaseModel):
    transformation_id: str = Field(..., description="Unique transformation UUID")
    source_title: str = Field(..., description="Document title")
    detected_topic: str = Field(..., description="NLP-identified topic")
    channels: List[str] = Field(default_factory=list, description="Generated channels")
    created_at: str = Field(..., description="Creation timestamp")
    total_tokens: int = Field(default=0, description="Tokens used")


class HistoryListResponse(BaseModel):
    total: int = Field(default=0, description="Total recorded transformations")
    database_status: str = Field(..., description="Database connection health: connected or offline_fallback")
    items: List[HistoryItemSummary] = Field(default_factory=list, description="List of recent transformations")


class StorageHealthResponse(BaseModel):
    status: str = Field(..., description="connected or disconnected")
    database: str = Field(..., description="MongoDB database name")
    type: str = Field(default="atlas_cloud", description="Database hosting type: atlas_cloud or local")
    record_count: int = Field(default=0, description="Total saved records in collection")
    error: Optional[str] = Field(None, description="Diagnostic error message if disconnected")
