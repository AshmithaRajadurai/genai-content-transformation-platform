import os
from typing import Optional

from backend.app.modules.llm.schemas import LLMProviderInfo
from backend.app.modules.llm.providers.base import BaseLLMProvider
from backend.app.modules.n8n.client import n8n_client
from backend.app.modules.n8n.webhooks import N8nWebhookPayload


class N8nLLMProvider(BaseLLMProvider):
    """
    n8n Workflow Orchestration LLM Provider:
    Delegates prompt synthesis to an n8n webhook workflow orchestrating
    local or hosted LLM nodes (Ollama, vLLM, self-hosted models).
    """

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("N8N_WEBHOOK_URL", "").strip()

    def is_available(self) -> bool:
        return bool(self.webhook_url or n8n_client.is_configured())

    def get_info(self) -> LLMProviderInfo:
        return LLMProviderInfo(
            id="n8n",
            name="n8n Workflow Orchestrator",
            status="configured" if self.is_available() else "available (webhook url needed)",
            active_model="n8n-orchestrated-llm",
            description="n8n automated workflow engine coordinating multi-agent chains, local Ollama, and tool integrations."
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500,
        channel_id: str = "general"
    ) -> Optional[str]:
        if not self.is_available():
            return None

        payload = N8nWebhookPayload(
            channel_id=channel_id,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        response_data = n8n_client.trigger_workflow(
            payload.model_dump(),
            custom_endpoint=self.webhook_url or None
        )
        if response_data and isinstance(response_data, dict):
            # Supports direct 'content', 'generated_content', or 'text' output
            return (
                response_data.get("generated_content") or
                response_data.get("content") or
                response_data.get("text")
            )
        return None
