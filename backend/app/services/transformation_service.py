"""Compatibility re-export layer for transformation service."""
from backend.app.modules.generation.service import GenerationService
from backend.app.modules.orchestration.pipeline import TransformationPipeline
from backend.app.modules.generation.schemas import (
    LinkedInArtefact,
    TwitterArtefact,
    AdvisoryArtefact,
    ExecutiveSummaryArtefact,
    InfographicArtefact,
    PresentationArtefact,
    VideoScriptArtefact,
    TransformationPipelineRequest,
    TransformationPipelineResponse,
)
from backend.app.modules.nlp.schemas import NLPAnalysisResponse


class TransformationService:
    """Compatibility wrapper preserving TransformationService API surface."""

    @classmethod
    def structure_linkedin(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> LinkedInArtefact:
        return GenerationService.structure_linkedin(raw_text, nlp_data, title)

    @classmethod
    def structure_twitter(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> TwitterArtefact:
        return GenerationService.structure_twitter(raw_text, nlp_data, title)

    @classmethod
    def structure_advisory(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> AdvisoryArtefact:
        return GenerationService.structure_advisory(raw_text, nlp_data, title)

    @classmethod
    def structure_executive(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> ExecutiveSummaryArtefact:
        return GenerationService.structure_executive(raw_text, nlp_data, title)

    @classmethod
    def structure_infographic(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> InfographicArtefact:
        return GenerationService.structure_infographic(raw_text, nlp_data, title)

    @classmethod
    def structure_presentation(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> PresentationArtefact:
        return GenerationService.structure_presentation(raw_text, nlp_data, title)

    @classmethod
    def structure_video(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> VideoScriptArtefact:
        return GenerationService.structure_video(raw_text, nlp_data, title)

    @classmethod
    def execute_pipeline(cls, request: TransformationPipelineRequest) -> TransformationPipelineResponse:
        return TransformationPipeline.execute(request)


__all__ = ["TransformationService"]
