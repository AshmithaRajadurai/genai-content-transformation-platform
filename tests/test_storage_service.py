import pytest
from backend.app.models.storage_model import TransformationRecord
from backend.app.models.transformation_model import TransformationPipelineRequest
from backend.app.services.storage_service import StorageService
from backend.app.services.transformation_service import TransformationService


@pytest.fixture(autouse=True)
def clean_storage():
    StorageService.clear_memory_buffer()
    yield
    StorageService.clear_memory_buffer()


def test_storage_service_save_and_get():
    record = TransformationRecord(
        transformation_id="test-uuid-1234",
        source_title="Cloud Security Best Practices",
        source_type="advisory",
        source_text="Cloud security requires rigorous IAM policies, MFA, and continuous monitoring.",
        selected_channels=["linkedin", "twitter"],
        detected_topic="Cloud Security",
        keywords=["IAM", "MFA", "Security"],
        entities_count=3,
        key_facts_count=2,
        artefacts={"linkedin": {"title": "Cloud Security"}},
        total_tokens=250,
        execution_time_ms=45.2
    )

    saved = StorageService.save_transformation(record)
    assert saved.transformation_id == "test-uuid-1234"

    fetched = StorageService.get_transformation("test-uuid-1234")
    assert fetched is not None
    assert fetched.transformation_id == "test-uuid-1234"
    assert fetched.source_title == "Cloud Security Best Practices"
    assert fetched.detected_topic == "Cloud Security"
    assert "linkedin" in fetched.selected_channels


def test_storage_service_list_history():
    for i in range(3):
        rec = TransformationRecord(
            transformation_id=f"tx-id-{i}",
            source_title=f"Security Alert {i}",
            source_type="text",
            source_text=f"Details for alert {i}",
            selected_channels=["advisory"],
            detected_topic="Cybersecurity",
            total_tokens=100 * (i + 1)
        )
        StorageService.save_transformation(rec)

    history = StorageService.list_history(limit=10, skip=0)
    assert history.total >= 3
    assert len(history.items) >= 3
    found_ids = [item.transformation_id for item in history.items]
    assert "tx-id-0" in found_ids
    assert "tx-id-1" in found_ids
    assert "tx-id-2" in found_ids


def test_storage_service_delete():
    rec = TransformationRecord(
        transformation_id="del-uuid-99",
        source_title="To Delete",
        source_type="text",
        source_text="Temporary text"
    )
    StorageService.save_transformation(rec)
    assert StorageService.get_transformation("del-uuid-99") is not None

    deleted = StorageService.delete_transformation("del-uuid-99")
    assert deleted is True
    assert StorageService.get_transformation("del-uuid-99") is None


def test_storage_health():
    health = StorageService.get_health()
    assert health.status in ["connected", "disconnected"]
    assert health.database == "genai_content_platform"
    assert isinstance(health.record_count, int)


def test_pipeline_execution_automatically_persists():
    request = TransformationPipelineRequest(
        source_text="Zero Trust architecture enforces strict verification for every user and device accessing private resources.",
        title="Zero Trust Guidelines",
        source_type="text",
        target_channels=["linkedin"],
        provider="heuristic"
    )
    result = TransformationService.execute_pipeline(request)
    assert result.transformation_id

    # Verify stored in StorageService
    stored = StorageService.get_transformation(result.transformation_id)
    assert stored is not None
    assert stored.transformation_id == result.transformation_id
    assert stored.source_title == "Zero Trust Guidelines"
    assert "linkedin" in stored.selected_channels
