from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    document_id: Optional[str] = Field(None, description="Source document UUID")
    chunk_index: int = Field(..., description="Zero-based sequence index")
    char_start: int = Field(..., description="Character offset start")
    char_end: int = Field(..., description="Character offset end")
    token_count: Optional[int] = Field(None, description="Estimated token count")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary custom metadata tags")


class TextChunk(BaseModel):
    chunk_id: str = Field(..., description="Unique chunk identifier")
    text: str = Field(..., description="Normalized text segment")
    metadata: ChunkMetadata = Field(..., description="Positional and source metadata")


class EmbeddingVector(BaseModel):
    chunk_id: str = Field(..., description="Associated chunk UUID")
    vector: List[float] = Field(..., description="Dense numerical vector embedding")
    dimension: int = Field(..., description="Embedding dimension")


class RetrievedContext(BaseModel):
    chunk_id: str = Field(..., description="Retrieved chunk identifier")
    text: str = Field(..., description="Content of the retrieved chunk")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Similarity or cosine relevance score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata associated with chunk")


class RAGStatusResponse(BaseModel):
    status: str = Field("ready", description="Module initialization state")
    is_active: bool = Field(False, description="Whether active vector indexing is currently enabled")
    architecture_status: str = Field(
        "Interfaces and pipeline integration points prepared.",
        description="Detailed status"
    )
    supported_components: List[str] = Field(
        default_factory=lambda: [
            "chunker (sentence-aware)",
            "embeddings (FastEmbed BGE-small-en-v1.5 / Deterministic fallback)",
            "vector_store (InMemoryVectorStore with cosine similarity)",
            "retriever (SemanticRetriever)"
        ],
        description="Modular components defined in RAG architecture"
    )
    total_indexed_chunks: int = Field(0, description="Total chunks indexed in vector store")
    embedding_provider: Optional[str] = Field(None, description="Active embedding provider name")
    embedding_dimension: Optional[int] = Field(None, description="Embedding vector dimensionality")


class RAGIndexRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw source text to chunk and index")
    document_id: Optional[str] = Field(None, description="Unique source document ID")
    title: Optional[str] = Field(None, description="Document title")
    chunk_size: Optional[int] = Field(500, description="Target character chunk size")
    chunk_overlap: Optional[int] = Field(50, description="Sliding window character overlap")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata tags")


class RAGIndexResponse(BaseModel):
    document_id: str = Field(..., description="Indexed document UUID")
    chunks_indexed: int = Field(..., description="Number of text chunks created and embedded")
    total_vectors: int = Field(..., description="Total vectors currently residing in store")
    message: str = Field(..., description="Status summary message")


class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Semantic search query")
    top_k: Optional[int] = Field(4, ge=1, le=20, description="Maximum number of context chunks to return")
    score_threshold: Optional[float] = Field(None, ge=0.0, le=1.0, description="Minimum similarity threshold")
    document_id: Optional[str] = Field(None, description="Optional document filter")


class RAGQueryResponse(BaseModel):
    query: str = Field(..., description="Search query executed")
    count: int = Field(..., description="Number of matching contexts retrieved")
    results: List[RetrievedContext] = Field(..., description="Ranked retrieved passages")
