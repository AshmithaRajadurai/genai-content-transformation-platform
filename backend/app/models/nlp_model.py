from typing import List, Optional
from pydantic import BaseModel, Field


class NamedEntity(BaseModel):
    name: str = Field(..., description="Entity surface name")
    type: str = Field(..., description="Entity category: PRODUCT, VULNERABILITY, ORGANIZATION, TECHNOLOGY, ROLE, STANDARD, etc.")
    frequency: int = Field(default=1, ge=1, description="Number of occurrences in text")


class KeywordItem(BaseModel):
    keyword: str = Field(..., description="Extracted key term or n-gram")
    relevance: float = Field(..., ge=0.0, le=1.0, description="Normalized relevance score")


class NLPAnalysisRequest(BaseModel):
    content: str = Field(
        ...,
        min_length=10,
        description="Source text content to analyze",
        examples=["Critical security advisory CVE-2026-4401 in Cloud Gateway authentication..."]
    )
    title: Optional[str] = Field(None, max_length=200, description="Optional document title")
    source_type: Optional[str] = Field("text", description="Optional source format/type")


class NLPAnalysisResponse(BaseModel):
    topic: str = Field(..., description="Primary identified topic domain")
    topics: List[str] = Field(default_factory=list, description="All identified topics/categories")
    content_type: str = Field(..., description="Inferred document type: Security Advisory, Research Briefing, Policy, Incident Report, etc.")
    detected_tone: str = Field(..., description="Inferred communication tone and emotional register")
    keywords: List[str] = Field(..., description="Top salient keywords and keyphrases")
    keyword_items: List[KeywordItem] = Field(default_factory=list, description="Keywords with relevance scores")
    entities: List[NamedEntity] = Field(..., description="Named entities identified in the text")
    key_facts: List[str] = Field(..., description="Core extracted factual statements and assertions")
    summary_context: str = Field(..., description="Condensed contextual summary prepared for the Context Engine and LLM")
    confidence_score: float = Field(..., ge=0.0, le=100.0, description="Overall extraction confidence score (0-100)")
