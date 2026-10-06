from abc import ABC, abstractmethod
from typing import List, Optional

from backend.app.modules.rag.schemas import RetrievedContext


class BaseRetriever(ABC):
    """Abstract interface for semantic context retrieval."""

    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        score_threshold: Optional[float] = None
    ) -> List[RetrievedContext]:
        """Retrieves most relevant context passages given a user query."""
        pass
