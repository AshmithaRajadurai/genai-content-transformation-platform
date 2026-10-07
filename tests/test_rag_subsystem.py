import uuid
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.modules.rag.chunker import TextChunker
from backend.app.modules.rag.embeddings import (
    FastEmbedProvider,
    DeterministicEmbeddingProvider,
    get_embedding_provider,
)
from backend.app.modules.rag.vector_store import InMemoryVectorStore
from backend.app.modules.rag.retriever import SemanticRetriever
from backend.app.modules.rag.service import RAGService
from backend.app.modules.rag.schemas import (
    TextChunk,
    ChunkMetadata,
    EmbeddingVector,
)
from backend.app.modules.generation.schemas import TransformationPipelineRequest
from backend.app.modules.orchestration.pipeline import TransformationPipeline

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_rag_store():
    """Ensure vector store is clean before and after each test."""
    RAGService.clear()
    yield
    RAGService.clear()


def test_rag_chunker_custom_settings():
    chunker = TextChunker()
    text = (
        "Zero-trust architecture enforces strict identity verification. "
        "Every request is authenticated and encrypted regardless of network perimeter. "
        "Micro-segmentation prevents lateral movement across enterprise assets."
    )
    chunks = chunker.chunk(text, chunk_size=80, chunk_overlap=15, document_id="doc-test-1")
    assert len(chunks) >= 2
    for idx, c in enumerate(chunks):
        assert c.chunk_id
        assert c.metadata.document_id == "doc-test-1"
        assert c.metadata.chunk_index == idx
        assert c.metadata.char_start >= 0
        assert c.metadata.char_end > c.metadata.char_start
        assert c.metadata.token_count is not None


def test_deterministic_embedding_provider():
    provider = DeterministicEmbeddingProvider(dimension=384)
    v1 = provider.embed_text("Cloud Computing Infrastructure")
    v2 = provider.embed_text("Cloud Computing Infrastructure")
    v3 = provider.embed_text("Organic Agriculture Farming")

    assert len(v1) == 384
    assert v1 == v2  # Purely deterministic
    assert v1 != v3  # Different text yields distinct vectors

    # Test embed_chunks
    chunk = TextChunk(
        chunk_id="chk-1",
        text="Cybersecurity firewall rules",
        metadata=ChunkMetadata(chunk_index=0, char_start=0, char_end=28)
    )
    vec_objs = provider.embed_chunks([chunk])
    assert len(vec_objs) == 1
    assert vec_objs[0].chunk_id == "chk-1"
    assert vec_objs[0].dimension == 384


def test_fastembed_provider():
    provider = get_embedding_provider(use_local_model=True)
    assert provider.get_dimension() == 384

    vec = provider.embed_text("Natural Language Processing for Enterprise")
    assert len(vec) == 384
    assert any(x != 0.0 for x in vec)

    batch_vecs = provider.embed_batch(["First sentence", "Second sentence"])
    assert len(batch_vecs) == 2
    assert len(batch_vecs[0]) == 384


def test_in_memory_vector_store():
    store = InMemoryVectorStore()
    assert store.count() == 0

    chunk1 = TextChunk(
        chunk_id="c1",
        text="Kubernetes orchestrates containerized workloads across server clusters.",
        metadata=ChunkMetadata(document_id="doc-k8s", chunk_index=0, char_start=0, char_end=70)
    )
    chunk2 = TextChunk(
        chunk_id="c2",
        text="Organic coffee beans are roasted at high temperatures for optimal flavor.",
        metadata=ChunkMetadata(document_id="doc-coffee", chunk_index=0, char_start=0, char_end=72)
    )

    provider = DeterministicEmbeddingProvider(dimension=384)
    v1 = provider.embed_text(chunk1.text)
    v2 = provider.embed_text(chunk2.text)

    inserted = store.upsert(
        [chunk1, chunk2],
        [
            EmbeddingVector(chunk_id="c1", vector=v1, dimension=384),
            EmbeddingVector(chunk_id="c2", vector=v2, dimension=384)
        ]
    )
    assert inserted == 2
    assert store.count() == 2

    # Query matching chunk 1
    query_vec = provider.embed_text("containers and kubernetes")
    results = store.search(query_vec, top_k=2)
    assert len(results) == 2
    assert all(0.0 <= r.relevance_score <= 1.0 for r in results)

    # Document filtering
    filtered = store.search(query_vec, top_k=2, filters={"document_id": "doc-coffee"})
    assert len(filtered) == 1
    assert filtered[0].chunk_id == "c2"

    # Deletion
    deleted = store.delete("doc-k8s")
    assert deleted is True
    assert store.count() == 1

    # Clear
    store.clear()
    assert store.count() == 0


def test_semantic_retriever():
    provider = get_embedding_provider()
    store = InMemoryVectorStore()
    retriever = SemanticRetriever(embedding_provider=provider, vector_store=store)

    # Empty store returns empty list
    empty_res = retriever.retrieve("artificial intelligence")
    assert empty_res == []

    chunk = TextChunk(
        chunk_id="ai-1",
        text="Machine learning models optimize loss functions via gradient descent.",
        metadata=ChunkMetadata(document_id="doc-ml", chunk_index=0, char_start=0, char_end=70)
    )
    vec = provider.embed_text(chunk.text)
    store.upsert([chunk], [EmbeddingVector(chunk_id="ai-1", vector=vec, dimension=len(vec))])

    matches = retriever.retrieve("machine learning optimization", top_k=1)
    assert len(matches) == 1
    assert matches[0].chunk_id == "ai-1"
    assert matches[0].relevance_score > 0.3


def test_rag_service_lifecycle():
    RAGService.clear()
    initial_status = RAGService.get_status()
    assert initial_status.status == "ready"
    assert initial_status.is_active is False
    assert initial_status.total_indexed_chunks == 0

    idx_res = RAGService.index_document(
        text=(
            "Retrieval-Augmented Generation (RAG) grounds language models in external knowledge. "
            "It reduces hallucinations and provides up-to-date domain factual grounding."
        ),
        document_id="rag-doc-test",
        title="RAG Primer"
    )
    assert idx_res.document_id == "rag-doc-test"
    assert idx_res.chunks_indexed >= 1
    assert idx_res.total_vectors >= 1

    # Status reflects indexed data
    active_status = RAGService.get_status()
    assert active_status.is_active is True
    assert active_status.total_indexed_chunks >= 1

    # Retrieve context
    retrieved = RAGService.retrieve_context("What does RAG prevent?", top_k=1)
    assert len(retrieved) >= 1
    assert "hallucinations" in retrieved[0].text or "knowledge" in retrieved[0].text
    assert 0.0 <= retrieved[0].relevance_score <= 1.0

    # Delete document
    del_ok = RAGService.delete_document("rag-doc-test")
    assert del_ok is True
    assert RAGService.count() == 0


def test_rag_api_endpoints():
    RAGService.clear()

    # 1. Check status
    res = client.get("/api/v1/rag/status")
    assert res.status_code == 200
    assert res.json()["status"] == "ready"

    # 2. Index content via POST
    index_payload = {
        "text": "Cybersecurity posture management continuously monitors cloud security drift and misconfigurations.",
        "document_id": "api-test-doc",
        "title": "CSPM Security Briefing",
        "chunk_size": 300,
        "chunk_overlap": 30,
        "metadata": {"environment": "production"}
    }
    idx_resp = client.post("/api/v1/rag/index", json=index_payload)
    assert idx_resp.status_code == 201
    idx_data = idx_resp.json()
    assert idx_data["document_id"] == "api-test-doc"
    assert idx_data["chunks_indexed"] >= 1

    # 3. Retrieve content via POST
    query_payload = {
        "query": "cloud misconfigurations and security drift",
        "top_k": 2
    }
    ret_resp = client.post("/api/v1/rag/retrieve", json=query_payload)
    assert ret_resp.status_code == 200
    ret_data = ret_resp.json()
    assert ret_data["count"] >= 1
    assert ret_data["results"][0]["metadata"]["environment"] == "production"

    # 4. Delete document
    del_resp = client.delete("/api/v1/rag/document/api-test-doc")
    assert del_resp.status_code == 200
    assert del_resp.json()["deleted"] is True

    # 5. Clear endpoint
    clear_resp = client.delete("/api/v1/rag/clear")
    assert clear_resp.status_code == 200
    assert clear_resp.json()["total_vectors"] == "0"


def test_transformation_pipeline_with_rag_enabled():
    RAGService.clear()
    pipeline_req = TransformationPipelineRequest(
        source_text=(
            "Quantum computing uses quantum bits or qubits to perform complex matrix calculations. "
            "Shor's algorithm can factor integers in polynomial time, impacting asymmetric cryptography."
        ),
        title="Quantum Computing Cryptography Impact",
        target_channels=["linkedin", "advisory"],
        use_rag=True,
        rag_top_k=2
    )
    result = TransformationPipeline.execute(pipeline_req)
    assert result.transformation_id
    assert result.source_title == "Quantum Computing Cryptography Impact"
    assert len(result.context_payload.retrieved_passages) >= 1
    assert "qubit" in result.context_payload.retrieved_passages[0].lower() or "quantum" in result.context_payload.retrieved_passages[0].lower()
    assert "linkedin" in result.artefacts
    assert "advisory" in result.artefacts
