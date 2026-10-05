from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_transform_execute_api_success():
    payload = {
        "source_text": (
            "CRITICAL SECURITY ADVISORY (CVE-2026-4401)\n"
            "Affected Product: Enterprise Cloud Gateway versions 4.2.0 through 4.9.1.\n"
            "A remote code execution vulnerability has been discovered in the authentication module.\n"
            "Immediate upgrade to version 4.9.2 or patch KB-89104 is required to mitigate root compromise."
        ),
        "title": "Cloud Gateway Patch Advisory",
        "target_channels": ["linkedin", "advisory", "executive"],
        "audience": "Enterprise Executives and CISOs",
        "tone": "Urgent & Action-Oriented",
        "provider": "fallback"
    }

    response = client.post("/api/v1/transform/execute", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["transformation_id"] is not None
    assert data["source_title"] == "Cloud Gateway Patch Advisory"
    assert "Cybersecurity" in data["nlp_analysis"]["topic"]
    assert "linkedin" in data["artefacts"]
    assert "advisory" in data["artefacts"]
    assert "executive" in data["artefacts"]
    assert data["total_tokens"] > 0
    assert data["execution_time_ms"] > 0


def test_transform_execute_api_invalid_content():
    response = client.post(
        "/api/v1/transform/execute",
        json={"source_text": "Short"}
    )
    assert response.status_code == 422
