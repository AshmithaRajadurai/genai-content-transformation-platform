from abc import ABC, abstractmethod
from typing import Optional
from backend.app.modules.llm.schemas import LLMProviderInfo


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers in the platform."""

    @abstractmethod
    def get_info(self) -> LLMProviderInfo:
        """Returns metadata regarding provider configuration and model."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Determines if the provider is currently usable."""
        pass

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> Optional[str]:
        """Executes content generation using the provider."""
        pass
