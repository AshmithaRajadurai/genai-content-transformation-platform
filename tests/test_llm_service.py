import pytest
from backend.app.models.context_model import ContextBuildRequest
from backend.app.models.llm_model import LLMGenerationRequest, LLMBatchGenerationRequest
from backend.app.services.context_service import ContextService
from backend.app.services.llm_service import LLMService


def test_get_available_providers():
    providers = LLMService.get_available_providers()
    assert len(providers) >= 3
    provider_ids = [p.id for p in providers]
    assert "gemini" in provider_ids
    assert "openai" in provider_ids
    assert "fallback" in provider_ids


def test_generate_single_channel_linkedin():
    prompt = (
        "DOCUMENT TITLE: Cloud Gateway Zero-Day Notice\n"
        "IDENTIFIED TOPIC: Cybersecurity & Vulnerability Intelligence\n"
        "KEYWORDS: cve-2026-4401, cloud gateway, authentication, patch\n"
        "CORE VERIFIED FACTS:\n"
        "1. Critical authentication bypass in Enterprise Cloud Gateway v4.2.\n"
        "2. Emergency patch KB-89104 released for immediate deployment.\n\n"
        "TASK INSTRUCTION:\n"
        "Transform this verified intelligence into a publication-ready LinkedIn Thought Leadership Post."
    )
    req = LLMGenerationRequest(
        channel_id="linkedin",
        channel_name="LinkedIn Post",
        system_prompt="You are an executive security communicator.",
        user_prompt=prompt,
        provider="fallback"
    )

    resp = LLMService.generate(req)

    assert resp.channel_id == "linkedin"
    assert resp.provider == "fallback"
    assert resp.tokens_used > 50
    assert "Cloud Gateway Zero-Day Notice" in resp.content
    assert "KB-89104" in resp.content or "Enterprise Cloud Gateway" in resp.content
    assert "#" in resp.content


def test_generate_batch_end_to_end_from_context():
    raw_text = (
        "CRITICAL SECURITY ADVISORY (CVE-2026-4401)\n"
        "Affected Product: Enterprise Cloud Gateway versions 4.2.0 through 4.9.1.\n"
        "A remote code execution vulnerability has been discovered in the authentication module.\n"
        "Immediate upgrade to version 4.9.2 or patch KB-89104 is required to mitigate root compromise."
    )
    # Step 1: Context Engine
    ctx_req = ContextBuildRequest(
        source_text=raw_text,
        title="Emergency Cloud Gateway Patch Notice",
        target_channels=["linkedin", "advisory", "executive_summary"]
    )
    context_payload = ContextService.build_context(ctx_req)

    # Step 2: LLM Generation Engine
    batch_req = LLMBatchGenerationRequest(
        context_payload=context_payload,
        provider="fallback"
    )
    batch_resp = LLMService.generate_batch(batch_req)

    assert batch_resp.source_title == "Emergency Cloud Gateway Patch Notice"
    assert len(batch_resp.results) == 3
    assert "linkedin" in batch_resp.results
    assert "advisory" in batch_resp.results
    assert "executive_summary" in batch_resp.results

    advisory_content = batch_resp.results["advisory"].content
    assert "SECURITY & OPERATIONAL ADVISORY" in advisory_content
    assert "MANDATORY REMEDIATION ACTIONS" in advisory_content
    assert batch_resp.total_tokens > 150
