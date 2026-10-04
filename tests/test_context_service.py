import pytest
from backend.app.models.context_model import ContextBuildRequest
from backend.app.models.nlp_model import NLPAnalysisResponse, NamedEntity, KeywordItem
from backend.app.services.context_service import ContextService


@pytest.fixture
def sample_nlp_response():
    return NLPAnalysisResponse(
        topic="Cybersecurity & Vulnerability Intelligence",
        topics=["Cybersecurity & Vulnerability Intelligence"],
        content_type="Security Advisory",
        detected_tone="Urgent & Action-Oriented",
        keywords=["vulnerability", "cloud gateway", "cve-2026-4401", "authentication"],
        keyword_items=[
            KeywordItem(keyword="vulnerability", relevance=0.95),
            KeywordItem(keyword="cloud gateway", relevance=0.88)
        ],
        entities=[
            NamedEntity(name="CVE-2026-4401", type="VULNERABILITY", frequency=3),
            NamedEntity(name="Cloud Gateway", type="PRODUCT", frequency=2)
        ],
        key_facts=[
            "Critical authentication bypass flaw in Cloud Gateway version 3.2.",
            "CVSS base score rated at 9.8 out of 10.0.",
            "Official emergency patch v3.2.4 released by security team."
        ],
        summary_context="Critical vulnerability CVE-2026-4401 affects Cloud Gateway version 3.2.",
        confidence_score=94.5
    )


def test_build_context_with_precomputed_nlp(sample_nlp_response):
    req = ContextBuildRequest(
        source_text="Sample text content for security advisory.",
        title="Emergency Security Notice",
        nlp_analysis=sample_nlp_response,
        target_channels=["linkedin", "twitter", "advisory", "executive_summary"],
        audience="DevOps and Security Engineers",
        tone="Urgent & Technical",
        language="English",
        detail_level="comprehensive"
    )

    payload = ContextService.build_context(req)

    assert payload.source_title == "Emergency Security Notice"
    assert payload.identified_topic == "Cybersecurity & Vulnerability Intelligence"
    assert len(payload.core_facts) == 3
    assert len(payload.guaranteed_entities) == 2
    assert "CVE-2026-4401" in payload.global_system_instruction
    assert set(payload.channel_prompts.keys()) == {"linkedin", "twitter", "advisory", "executive_summary"}

    linkedin_prompt = payload.channel_prompts["linkedin"]
    assert "LinkedIn" in linkedin_prompt.channel_name
    assert "CVE-2026-4401" in linkedin_prompt.user_prompt
    assert any("CVE-2026-4401" in rule for rule in linkedin_prompt.grounding_rules)


def test_build_context_without_precomputed_nlp():
    raw_text = (
        "# Urgent Threat Intelligence: Active Zero-Day in Edge Routers\n\n"
        "Security researchers have discovered CVE-2026-9901 affecting EdgeOS devices. "
        "Threat actors are actively scanning enterprise networks to exploit unauthenticated remote code execution. "
        "Organizations running EdgeOS version 4.1 or earlier must apply immediate perimeter firewall filtering."
    )
    req = ContextBuildRequest(
        source_text=raw_text,
        target_channels=["advisory", "twitter"]
    )

    payload = ContextService.build_context(req)

    assert "Edge Routers" in payload.source_title or "Threat" in payload.source_title
    assert len(payload.core_facts) >= 1
    assert "advisory" in payload.channel_prompts
    assert "twitter" in payload.channel_prompts
    assert "CVE-2026-9901" in payload.channel_prompts["advisory"].user_prompt


def test_all_seven_channels_supported(sample_nlp_response):
    all_channels = [
        "linkedin", "twitter", "advisory", "executive_summary",
        "infographic", "presentation", "video_script"
    ]
    req = ContextBuildRequest(
        source_text="Sample text content.",
        title="Universal Transformation Test",
        nlp_analysis=sample_nlp_response,
        target_channels=all_channels
    )

    payload = ContextService.build_context(req)

    assert len(payload.channel_prompts) == 7
    for ch in all_channels:
        assert ch in payload.channel_prompts
        prompt = payload.channel_prompts[ch]
        assert len(prompt.system_prompt) > 50
        assert len(prompt.user_prompt) > 50
        assert len(prompt.grounding_rules) >= 2
