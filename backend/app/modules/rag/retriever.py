import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from backend.app.modules.rag.schemas import RetrievedContext
from backend.app.modules.rag.embeddings import BaseEmbeddingProvider
from backend.app.modules.rag.vector_store import BaseVectorStore

logger = logging.getLogger("semantic_retriever")


class BaseRetriever(ABC):
    """Abstract interface for semantic context retrieval."""

    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[RetrievedContext]:
        """Retrieves most relevant context passages given a user query."""
        pass


class SemanticRetriever(BaseRetriever):
    """
    Semantic Retriever combining dense embedding generation with vector similarity search.
    """

    def __init__(
        self,
        embedding_provider: BaseEmbeddingProvider,
        vector_store: BaseVectorStore
    ) -> None:
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[RetrievedContext]:
        """
        Embeds the query text, queries the vector store, and returns top-k matching contexts.
        Optionally filters results below the score_threshold.
        """
        cleaned_query = (query or "").strip()
        if not cleaned_query:
            return []

        try:
            query_vector = self.embedding_provider.embed_text(cleaned_query)
        except Exception as exc:
            logger.error("Failed to generate query embedding: %s", exc)
            return []

        matches = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
            filters=filters
        )

        if score_threshold is not None:
            matches = [ctx for ctx in matches if ctx.relevance_score >= score_threshold]

        return matches
