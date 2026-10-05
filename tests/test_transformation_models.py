import pytest
from backend.app.models.transformation_model import (
    LinkedInArtefact,
    TwitterArtefact,
    TweetItem,
    AdvisoryArtefact,
    ExecutiveSummaryArtefact,
    InfographicArtefact,
    InfographicSection,
    PresentationArtefact,
    SlideItem,
    VideoScriptArtefact,
    VideoScene,
    TransformationPipelineRequest,
    TransformationPipelineResponse
)
from backend.app.models.nlp_model import NLPAnalysisResponse
from backend.app.models.context_model import CompiledContextPayload, ChannelContextPrompt
from backend.app.models.llm_model import LLMBatchGenerationResponse, LLMGenerationResponse


def test_linkedin_artefact():
    art = LinkedInArtefact(
        title="Zero-Day in Enterprise Gateway",
        hook="Urgent security notification for cloud infrastructure leaders.",
        content="Full post content details...",
        key_takeaways=["Apply patch KB-89104", "Restrict port 8443"],
        hashtags=["#Cybersecurity", "#CloudSecurity"],
        estimated_read_time="1 min read"
    )
    assert art.channel_id == "linkedin"
    assert len(art.key_takeaways) == 2
    assert len(art.hashtags) == 2


def test_advisory_artefact():
    art = AdvisoryArtefact(
        advisory_id="ADV-2026-4401",
        severity="CRITICAL",
        title="Remote Code Execution in Authentication Module",
        impact="Allows unauthenticated remote code execution with root privileges.",
        affected_systems=["Enterprise Cloud Gateway v4.2.0 - v4.9.1"],
        mitigation_steps=["Upgrade to v4.9.2 immediately"],
        monitoring_actions=["Inspect /api/v2/auth/token POST requests"],
        references=["CVE-2026-4401"]
    )
    assert art.channel_id == "advisory"
    assert art.advisory_id == "ADV-2026-4401"
    assert "Root" in art.impact.title()


def test_pipeline_request_defaults():
    req = TransformationPipelineRequest(source_text="Test source text long enough for processing.")
    assert len(req.target_channels) == 7
    assert req.provider == "auto"
    assert "linkedin" in req.target_channels
    assert "video" in req.target_channels
