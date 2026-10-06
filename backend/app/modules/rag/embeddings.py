from abc import ABC, abstractmethod
from typing import List

from backend.app.modules.rag.schemas import EmbeddingVector, TextChunk


class BaseEmbeddingProvider(ABC):
    """Abstract interface for dense embedding generation."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generates embedding vector for a single query or text."""
        pass

    @abstractmethod
    def embed_chunks(self, chunks: List[TextChunk]) -> List[EmbeddingVector]:
        """Generates embedding vectors for a list of TextChunks."""
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """Returns embedding vector dimension."""
        pass
