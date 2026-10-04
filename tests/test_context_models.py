import pytest
from backend.app.models.context_model import (
    ChannelInstruction,
    ContextBuildRequest,
    ChannelContextPrompt,
    CompiledContextPayload
)
from backend.app.models.nlp_model import NamedEntity, NLPAnalysisResponse


def test_context_build_request_defaults():
    req = ContextBuildRequest(source_text="This is a test source document that is long enough for context.")
    assert req.target_channels == ["linkedin", "executive_summary"]
    assert req.audience == "General Enterprise & Technical Leaders"
    assert req.language == "English"
    assert req.detail_level == "balanced"
    assert req.nlp_analysis is None


def test_compiled_context_payload():
    prompt = ChannelContextPrompt(
        channel_id="linkedin",
        channel_name="LinkedIn Post",
        system_prompt="You are an expert executive communication strategist.",
        user_prompt="Transform the following context into a LinkedIn post.",
        grounding_rules=["Do not hallucinate CVEs."]
    )
    payload = CompiledContextPayload(
        source_title="Cloud Security Update",
        source_type="advisory",
        identified_topic="Cloud Security",
        core_facts=["Critical vulnerability discovered in Cloud Gateway."],
        guaranteed_entities=[NamedEntity(name="Cloud Gateway", type="PRODUCT", frequency=2)],
        salient_keywords=["cloud", "vulnerability", "patch"],
        context_summary="Summary of cloud vulnerability.",
        audience_persona="Executive",
        tone_guideline="Professional",
        language="English",
        detail_level="balanced",
        global_system_instruction="Strict factual adherence.",
        channel_prompts={"linkedin": prompt}
    )
    assert payload.source_title == "Cloud Security Update"
    assert "linkedin" in payload.channel_prompts
    assert payload.channel_prompts["linkedin"].channel_id == "linkedin"
