from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_nlp_analyze_api_valid():
    content = (
        "CRITICAL SECURITY ADVISORY (CVE-2026-4401)\n"
        "Affected Product: Enterprise Cloud Gateway versions 4.2.0 through 4.9.1.\n"
        "A remote code execution vulnerability has been discovered in the authentication module.\n"
        "Immediate upgrade to version 4.9.2 or patch KB-89104 is required to mitigate root compromise."
    )
    response = client.post(
        "/api/v1/nlp/analyze",
        json={"content": content, "source_type": "advisory"}
    )
    assert response.status_code == 200
    data = response.json()

    assert "Cybersecurity" in data["topic"]
    assert "Critical Security Advisory" in data["content_type"]
    assert "Urgent & Action-Oriented" in data["detected_tone"]
    assert len(data["keywords"]) > 0
    assert len(data["entities"]) > 0
    assert len(data["key_facts"]) > 0
    assert data["confidence_score"] >= 85.0
    assert "CVE-2026-4401" in [e["name"] for e in data["entities"]]


def test_nlp_analyze_api_short_content():
    response = client.post(
        "/api/v1/nlp/analyze",
        json={"content": "Too short"}
    )
    assert response.status_code == 422
