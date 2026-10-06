from abc import ABC, abstractmethod
from typing import List, Optional

from backend.app.modules.rag.schemas import EmbeddingVector, RetrievedContext, TextChunk


class BaseVectorStore(ABC):
    """Abstract interface for vector database storage and similarity indexing."""

    @abstractmethod
    def upsert(self, chunks: List[TextChunk], vectors: List[EmbeddingVector]) -> int:
        """Stores chunks alongside their embedding vectors. Returns count inserted."""
        pass

    @abstractmethod
    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filters: Optional[dict] = None
    ) -> List[RetrievedContext]:
        """Performs nearest-neighbor similarity search."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Returns total vector records stored."""
        pass

    @abstractmethod
    def delete(self, document_id: str) -> bool:
        """Deletes all chunks belonging to a document."""
        pass
