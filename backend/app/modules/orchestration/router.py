from fastapi import APIRouter, HTTPException, status

from backend.app.modules.generation.schemas import (
    TransformationPipelineRequest,
    TransformationPipelineResponse,
)
from backend.app.modules.orchestration.pipeline import TransformationPipeline

router = APIRouter(prefix="/api/v1/transform", tags=["Transformation Orchestration Pipeline"])


@router.post(
    "/execute",
    response_model=TransformationPipelineResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute Full Multi-Channel Transformation Pipeline",
    description="Orchestrates the complete pipeline: Source Ingestion → NLP Analysis → Context Engine → LLM Generation → Schema Structuring into 7 validated multi-channel artefacts."
)
def execute_pipeline_endpoint(payload: TransformationPipelineRequest):
    try:
        return TransformationPipeline.execute(payload)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transformation Pipeline Error: {str(e)}"
        )
