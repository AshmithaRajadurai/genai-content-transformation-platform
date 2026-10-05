import pytest
from backend.app.models.storage_model import (
    TransformationRecord,
    HistoryItemSummary,
    HistoryListResponse,
    StorageHealthResponse
)


def test_transformation_record_creation():
    rec = TransformationRecord(
        transformation_id="test-trans-uuid-001",
        source_title="Advisory on Cloud Gateway",
        source_type="advisory",
        source_text="Sample text content for testing storage.",
        selected_channels=["linkedin", "advisory"],
        audience="DevOps Leads",
        tone="Urgent",
        detected_topic="Cybersecurity",
        keywords=["cloud", "cve"],
        artefacts={"linkedin": {"title": "Sample Post"}}
    )
    assert rec.transformation_id == "test-trans-uuid-001"
    assert rec.source_title == "Advisory on Cloud Gateway"
    assert len(rec.selected_channels) == 2
    assert "linkedin" in rec.artefacts


def test_history_list_response():
    resp = HistoryListResponse(
        total=1,
        database_status="connected",
        items=[
            HistoryItemSummary(
                transformation_id="uuid-123",
                source_title="Threat Report",
                detected_topic="Security",
                channels=["advisory"],
                created_at="2026-10-05T09:00:00Z",
                total_tokens=250
            )
        ]
    )
    assert resp.total == 1
    assert resp.database_status == "connected"
    assert resp.items[0].transformation_id == "uuid-123"
