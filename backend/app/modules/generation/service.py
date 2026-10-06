from typing import Any, Dict
from backend.app.modules.nlp.schemas import NLPAnalysisResponse
from backend.app.modules.generation.schemas import (
    LinkedInArtefact,
    TwitterArtefact,
    AdvisoryArtefact,
    ExecutiveSummaryArtefact,
    InfographicArtefact,
    PresentationArtefact,
    VideoScriptArtefact,
)
from backend.app.modules.generation.generators import (
    structure_linkedin,
    structure_twitter,
    structure_advisory,
    structure_executive,
    structure_infographic,
    structure_presentation,
    structure_video,
)


class GenerationService:
    """
    Generative AI Formatting & Structuring Service:
    Converts LLM output text into channel-specialized, schema-validated artefacts.
    """

    @classmethod
    def structure_linkedin(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> LinkedInArtefact:
        return structure_linkedin(raw_text, nlp_data, title)

    @classmethod
    def structure_twitter(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> TwitterArtefact:
        return structure_twitter(raw_text, nlp_data, title)

    @classmethod
    def structure_advisory(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> AdvisoryArtefact:
        return structure_advisory(raw_text, nlp_data, title)

    @classmethod
    def structure_executive(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> ExecutiveSummaryArtefact:
        return structure_executive(raw_text, nlp_data, title)

    @classmethod
    def structure_infographic(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> InfographicArtefact:
        return structure_infographic(raw_text, nlp_data, title)

    @classmethod
    def structure_presentation(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> PresentationArtefact:
        return structure_presentation(raw_text, nlp_data, title)

    @classmethod
    def structure_video(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> VideoScriptArtefact:
        return structure_video(raw_text, nlp_data, title)

    @classmethod
    def format_channel(
        cls,
        channel_id: str,
        raw_text: str,
        nlp_data: NLPAnalysisResponse,
        title: str
    ) -> Dict[str, Any]:
        """Formats raw generated content into the requested channel artefact dictionary."""
        ch = channel_id.lower()
        if ch == "linkedin":
            return cls.structure_linkedin(raw_text, nlp_data, title).model_dump()
        elif ch == "twitter":
            return cls.structure_twitter(raw_text, nlp_data, title).model_dump()
        elif ch == "advisory":
            return cls.structure_advisory(raw_text, nlp_data, title).model_dump()
        elif ch in ["executive", "executive_summary"]:
            return cls.structure_executive(raw_text, nlp_data, title).model_dump()
        elif ch == "infographic":
            return cls.structure_infographic(raw_text, nlp_data, title).model_dump()
        elif ch == "presentation":
            return cls.structure_presentation(raw_text, nlp_data, title).model_dump()
        elif ch in ["video", "video_script"]:
            return cls.structure_video(raw_text, nlp_data, title).model_dump()
        return {"channel_id": channel_id, "content": raw_text}
