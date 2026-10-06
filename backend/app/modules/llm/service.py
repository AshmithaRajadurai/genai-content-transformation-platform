import os
import time
from typing import Dict, List, Optional

from backend.app.modules.llm.schemas import (
    LLMProviderInfo,
    LLMGenerationRequest,
    LLMGenerationResponse,
    LLMBatchGenerationRequest,
    LLMBatchGenerationResponse,
)
from backend.app.modules.llm.providers.gemini import GeminiProvider
from backend.app.modules.llm.providers.openai import OpenAIProvider
from backend.app.modules.llm.providers.fallback import FallbackProvider
from backend.app.modules.llm.providers.n8n import N8nLLMProvider


class LLMService:
    """
    LLM Orchestration Layer:
    Provides multi-provider LLM access (Gemini, OpenAI, n8n) with a robust,
    zero-hallucination semantic synthesis fallback engine when external
    API keys are not configured.
    """

    _gemini_provider = GeminiProvider()
    _openai_provider = OpenAIProvider()
    _fallback_provider = FallbackProvider()
    _n8n_provider = N8nLLMProvider()

    @classmethod
    def get_available_providers(cls) -> List[LLMProviderInfo]:
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()

        providers = [
            LLMProviderInfo(
                id="gemini",
                name="Google Gemini",
                status="configured" if gemini_key else "available (key needed)",
                active_model="gemini-1.5-flash",
                description="Google DeepMind Gemini high-speed multi-modal reasoning engine."
            ),
            LLMProviderInfo(
                id="openai",
                name="OpenAI GPT",
                status="configured" if openai_key else "available (key needed)",
                active_model="gpt-4o-mini",
                description="OpenAI flagship instruction-tuned completion engine."
            ),
            LLMProviderInfo(
                id="fallback",
                name="Local High-Fidelity LLM Synthesizer",
                status="active",
                active_model="semantic-fusion-engine-v1",
                description="Built-in deterministic prompt-conditioned semantic transformation engine adhering strictly to factual guardrails."
            ),
            cls._n8n_provider.get_info()
        ]
        return providers

    @classmethod
    def resolve_provider(cls, requested: Optional[str] = "auto") -> str:
        req = (requested or "auto").lower()
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        n8n_configured = cls._n8n_provider.is_available()

        if req == "gemini" and gemini_key:
            return "gemini"
        if req == "openai" and openai_key:
            return "openai"
        if req == "n8n" and n8n_configured:
            return "n8n"
        if req == "auto":
            if gemini_key:
                return "gemini"
            if openai_key:
                return "openai"
            if n8n_configured:
                return "n8n"
        return "fallback"

    @classmethod
    def _call_gemini_api(
        cls,
        system_prompt: str,
        user_prompt: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> Optional[str]:
        provider = GeminiProvider(api_key=api_key)
        return provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

    @classmethod
    def _call_openai_api(
        cls,
        system_prompt: str,
        user_prompt: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> Optional[str]:
        provider = OpenAIProvider(api_key=api_key)
        return provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

    @classmethod
    def _synthesize_fallback_channel_content(
        cls,
        channel_id: str,
        channel_name: str,
        user_prompt: str
    ) -> str:
        return cls._fallback_provider.synthesize(
            channel_id=channel_id,
            channel_name=channel_name,
            user_prompt=user_prompt
        )

    @classmethod
    def generate(cls, request: LLMGenerationRequest) -> LLMGenerationResponse:
        provider = cls.resolve_provider(request.provider)
        channel_name = request.channel_name or request.channel_id.replace("_", " ").title()
        content: Optional[str] = None
        model_name = "semantic-fusion-engine-v1"

        if provider == "gemini":
            content = cls._gemini_provider.generate(
                system_prompt=request.system_prompt,
                user_prompt=request.user_prompt,
                temperature=request.temperature or 0.7,
                max_tokens=request.max_tokens or 1500
            )
            model_name = "gemini-1.5-flash"

        elif provider == "openai":
            content = cls._openai_provider.generate(
                system_prompt=request.system_prompt,
                user_prompt=request.user_prompt,
                temperature=request.temperature or 0.7,
                max_tokens=request.max_tokens or 1500
            )
            model_name = "gpt-4o-mini"

        elif provider == "n8n":
            content = cls._n8n_provider.generate(
                system_prompt=request.system_prompt,
                user_prompt=request.user_prompt,
                temperature=request.temperature or 0.7,
                max_tokens=request.max_tokens or 1500,
                channel_id=request.channel_id
            )
            model_name = "n8n-orchestrated-llm"

        # Fallback if provider was not selected or external API failed
        if not content:
            content = cls._fallback_provider.synthesize(
                channel_id=request.channel_id,
                channel_name=channel_name,
                user_prompt=request.user_prompt
            )
            provider = "fallback"
            model_name = "semantic-fusion-engine-v1"

        word_count = len(content.split())
        estimated_tokens = int(word_count * 1.35)

        return LLMGenerationResponse(
            channel_id=request.channel_id,
            channel_name=channel_name,
            provider=provider,
            model=model_name,
            content=content,
            tokens_used=estimated_tokens,
            finish_reason="stop"
        )

    @classmethod
    def generate_batch(cls, request: LLMBatchGenerationRequest) -> LLMBatchGenerationResponse:
        t0 = time.time()
        payload = request.context_payload
        results: Dict[str, LLMGenerationResponse] = {}
        total_tokens = 0
        provider_used = "fallback"

        for channel_id, prompt_item in payload.channel_prompts.items():
            gen_req = LLMGenerationRequest(
                channel_id=channel_id,
                channel_name=prompt_item.channel_name,
                system_prompt=prompt_item.system_prompt,
                user_prompt=prompt_item.user_prompt,
                provider=request.provider,
                temperature=request.temperature or 0.7
            )
            response = cls.generate(gen_req)
            results[channel_id] = response
            total_tokens += response.tokens_used
            provider_used = response.provider

        latency_ms = round((time.time() - t0) * 1000, 2)

        return LLMBatchGenerationResponse(
            source_title=payload.source_title,
            provider=provider_used,
            results=results,
            total_tokens=total_tokens,
            execution_time_ms=latency_ms
        )
