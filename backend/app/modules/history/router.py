from fastapi import APIRouter, HTTPException, Query, status

from backend.app.modules.history.schemas import (
    TransformationRecord,
    HistoryListResponse,
    StorageHealthResponse,
)
from backend.app.modules.history.service import HistoryService

router = APIRouter(prefix="/api/v1/history", tags=["Storage & History"])


@router.get("", response_model=HistoryListResponse)
def list_history(
    limit: int = Query(20, ge=1, le=100, description="Page limit"),
    skip: int = Query(0, ge=0, description="Offset items")
):
    """
    Returns paginated list of past transformation summaries from MongoDB or fallback cache.
    """
    return HistoryService.list_history(limit=limit, skip=skip)


@router.get("/storage/health", response_model=StorageHealthResponse)
def get_storage_health():
    """
    Returns connection and collection health metrics for the MongoDB storage layer.
    """
    return HistoryService.get_health()


@router.get("/{transformation_id}", response_model=TransformationRecord)
def get_transformation_detail(transformation_id: str):
    """
    Retrieves full transformation record including NLP facts and all generated multi-channel artefacts.
    """
    record = HistoryService.get_transformation(transformation_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transformation with ID '{transformation_id}' not found."
        )
    return record


@router.delete("/{transformation_id}")
def delete_transformation_record(transformation_id: str):
    """
    Deletes a transformation record by ID from MongoDB Atlas and local session cache.
    """
    record = HistoryService.get_transformation(transformation_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transformation with ID '{transformation_id}' not found."
        )

    HistoryService.delete_transformation(transformation_id)
    return {
        "success": True,
        "message": f"Transformation '{transformation_id}' deleted successfully.",
        "transformation_id": transformation_id
    }
