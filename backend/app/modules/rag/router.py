import logging
from typing import Any, Dict
from fastapi import APIRouter, HTTPException, status

from backend.app.modules.rag.schemas import (
    RAGIndexRequest,
    RAGIndexResponse,
    RAGQueryRequest,
    RAGQueryResponse,
    RAGStatusResponse,
)
from backend.app.modules.rag.service import RAGService

logger = logging.getLogger("rag_router")

router = APIRouter(prefix="/api/v1/rag", tags=["RAG (Retrieval-Augmented Generation) Layer"])


@router.get(
    "/status",
    response_model=RAGStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get RAG Subsystem Status",
    description="Returns current initialization and architecture readiness status for the RAG subsystem."
)
def get_rag_status():
    return RAGService.get_status()


@router.post(
    "/index",
    response_model=RAGIndexResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Index Document into Vector Store",
    description="Splits document text into semantic chunks, generates dense vector embeddings, and stores them in the in-memory vector store."
)
def index_document(request: RAGIndexRequest):
    try:
        return RAGService.index_document(
            text=request.text,
            document_id=request.document_id,
            title=request.title,
            chunk_size=request.chunk_size or 500,
            chunk_overlap=request.chunk_overlap or 50,
            metadata=request.metadata,
        )
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )
    except Exception as exc:
        logger.error("Failed to index document: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector indexing error: {str(exc)}"
        )


@router.post(
    "/retrieve",
    response_model=RAGQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Semantic Context Retrieval",
    description="Retrieves top-k context passages most relevant to the query based on cosine similarity."
)
def retrieve_context(request: RAGQueryRequest):
    try:
        results = RAGService.retrieve_context(
            query=request.query,
            top_k=request.top_k or 4,
            score_threshold=request.score_threshold,
            document_id=request.document_id,
        )
        return RAGQueryResponse(
            query=request.query,
            count=len(results),
            results=results
        )
    except Exception as exc:
        logger.error("Failed to retrieve context: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Context retrieval error: {str(exc)}"
        )


@router.delete(
    "/clear",
    status_code=status.HTTP_200_OK,
    summary="Clear Vector Store",
    description="Clears all indexed chunks and embeddings from the vector store."
)
def clear_vector_store() -> Dict[str, str]:
    RAGService.clear()
    return {"message": "Vector store successfully cleared", "total_vectors": "0"}


@router.delete(
    "/document/{document_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Document Chunks",
    description="Removes all indexed chunks and vectors for a specific document."
)
def delete_document(document_id: str) -> Dict[str, Any]:
    deleted = RAGService.delete_document(document_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{document_id}' not found in vector store."
        )
    return {"document_id": document_id, "deleted": True}
