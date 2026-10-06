from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class SourceTextInput(BaseModel):
    content: str = Field(
        ...,
        min_length=5,
        max_length=500_000,
        description="Raw source content to be ingested (article, report, advisory, prompt, etc.)",
        examples=["Critical security advisory CVE-2026-4401 in Cloud Gateway..."]
    )
    title: Optional[str] = Field(
        None,
        max_length=200,
        description="Optional title for the source document"
    )
    source_type: Optional[str] = Field(
        "text",
        description="Category/type of source input (e.g. text, article, advisory, report, prompt)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Optional caller metadata or routing tags"
    )


class IngestionResponse(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique UUID identifier for this ingested document"
    )
    title: str = Field(
        ...,
        description="Detected or provided document title"
    )
    raw_content: str = Field(
        ...,
        description="Original uncleaned source content"
    )
    cleaned_content: str = Field(
        ...,
        description="Normalized and sanitized text ready for NLP processing"
    )
    source_type: str = Field(
        ...,
        description="Detected format or category (text, pdf, docx, markdown, etc.)"
    )
    word_count: int = Field(
        ...,
        ge=0,
        description="Word count of normalized content"
    )
    char_count: int = Field(
        ...,
        ge=0,
        description="Character count of normalized content"
    )
    estimated_reading_time_minutes: int = Field(
        ...,
        ge=0,
        description="Estimated reading time in minutes (based on 200 wpm)"
    )
    filename: Optional[str] = Field(
        None,
        description="Original filename if uploaded as a file"
    )
    file_size_bytes: Optional[int] = Field(
        None,
        description="Size in bytes if uploaded as a file"
    )
    mime_type: Optional[str] = Field(
        None,
        description="MIME content type of input"
    )
    ingested_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of ingestion"
    )
    status: str = Field(
        "ingested",
        description="Status of ingestion pipeline (ingested, validated)"
    )
    message: str = Field(
        "Source content successfully ingested and normalized.",
        description="Status confirmation message"
    )
