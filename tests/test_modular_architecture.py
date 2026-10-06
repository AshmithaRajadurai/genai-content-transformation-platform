from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.modules.rag.chunker import TextChunker
from backend.app.modules.rag.service import RAGService
from backend.app.modules.n8n.client import N8nClient
from backend.app.modules.llm.service import LLMService
from backend.app.modules.generation.generators import (
    structure_linkedin,
    structure_twitter,
    structure_advisory,
    structure_executive,
    structure_infographic,
    structure_presentation,
    structure_video,
)
from backend.app.modules.nlp.schemas import NLPAnalysisResponse, NamedEntity, KeywordItem

client = TestClient(app)


def test_rag_status_endpoint():
    response = client.get("/api/v1/rag/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["is_active"] is False
    assert len(data["supported_components"]) >= 4


def test_rag_text_chunker():
    chunker = TextChunker()
    sample_text = (
        "Paragraph 1 discusses enterprise artificial intelligence.\n\n"
        "Paragraph 2 details prompt synthesis and context compilation.\n\n"
        "Paragraph 3 covers multi-channel output generation."
    )
    chunks = chunker.chunk(sample_text, chunk_size=100, chunk_overlap=20)
    assert len(chunks) >= 2
    for chunk in chunks:
        assert chunk.chunk_id
        assert chunk.text
        assert chunk.metadata.chunk_index >= 0


def test_n8n_provider_in_llm_service():
    providers = LLMService.get_available_providers()
    provider_ids = [p.id for p in providers]
    assert "n8n" in provider_ids
    assert "gemini" in provider_ids
    assert "openai" in provider_ids
    assert "fallback" in provider_ids


def test_n8n_client_initialization():
    client_instance = N8nClient(webhook_url="http://localhost:5678/webhook/test")
    assert client_instance.is_configured() is True
    unconfigured = N8nClient(webhook_url="")
    assert unconfigured.is_configured() is False


def test_individual_generators():
    mock_nlp = NLPAnalysisResponse(
        topic="Cybersecurity & Cloud",
        topics=["Cybersecurity & Cloud"],
        content_type="Critical Security Advisory",
        detected_tone="Urgent",
        keywords=["vulnerability", "patch", "gateway"],
        keyword_items=[KeywordItem(keyword="vulnerability", relevance=0.9)],
        entities=[NamedEntity(name="Cloud Gateway", type="PRODUCT", frequency=2)],
        key_facts=["Critical vulnerability CVE-2026-1102 patched in version 2.1."],
        summary_context="Urgent security advisory regarding Cloud Gateway.",
        confidence_score=95.0
    )
    raw_text = "Headline: Critical Advisory CVE-2026-1102\n- Immediate patch required.\n#CyberSecurity"

    linkedin_artefact = structure_linkedin(raw_text, mock_nlp, "Advisory Title")
    assert linkedin_artefact.channel_id == "linkedin"
    assert linkedin_artefact.title == "Advisory Title"

    twitter_artefact = structure_twitter(raw_text, mock_nlp, "Advisory Title")
    assert twitter_artefact.channel_id == "twitter"
    assert len(twitter_artefact.tweets) >= 1

    advisory_artefact = structure_advisory(raw_text, mock_nlp, "Advisory Title")
    assert advisory_artefact.channel_id == "advisory"
    assert "CVE" in advisory_artefact.advisory_id or "ADV" in advisory_artefact.advisory_id

    exec_artefact = structure_executive(raw_text, mock_nlp, "Advisory Title")
    assert exec_artefact.channel_id == "executive"
    assert len(exec_artefact.recommendations) > 0

    info_artefact = structure_infographic(raw_text, mock_nlp, "Advisory Title")
    assert info_artefact.channel_id == "infographic"
    assert len(info_artefact.sections) == 3

    pres_artefact = structure_presentation(raw_text, mock_nlp, "Advisory Title")
    assert pres_artefact.channel_id == "presentation"
    assert pres_artefact.total_slides == 5

    video_artefact = structure_video(raw_text, mock_nlp, "Advisory Title")
    assert video_artefact.channel_id == "video"
    assert len(video_artefact.scenes) == 4
