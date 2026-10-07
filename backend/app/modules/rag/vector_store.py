from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set
import numpy as np

from backend.app.modules.rag.schemas import EmbeddingVector, RetrievedContext, TextChunk


class BaseVectorStore(ABC):
    """Abstract interface for vector database storage and similarity indexing."""

    @abstractmethod
    def upsert(self, chunks: List[TextChunk], vectors: List[EmbeddingVector]) -> int:
        """Stores chunks alongside their embedding vectors. Returns count inserted."""
        pass

    @abstractmethod
    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filters: Optional[dict] = None
    ) -> List[RetrievedContext]:
        """Performs nearest-neighbor similarity search."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Returns total vector records stored."""
        pass

    @abstractmethod
    def delete(self, document_id: str) -> bool:
        """Deletes all chunks belonging to a document."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clears all indexed chunks and vectors."""
        pass


class InMemoryVectorStore(BaseVectorStore):
    """
    In-memory vector store utilizing NumPy for fast vectorized cosine similarity.
    Requires no external daemon or heavyweight database; 100% self-contained and local.
    """

    def __init__(self) -> None:
        self._chunks: Dict[str, TextChunk] = {}
        self._vectors: Dict[str, np.ndarray] = {}
        self._doc_to_chunk_ids: Dict[str, Set[str]] = {}

    def upsert(self, chunks: List[TextChunk], vectors: List[EmbeddingVector]) -> int:
        """
        Stores chunks alongside their embedding vectors.
        Normalizes vectors upon insertion for rapid unit-vector cosine similarity.
        """
        if len(chunks) != len(vectors):
            raise ValueError(
                f"Chunks count ({len(chunks)}) must match vectors count ({len(vectors)})"
            )

        inserted_count = 0
        for chunk, vec_obj in zip(chunks, vectors):
            vec_arr = np.array(vec_obj.vector, dtype=np.float32)
            norm = np.linalg.norm(vec_arr)
            if norm > 1e-8:
                vec_arr = vec_arr / norm

            self._chunks[chunk.chunk_id] = chunk
            self._vectors[chunk.chunk_id] = vec_arr

            doc_id = chunk.metadata.document_id
            if doc_id:
                if doc_id not in self._doc_to_chunk_ids:
                    self._doc_to_chunk_ids[doc_id] = set()
                self._doc_to_chunk_ids[doc_id].add(chunk.chunk_id)

            inserted_count += 1

        return inserted_count

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filters: Optional[dict] = None
    ) -> List[RetrievedContext]:
        """
        Performs nearest-neighbor similarity search using cosine similarity.
        Clamps scores between 0.0 and 1.0.
        """
        if not self._chunks or not self._vectors:
            return []

        q_vec = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)
        if q_norm > 1e-8:
            q_vec = q_vec / q_norm

        target_chunk_ids: List[str] = []
        for chunk_id, chunk in self._chunks.items():
            if filters:
                match = True
                for k, v in filters.items():
                    if k == "document_id":
                        if chunk.metadata.document_id != v:
                            match = False
                            break
                    else:
                        custom_meta = chunk.metadata.metadata or {}
                        if custom_meta.get(k) != v:
                            match = False
                            break
                if not match:
                    continue
            target_chunk_ids.append(chunk_id)

        if not target_chunk_ids:
            return []

        # Vectorized dot product (cosine similarity because vectors are normalized)
        matrix = np.stack([self._vectors[cid] for cid in target_chunk_ids], axis=0)
        scores = np.dot(matrix, q_vec)

        # Pair scores with chunk ids
        scored_pairs = list(zip(target_chunk_ids, scores))
        scored_pairs.sort(key=lambda item: float(item[1]), reverse=True)

        results: List[RetrievedContext] = []
        for chunk_id, raw_score in scored_pairs[:top_k]:
            chunk = self._chunks[chunk_id]
            # Clamp similarity score to valid schema range [0.0, 1.0]
            clamped_score = max(0.0, min(1.0, float(raw_score)))

            metadata_dict: Dict[str, Any] = {
                "document_id": chunk.metadata.document_id,
                "chunk_index": chunk.metadata.chunk_index,
                "char_start": chunk.metadata.char_start,
                "char_end": chunk.metadata.char_end,
                "token_count": chunk.metadata.token_count,
            }
            if chunk.metadata.metadata:
                metadata_dict.update(chunk.metadata.metadata)

            results.append(
                RetrievedContext(
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    relevance_score=round(clamped_score, 4),
                    metadata=metadata_dict
                )
            )

        return results

    def count(self) -> int:
        """Returns total vector records stored."""
        return len(self._chunks)

    def delete(self, document_id: str) -> bool:
        """Deletes all chunks belonging to a document."""
        chunk_ids = self._doc_to_chunk_ids.pop(document_id, None)
        if not chunk_ids:
            return False

        for cid in chunk_ids:
            self._chunks.pop(cid, None)
            self._vectors.pop(cid, None)

        return True

    def clear(self) -> None:
        """Clears all indexed chunks and vectors."""
        self._chunks.clear()
        self._vectors.clear()
        self._doc_to_chunk_ids.clear()
