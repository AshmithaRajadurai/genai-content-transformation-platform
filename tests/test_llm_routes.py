from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_get_providers_api():
    response = client.get("/api/v1/llm/providers")
    assert response.status_code == 200
    providers = response.json()
    assert len(providers) >= 3
    ids = [p["id"] for p in providers]
    assert "gemini" in ids
    assert "fallback" in ids


def test_generate_single_api():
    response = client.post(
        "/api/v1/llm/generate",
        json={
            "channel_id": "linkedin",
            "channel_name": "LinkedIn Post",
            "system_prompt": "You are a communication expert.",
            "user_prompt": (
                "DOCUMENT TITLE: Incident Report 2026\n"
                "IDENTIFIED TOPIC: Cloud Infrastructure\n"
                "KEYWORDS: cloud, uptime, recovery\n"
                "CORE VERIFIED FACTS:\n"
                "1. Core services restored in under 4 minutes.\n"
                "2. Zero customer data lost during failover.\n\n"
                "TASK INSTRUCTION: Transform into LinkedIn Post."
            ),
            "provider": "fallback"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["channel_id"] == "linkedin"
    assert data["provider"] == "fallback"
    assert len(data["content"]) > 30
    assert "Incident Report 2026" in data["content"]


def test_generate_batch_api():
    # First build context
    ctx_res = client.post(
        "/api/v1/context/build",
        json={
            "source_text": (
                "CRITICAL SECURITY ADVISORY (CVE-2026-4401)\n"
                "Affected Product: Enterprise Cloud Gateway versions 4.2.0 through 4.9.1.\n"
                "A remote code execution vulnerability has been discovered in the authentication module.\n"
                "Immediate upgrade to version 4.9.2 or patch KB-89104 is required to mitigate root compromise."
            ),
            "target_channels": ["linkedin", "advisory"]
        }
    )
    assert ctx_res.status_code == 200
    context_payload = ctx_res.json()

    # Now call batch generation
    batch_res = client.post(
        "/api/v1/llm/generate-batch",
        json={
            "context_payload": context_payload,
            "provider": "fallback"
        }
    )
    assert batch_res.status_code == 200
    data = batch_res.json()
    assert "results" in data
    assert "linkedin" in data["results"]
    assert "advisory" in data["results"]
    assert data["total_tokens"] > 0
    assert "SECURITY & OPERATIONAL ADVISORY" in data["results"]["advisory"]["content"]
