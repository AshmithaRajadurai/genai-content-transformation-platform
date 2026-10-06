import os
from typing import Optional
import httpx

from backend.app.modules.llm.schemas import LLMProviderInfo
from backend.app.modules.llm.providers.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM Provider."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()

    def is_available(self) -> bool:
        return bool(self.api_key)

    def get_info(self) -> LLMProviderInfo:
        return LLMProviderInfo(
            id="gemini",
            name="Google Gemini",
            status="configured" if self.is_available() else "available (key needed)",
            active_model="gemini-1.5-flash",
            description="Google DeepMind Gemini high-speed multi-modal reasoning engine."
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

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        payload = {
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "parts": [{"text": user_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        try:
            with httpx.Client(timeout=15.0) as client:
                res = client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
        except Exception:
            pass
        return None
