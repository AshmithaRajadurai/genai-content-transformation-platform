from fastapi import APIRouter, HTTPException, status

from backend.app.models.context_model import ContextBuildRequest, CompiledContextPayload
from backend.app.services.context_service import ContextService

router = APIRouter(prefix="/api/v1/context", tags=["Context Engine Layer"])


@router.post(
    "/build",
    response_model=CompiledContextPayload,
    status_code=status.HTTP_200_OK,
    summary="Compile Grounded Context & Channel Prompts",
    description="Fuses source content, extracted NLP facts, audience persona, and channel guardrails into execution-ready prompts for the LLM Engine."
)
def build_context_endpoint(payload: ContextBuildRequest):
    try:
        return ContextService.build_context(payload)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Context compilation error: {str(e)}"
        )
