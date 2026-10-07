import logging
import uuid
from typing import Any, Dict, List, Optional

from backend.app.modules.rag.schemas import (
    RAGIndexResponse,
    RAGStatusResponse,
    RetrievedContext,
    TextChunk,
    EmbeddingVector,
)
from backend.app.modules.rag.chunker import TextChunker, BaseChunker
from backend.app.modules.rag.embeddings import (
    BaseEmbeddingProvider,
    get_embedding_provider,
)
from backend.app.modules.rag.vector_store import (
    BaseVectorStore,
    InMemoryVectorStore,
)
from backend.app.modules.rag.retriever import (
    BaseRetriever,
    SemanticRetriever,
)

logger = logging.getLogger("rag_service")


class RAGService:
    """
    RAG (Retrieval-Augmented Generation) Orchestration Service:
    Coordinates document chunking, dense embeddings, in-memory vector storage,
    and semantic context retrieval.
    """

    _chunker: BaseChunker = TextChunker()
    _embeddings: Optional[BaseEmbeddingProvider] = None
    _vector_store: Optional[BaseVectorStore] = None
    _retriever: Optional[BaseRetriever] = None

    @classmethod
    def get_embedding_provider(cls) -> BaseEmbeddingProvider:
        if cls._embeddings is None:
            cls._embeddings = get_embedding_provider()
        return cls._embeddings

    @classmethod
    def get_vector_store(cls) -> BaseVectorStore:
        if cls._vector_store is None:
            cls._vector_store = InMemoryVectorStore()
        return cls._vector_store

    @classmethod
    def get_retriever(cls) -> BaseRetriever:
        if cls._retriever is None:
            cls._retriever = SemanticRetriever(
                embedding_provider=cls.get_embedding_provider(),
                vector_store=cls.get_vector_store(),
            )
        return cls._retriever

    @classmethod
    def get_status(cls) -> RAGStatusResponse:
        """Returns the readiness and indexing status of the RAG module."""
        store = cls.get_vector_store()
        provider = cls.get_embedding_provider()
        total_chunks = store.count()

        return RAGStatusResponse(
            status="ready",
            is_active=total_chunks > 0,
            architecture_status=(
                f"Local RAG pipeline online: {provider.provider_name} "
                f"(model={provider.model_name}, dim={provider.dimension}), "
                f"InMemoryVectorStore ({total_chunks} indexed chunks), SemanticRetriever."
            ),
            supported_components=[
                "TextChunker (sentence-preserving sliding window)",
                f"BaseEmbeddingProvider ({provider.provider_name})",
                "InMemoryVectorStore (NumPy cosine similarity)",
                "SemanticRetriever (top-k threshold ranking)"
            ],
            total_indexed_chunks=total_chunks,
            embedding_provider=provider.provider_name,
            embedding_dimension=provider.dimension,
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
    def index_document(
        cls,
        text: str,
        document_id: Optional[str] = None,
        title: Optional[str] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RAGIndexResponse:
        """
        Chunks source text, generates dense vector embeddings, and stores them in the vector store.
        """
        cleaned_text = (text or "").strip()
        if not cleaned_text:
            raise ValueError("Document text cannot be empty for indexing.")

        doc_id = document_id or str(uuid.uuid4())
        chunks = cls.chunk_document(
            text=cleaned_text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            document_id=doc_id,
        )

        if not chunks:
            raise ValueError("No text chunks generated from the provided text.")

        # Attach custom metadata to each chunk
        for chunk in chunks:
            if title:
                chunk.metadata.metadata["title"] = title
            if metadata:
                chunk.metadata.metadata.update(metadata)

        chunk_texts = [c.text for c in chunks]
        embeddings = cls.get_embedding_provider().embed_batch(chunk_texts)

        vector_objects: List[EmbeddingVector] = []
        for chunk, vec in zip(chunks, embeddings):
            vector_objects.append(
                EmbeddingVector(
                    chunk_id=chunk.chunk_id,
                    vector=vec,
                    dimension=len(vec)
                )
            )

        store = cls.get_vector_store()
        indexed_count = store.upsert(chunks, vector_objects)

        logger.info(
            "Indexed %d chunks for document %s (total vectors in store: %d)",
            indexed_count,
            doc_id,
            store.count()
        )

        return RAGIndexResponse(
            document_id=doc_id,
            chunks_indexed=indexed_count,
            total_vectors=store.count(),
            message=f"Successfully indexed {indexed_count} chunks for document {doc_id}."
        )

    @classmethod
    def retrieve_context(
        cls,
        query: str,
        top_k: int = 4,
        score_threshold: Optional[float] = None,
        document_id: Optional[str] = None,
    ) -> List[RetrievedContext]:
        """
        Retrieval hook for semantic context search.
        Embeds the query and retrieves the top-k most similar chunks.
        """
        filters = {"document_id": document_id} if document_id else None
        retriever = cls.get_retriever()
        return retriever.retrieve(
            query=query,
            top_k=top_k,
            score_threshold=score_threshold,
            filters=filters
        )

    @classmethod
    def delete_document(cls, document_id: str) -> bool:
        """Deletes all chunks belonging to a document."""
        return cls.get_vector_store().delete(document_id)

    @classmethod
    def clear(cls) -> None:
        """Clears all indexed vectors from the store."""
        cls.get_vector_store().clear()

    @classmethod
    def count(cls) -> int:
        """Returns total vector count in the store."""
        return cls.get_vector_store().count()
