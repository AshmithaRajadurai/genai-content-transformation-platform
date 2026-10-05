import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.models.storage_model import TransformationRecord
from backend.app.services.storage_service import StorageService

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_storage():
    StorageService.clear_memory_buffer()
    yield
    StorageService.clear_memory_buffer()


def test_get_history_empty():
    response = client.get("/api/v1/history")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "database_status" in data
    assert "items" in data
    assert isinstance(data["items"], list)


def test_get_storage_health():
    response = client.get("/api/v1/history/storage/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["connected", "disconnected"]
    assert data["database"] == "genai_content_platform"
    assert "record_count" in data


def test_get_and_delete_transformation_record():
    rec = TransformationRecord(
        transformation_id="hist-route-test-1",
        source_title="Incident Report: Microservices Latency",
        source_type="text",
        source_text="Network packet loss triggered queue build-up in downstream services.",
        selected_channels=["linkedin", "twitter"],
        detected_topic="Site Reliability",
        keywords=["Latency", "Packet Loss", "Reliability"],
        entities_count=3,
        key_facts_count=2,
        artefacts={"linkedin": {"title": "Incident Post"}},
        total_tokens=180
    )
    StorageService.save_transformation(rec)

    # Fetch detail
    get_res = client.get("/api/v1/history/hist-route-test-1")
    assert get_res.status_code == 200
    detail = get_res.json()
    assert detail["transformation_id"] == "hist-route-test-1"
    assert detail["source_title"] == "Incident Report: Microservices Latency"
    assert detail["detected_topic"] == "Site Reliability"

    # Delete record
    del_res = client.delete("/api/v1/history/hist-route-test-1")
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Confirm 404 after deletion
    not_found_res = client.get("/api/v1/history/hist-route-test-1")
    assert not_found_res.status_code == 404


def test_get_nonexistent_transformation():
    response = client.get("/api/v1/history/non-existent-uuid")
    assert response.status_code == 404


def test_delete_nonexistent_transformation():
    response = client.delete("/api/v1/history/non-existent-uuid")
    assert response.status_code == 404


def test_e2e_pipeline_persists_to_history_route():
    payload = {
        "source_text": "Quantum computing harnesses superposition and entanglement to solve intractable optimization problems.",
        "title": "Quantum Computing Primer",
        "source_type": "text",
        "target_channels": ["linkedin"],
        "provider": "heuristic"
    }
    tx_res = client.post("/api/v1/transform/execute", json=payload)
    assert tx_res.status_code == 200
    tx_data = tx_res.json()
    created_id = tx_data["transformation_id"]

    # History API should list it
    hist_res = client.get("/api/v1/history")
    assert hist_res.status_code == 200
    items = hist_res.json()["items"]
    ids = [it["transformation_id"] for it in items]
    assert created_id in ids
