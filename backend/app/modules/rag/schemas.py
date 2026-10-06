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
        "Interfaces and pipeline integration points prepared. Vector store implementation scheduled for next phase.",
        description="Detailed status"
    )
    supported_components: List[str] = Field(
        default_factory=lambda: [
            "chunker (sentence-aware)",
            "embeddings_interface",
            "vector_store_interface",
            "retriever_interface"
        ],
        description="Modular components defined in RAG architecture"
    )
