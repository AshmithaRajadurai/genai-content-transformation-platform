from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_context_build_api_valid():
    text = (
        "Enterprise Intelligence Briefing: AI Agent Adoption in 2026\n"
        "According to our survey of 500 enterprise CTOs, 72% of companies have deployed autonomous AI agents. "
        "Adoption of multi-agent LLM systems has reduced incident resolution time by 48%. "
        "Top challenges cited include token cost governance, prompt injection security, and data provenance."
    )
    response = client.post(
        "/api/v1/context/build",
        json={
            "source_text": text,
            "title": "Enterprise AI Agent Adoption Report",
            "target_channels": ["linkedin", "executive_summary", "presentation"],
            "audience": "Enterprise Executives and VP Engineering",
            "tone": "Strategic & Visionary",
            "language": "English",
            "detail_level": "balanced"
        }
    )
    assert response.status_code == 200
    data = response.json()

    assert data["source_title"] == "Enterprise AI Agent Adoption Report"
    assert "Enterprise AI" in data["identified_topic"]
    assert len(data["core_facts"]) >= 1
    assert len(data["channel_prompts"]) == 3
    assert "linkedin" in data["channel_prompts"]
    assert "executive_summary" in data["channel_prompts"]
    assert "presentation" in data["channel_prompts"]
    assert "72%" in data["channel_prompts"]["executive_summary"]["user_prompt"] or "48%" in data["channel_prompts"]["executive_summary"]["user_prompt"]


def test_context_build_api_short_content():
    response = client.post(
        "/api/v1/context/build",
        json={"source_text": "Short"}
    )
    assert response.status_code == 422
