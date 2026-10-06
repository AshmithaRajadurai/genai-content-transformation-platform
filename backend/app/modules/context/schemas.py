from typing import List, Dict, Optional, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from backend.app.modules.nlp.schemas import NamedEntity, KeywordItem, NLPAnalysisResponse


class ChannelInstruction(BaseModel):
    channel_id: str = Field(..., description="Target output format identifier (e.g. linkedin, twitter, advisory)")
    name: str = Field(..., description="Human-readable channel name")
    audience: str = Field(..., description="Audience persona tailored for this channel")
    tone: str = Field(..., description="Target communication tone")
    format_guidelines: List[str] = Field(default_factory=list, description="Formatting and structure requirements")
    length_constraints: str = Field(..., description="Target length or word count limit")
    required_elements: List[str] = Field(default_factory=list, description="Mandatory elements (e.g. hashtags, key takeaways, call to action)")


class ContextBuildRequest(BaseModel):
    source_text: str = Field(..., min_length=10, description="Raw or normalized source content text")
    title: Optional[str] = Field(None, max_length=200, description="Document title or header")
    source_type: Optional[str] = Field("text", description="Source format (e.g. text, pdf, docx, advisory)")
    nlp_analysis: Optional[NLPAnalysisResponse] = Field(
        None,
        description="Pre-computed NLP analysis. If omitted, Context Engine will generate NLP analysis automatically."
    )
    target_channels: List[str] = Field(
        default_factory=lambda: ["linkedin", "executive_summary"],
        description="Target output formats to prepare context for"
    )
    audience: Optional[str] = Field("General Enterprise & Technical Leaders", description="Target audience persona")
    tone: Optional[str] = Field("Professional & Authoritative", description="Primary tone of voice")
    language: Optional[str] = Field("English", description="Target output language")
    detail_level: Optional[str] = Field("balanced", description="Detail depth: concise, balanced, or comprehensive")


class ChannelContextPrompt(BaseModel):
    channel_id: str = Field(..., description="Target channel ID")
    channel_name: str = Field(..., description="Human-readable channel name")
    system_prompt: str = Field(..., description="Specialized system instructions for this channel")
    user_prompt: str = Field(..., description="Formatted user prompt combining facts, context, and structural requirements")
    grounding_rules: List[str] = Field(default_factory=list, description="Strict factual anti-hallucination rules")


class CompiledContextPayload(BaseModel):
    source_title: str = Field(..., description="Resolved document title")
    source_type: str = Field(..., description="Source document format")
    identified_topic: str = Field(..., description="Identified core domain topic")
    core_facts: List[str] = Field(..., description="Verified key factual assertions extracted from source")
    guaranteed_entities: List[NamedEntity] = Field(..., description="Entities (CVEs, products, orgs) that must be preserved")
    salient_keywords: List[str] = Field(..., description="Top domain keywords to naturally weave into outputs")
    context_summary: str = Field(..., description="Condensed summary synthesized for LLM grounding")
    audience_persona: str = Field(..., description="Target audience persona profile")
    tone_guideline: str = Field(..., description="Applied tone directives")
    language: str = Field(..., description="Output language")
    detail_level: str = Field(..., description="Detail level: concise, balanced, comprehensive")
    global_system_instruction: str = Field(..., description="Global guardrails and anti-hallucination instructions")
    channel_prompts: Dict[str, ChannelContextPrompt] = Field(..., description="Ready-to-execute prompts for each requested channel")
    compiled_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="ISO timestamp of compilation")
