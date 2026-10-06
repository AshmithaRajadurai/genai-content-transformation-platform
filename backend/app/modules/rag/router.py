from fastapi import APIRouter, status

from backend.app.modules.rag.schemas import RAGStatusResponse
from backend.app.modules.rag.service import RAGService

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
