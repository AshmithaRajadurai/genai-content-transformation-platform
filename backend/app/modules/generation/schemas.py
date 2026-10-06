from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field

from backend.app.modules.nlp.schemas import NLPAnalysisResponse
from backend.app.modules.context.schemas import CompiledContextPayload
from backend.app.modules.llm.schemas import LLMBatchGenerationResponse


# --- Channel Specific Artefact Models ---

class LinkedInArtefact(BaseModel):
    channel_id: str = "linkedin"
    title: str = Field(..., description="Headline of the LinkedIn post")
    hook: str = Field(..., description="First line hook")
    content: str = Field(..., description="Full formatted post body")
    key_takeaways: List[str] = Field(default_factory=list, description="Bullet takeaways")
    hashtags: List[str] = Field(default_factory=list, description="Target hashtags")
    estimated_read_time: str = Field(default="1 min read", description="Estimated reading duration")


class TweetItem(BaseModel):
    index: int = Field(..., ge=1, description="Tweet position in thread")
    text: str = Field(..., max_length=320, description="Tweet text")
    char_count: int = Field(default=0, description="Character count")


class TwitterArtefact(BaseModel):
    channel_id: str = "twitter"
    hook: str = Field(..., description="Opening hook of the thread")
    tweets: List[TweetItem] = Field(default_factory=list, description="Ordered tweets in the thread")
    hashtags: List[str] = Field(default_factory=list, description="Thread hashtags")
    thread_length: int = Field(default=0, description="Total number of tweets")


class AdvisoryArtefact(BaseModel):
    channel_id: str = "advisory"
    advisory_id: str = Field(..., description="Generated or extracted advisory ID (e.g. ADV-2026-001)")
    severity: str = Field(default="CRITICAL / HIGH", description="Severity classification")
    title: str = Field(..., description="Official advisory title")
    impact: str = Field(..., description="Executive summary of threat/operational impact")
    affected_systems: List[str] = Field(default_factory=list, description="Affected components or environments")
    mitigation_steps: List[str] = Field(default_factory=list, description="Mandatory mitigation checklist")
    monitoring_actions: List[str] = Field(default_factory=list, description="Ongoing telemetry/audit instructions")
    references: List[str] = Field(default_factory=list, description="Source anchors and citations")


class ExecutiveSummaryArtefact(BaseModel):
    channel_id: str = "executive"
    title: str = Field(..., description="Executive briefing title")
    tldr: str = Field(..., description="Bottom-line upfront synopsis")
    business_impact: str = Field(..., description="Commercial, financial, and regulatory risk")
    key_points: List[str] = Field(default_factory=list, description="Crucial facts for leadership")
    recommendations: List[str] = Field(default_factory=list, description="Action items for the board/C-suite")
    decision_timeline: str = Field(default="Immediate (24-48 Hours)", description="Action timeframe")


class InfographicSection(BaseModel):
    title: str = Field(..., description="Panel section title")
    icon: str = Field(default="shield", description="Visual icon identifier")
    metric: str = Field(..., description="Key callout metric or data point")
    text: str = Field(..., description="Exploratory text")


class InfographicArtefact(BaseModel):
    channel_id: str = "infographic"
    title: str = Field(..., description="Infographic header")
    hero_stat: str = Field(..., description="Primary headline metric")
    theme: str = Field(..., description="Visual thematic domain")
    sections: List[InfographicSection] = Field(default_factory=list, description="Visual content panels")
    visual_flow_diagram: List[str] = Field(default_factory=list, description="Sequential steps in the visual flow")
    footer_badge: str = Field(default="Grounded via Factual Context Engine", description="Footer authenticity badge")


class SlideItem(BaseModel):
    slide_number: int = Field(..., ge=1, description="Slide index")
    title: str = Field(..., description="Slide title")
    subtitle: str = Field(default="", description="Slide subtitle")
    bullets: List[str] = Field(default_factory=list, description="Slide bullet points")
    speaker_notes: str = Field(default="", description="Presenter speaker notes")
    visual_cue: str = Field(default="", description="Slide layout / graphic direction")


class PresentationArtefact(BaseModel):
    channel_id: str = "presentation"
    title: str = Field(..., description="Deck title")
    slides: List[SlideItem] = Field(default_factory=list, description="Ordered slides")
    total_slides: int = Field(default=0, description="Total slide count")


class VideoScene(BaseModel):
    timestamp: str = Field(..., description="Timecode range (e.g. 0:00 - 0:10)")
    visual_cues: str = Field(..., description="B-Roll / screen graphic description")
    audio_narration: str = Field(..., description="Spoken voiceover script")
    text_overlay: str = Field(default="", description="On-screen title / lower-third text")


class VideoScriptArtefact(BaseModel):
    channel_id: str = "video"
    title: str = Field(..., description="Video production title")
    target_duration_seconds: int = Field(default=60, description="Target video runtime in seconds")
    scenes: List[VideoScene] = Field(default_factory=list, description="Ordered production scenes")
    subtitles: List[str] = Field(default_factory=list, description="Timed caption transcript")
    visual_recommendations: List[str] = Field(default_factory=list, description="Director and motion graphics guidelines")


# --- Pipeline Orchestration Request & Response ---

class TransformationPipelineRequest(BaseModel):
    source_text: str = Field(..., min_length=10, description="Source content text to transform")
    title: Optional[str] = Field(None, max_length=200, description="Optional explicit document title")
    source_type: Optional[str] = Field("text", description="Source format: text, pdf, docx, advisory")
    target_channels: List[str] = Field(
        default_factory=lambda: [
            "linkedin", "twitter", "advisory", "executive",
            "infographic", "presentation", "video"
        ],
        description="Target output formats to synthesize"
    )
    audience: Optional[str] = Field("Business Executives & C-Suite", description="Target audience persona")
    tone: Optional[str] = Field("Professional & Authoritative", description="Target communication tone")
    language: Optional[str] = Field("English (US)", description="Output language")
    detail_level: Optional[str] = Field("Balanced (Standard Comprehensive Overview)", description="Detail level")
    provider: Optional[str] = Field("auto", description="LLM provider: auto, gemini, openai, fallback, n8n")


class TransformationPipelineResponse(BaseModel):
    transformation_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique transformation identifier"
    )
    source_title: str = Field(..., description="Resolved source title")
    source_type: str = Field(..., description="Source format")
    nlp_analysis: NLPAnalysisResponse = Field(..., description="Layer 2: Real NLP Extraction results")
    context_payload: CompiledContextPayload = Field(..., description="Layer 3: Context Engine Grounding & Prompts")
    llm_batch_response: LLMBatchGenerationResponse = Field(..., description="Layer 4: Real LLM Generation results")
    artefacts: Dict[str, Any] = Field(..., description="Layer 5: Structured Generative AI Artefacts per channel")
    total_tokens: int = Field(default=0, description="Total tokens consumed across all stages")
    execution_time_ms: float = Field(default=0.0, description="End-to-end processing latency in milliseconds")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO timestamp of pipeline execution"
    )
