from typing import Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from backend.app.modules.context.schemas import CompiledContextPayload, ChannelContextPrompt


class LLMProviderInfo(BaseModel):
    id: str = Field(..., description="Provider identifier (gemini, openai, local, fallback, n8n)")
    name: str = Field(..., description="Human-readable provider name")
    status: str = Field(..., description="Provider availability status: active, configured, or fallback")
    active_model: str = Field(..., description="Model identifier in use")
    description: str = Field(..., description="Description of the provider capabilities")


class LLMGenerationRequest(BaseModel):
    channel_id: str = Field(..., description="Target output channel ID (e.g. linkedin, twitter, advisory)")
    channel_name: Optional[str] = Field(None, description="Human-readable channel title")
    system_prompt: str = Field(..., min_length=10, description="System instruction containing guardrails and tone")
    user_prompt: str = Field(..., min_length=10, description="User prompt containing factual context and formatting rules")
    provider: Optional[str] = Field("auto", description="Selected LLM provider: auto, gemini, openai, fallback, or n8n")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(1500, ge=100, le=4096, description="Maximum token budget")


class LLMGenerationResponse(BaseModel):
    channel_id: str = Field(..., description="Target channel ID")
    channel_name: str = Field(..., description="Human-readable channel title")
    provider: str = Field(..., description="LLM provider that executed generation")
    model: str = Field(..., description="Exact model name used")
    content: str = Field(..., description="Generated text content for this channel")
    tokens_used: int = Field(default=0, ge=0, description="Estimated or actual tokens consumed")
    finish_reason: str = Field(default="stop", description="Execution stop reason")
    generated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO timestamp of generation"
    )


class LLMBatchGenerationRequest(BaseModel):
    context_payload: CompiledContextPayload = Field(
        ...,
        description="Complete CompiledContextPayload from the Context Engine"
    )
    provider: Optional[str] = Field("auto", description="LLM provider preference")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0, description="Sampling temperature")


class LLMBatchGenerationResponse(BaseModel):
    source_title: str = Field(..., description="Source document title")
    provider: str = Field(..., description="Provider executed")
    results: Dict[str, LLMGenerationResponse] = Field(
        ...,
        description="Mapping of channel ID to generated LLM output"
    )
    total_tokens: int = Field(default=0, description="Total tokens consumed across all channels")
    execution_time_ms: float = Field(default=0.0, description="Total processing latency in milliseconds")
