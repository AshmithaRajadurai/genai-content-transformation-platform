import os
from typing import Optional
import httpx

from backend.app.modules.llm.schemas import LLMProviderInfo
from backend.app.modules.llm.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT LLM Provider."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "").strip()

    def is_available(self) -> bool:
        return bool(self.api_key)

    def get_info(self) -> LLMProviderInfo:
        return LLMProviderInfo(
            id="openai",
            name="OpenAI GPT",
            status="configured" if self.is_available() else "available (key needed)",
            active_model="gpt-4o-mini",
            description="OpenAI flagship instruction-tuned completion engine."
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> Optional[str]:
        if not self.is_available():
            return None

        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            with httpx.Client(timeout=15.0) as client:
                res = client.post(url, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
        except Exception:
            pass
        return None
