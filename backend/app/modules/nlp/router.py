from fastapi import APIRouter, status

from backend.app.modules.nlp.schemas import NLPAnalysisRequest, NLPAnalysisResponse
from backend.app.modules.nlp.service import NLPService

router = APIRouter(prefix="/api/v1/nlp", tags=["NLP Analysis Layer"])


@router.post(
    "/analyze",
    response_model=NLPAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Source Content via NLP",
    description="Performs topic identification, keyword extraction, named entity recognition (NER), tone detection, and key factual assertion extraction."
)
def analyze_nlp_endpoint(payload: NLPAnalysisRequest):
    return NLPService.analyze(payload)
