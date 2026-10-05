import pytest
from backend.app.models.transformation_model import TransformationPipelineRequest
from backend.app.services.transformation_service import TransformationService


def test_transformation_pipeline_end_to_end():
    source_content = (
        "CRITICAL SECURITY ADVISORY (CVE-2026-4401)\n"
        "Affected Product: Enterprise Cloud Gateway versions 4.2.0 through 4.9.1.\n"
        "A remote code execution vulnerability has been discovered in the authentication module.\n"
        "Immediate upgrade to version 4.9.2 or patch KB-89104 is required to mitigate root compromise.\n"
        "Organizations running Enterprise Cloud Gateway must apply firewall filtering on port 8443."
    )

    req = TransformationPipelineRequest(
        source_text=source_content,
        title="Emergency Cloud Gateway Security Advisory",
        target_channels=[
            "linkedin", "twitter", "advisory", "executive",
            "infographic", "presentation", "video"
        ],
        audience="DevSecOps & IT Leaders",
        tone="Urgent & Action-Oriented",
        provider="fallback"
    )

    resp = TransformationService.execute_pipeline(req)

    assert resp.transformation_id is not None
    assert resp.source_title == "Emergency Cloud Gateway Security Advisory"
    assert "Cybersecurity" in resp.nlp_analysis.topic
    assert len(resp.context_payload.channel_prompts) == 7
    assert len(resp.llm_batch_response.results) == 7
    assert len(resp.artefacts) == 7

    # Verify LinkedIn artefact
    linkedin = resp.artefacts["linkedin"]
    assert linkedin["channel_id"] == "linkedin"
    assert len(linkedin["key_takeaways"]) > 0
    assert len(linkedin["hashtags"]) > 0

    # Verify Twitter thread artefact
    twitter = resp.artefacts["twitter"]
    assert twitter["channel_id"] == "twitter"
    assert len(twitter["tweets"]) >= 3
    assert all(t["char_count"] <= 280 for t in twitter["tweets"])

    # Verify Advisory artefact
    advisory = resp.artefacts["advisory"]
    assert advisory["channel_id"] == "advisory"
    assert "CVE-2026-4401" in advisory["advisory_id"]
    assert len(advisory["mitigation_steps"]) >= 2

    # Verify Presentation artefact
    presentation = resp.artefacts["presentation"]
    assert presentation["channel_id"] == "presentation"
    assert presentation["total_slides"] == 5

    # Verify Video artefact
    video = resp.artefacts["video"]
    assert video["channel_id"] == "video"
    assert len(video["scenes"]) >= 3

    # Total tokens and execution time
    assert resp.total_tokens > 200
    assert resp.execution_time_ms > 0
