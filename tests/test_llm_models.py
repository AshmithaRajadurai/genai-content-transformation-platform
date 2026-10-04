import pytest
from backend.app.models.llm_model import (
    LLMProviderInfo,
    LLMGenerationRequest,
    LLMGenerationResponse,
    LLMBatchGenerationRequest,
    LLMBatchGenerationResponse
)
from backend.app.models.context_model import CompiledContextPayload, ChannelContextPrompt


def test_llm_generation_request_defaults():
    req = LLMGenerationRequest(
        channel_id="linkedin",
        system_prompt="You are an executive communications expert.",
        user_prompt="Transform source facts into a LinkedIn post."
    )
    assert req.provider == "auto"
    assert req.temperature == 0.7
    assert req.max_tokens == 1500


def test_llm_generation_response():
    resp = LLMGenerationResponse(
        channel_id="linkedin",
        channel_name="LinkedIn Thought Leadership Post",
        provider="gemini",
        model="gemini-1.5-flash",
        content="🚀 Critical update on cloud infrastructure security...",
        tokens_used=420,
        finish_reason="stop"
    )
    assert resp.channel_id == "linkedin"
    assert resp.provider == "gemini"
    assert "Critical update" in resp.content


def test_llm_batch_response():
    resp = LLMBatchGenerationResponse(
        source_title="Threat Advisory 2026",
        provider="fallback",
        results={
            "linkedin": LLMGenerationResponse(
                channel_id="linkedin",
                channel_name="LinkedIn Post",
                provider="fallback",
                model="deterministic-llm-engine",
                content="Post content",
                tokens_used=300
            )
        },
        total_tokens=300,
        execution_time_ms=45.2
    )
    assert resp.source_title == "Threat Advisory 2026"
    assert "linkedin" in resp.results
