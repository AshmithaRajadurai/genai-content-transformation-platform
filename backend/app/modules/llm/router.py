from typing import List
from fastapi import APIRouter, HTTPException, status

from backend.app.modules.llm.schemas import (
    LLMProviderInfo,
    LLMGenerationRequest,
    LLMGenerationResponse,
    LLMBatchGenerationRequest,
    LLMBatchGenerationResponse,
)
from backend.app.modules.llm.service import LLMService

router = APIRouter(prefix="/api/v1/llm", tags=["LLM Engine Layer"])


@router.get(
    "/providers",
    response_model=List[LLMProviderInfo],
    status_code=status.HTTP_200_OK,
    summary="List Available LLM Providers",
    description="Returns configuration status for supported LLM providers (Gemini, OpenAI, Local Fallback, n8n Orchestrator)."
)
def get_providers_endpoint():
    return LLMService.get_available_providers()


@router.post(
    "/generate",
    response_model=LLMGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Single Channel LLM Content",
    description="Executes grounded LLM generation for a single target channel using supplied system and user prompts."
)
def generate_single_endpoint(payload: LLMGenerationRequest):
    try:
        return LLMService.generate(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM Generation Error: {str(e)}"
        )


@router.post(
    "/generate-batch",
    response_model=LLMBatchGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Batch Generate All Requested Channel Artefacts",
    description="Accepts a CompiledContextPayload from the Context Engine and executes grounded generation for all requested channels."
)
def generate_batch_endpoint(payload: LLMBatchGenerationRequest):
    try:
        return LLMService.generate_batch(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM Batch Generation Error: {str(e)}"
        )
