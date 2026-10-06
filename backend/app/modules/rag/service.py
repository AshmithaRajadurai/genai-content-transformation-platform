import logging
from typing import List, Optional

from backend.app.modules.rag.schemas import (
    RAGStatusResponse,
    TextChunk,
    RetrievedContext,
)
from backend.app.modules.rag.chunker import TextChunker, BaseChunker
from backend.app.modules.rag.embeddings import BaseEmbeddingProvider
from backend.app.modules.rag.vector_store import BaseVectorStore
from backend.app.modules.rag.retriever import BaseRetriever

logger = logging.getLogger("rag_service")


class RAGService:
    """
    RAG (Retrieval-Augmented Generation) Orchestration Service:
    Coordinates document chunking, embedding generation, vector store indexing,
    and semantic retrieval.
    Architecture interfaces are established; actual vector database binding
    will occur in the subsequent RAG implementation phase.
    """

    _chunker: BaseChunker = TextChunker()
    _embeddings: Optional[BaseEmbeddingProvider] = None
    _vector_store: Optional[BaseVectorStore] = None
    _retriever: Optional[BaseRetriever] = None

    @classmethod
    def get_status(cls) -> RAGStatusResponse:
        """Returns the readiness status of the RAG module."""
        return RAGStatusResponse(
            status="ready",
            is_active=False,
            architecture_status=(
                "RAG architectural abstractions and pipeline interfaces successfully established. "
                "Vector database indexing and semantic retrieval implementation will be connected in next phase."
            ),
            supported_components=[
                "TextChunker (sentence-preserving sliding window)",
                "BaseEmbeddingProvider (abstract interface)",
                "BaseVectorStore (abstract interface)",
                "BaseRetriever (abstract interface)"
            ]
        )

    @classmethod
    def chunk_document(
        cls,
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        document_id: Optional[str] = None
    ) -> List[TextChunk]:
        """Splits document content into structured chunks."""
        return cls._chunker.chunk(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            document_id=document_id
        )

    @classmethod
    def retrieve_context(cls, query: str, top_k: int = 4) -> List[RetrievedContext]:
        """
        Retrieval hook for the pipeline.
        Returns empty list until vector store provider is configured in next phase.
        """
        if cls._retriever is not None:
            return cls._retriever.retrieve(query, top_k=top_k)
        return []
