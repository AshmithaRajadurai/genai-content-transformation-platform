import logging
import hashlib
import math
from abc import ABC, abstractmethod
from typing import List, Optional

from backend.app.modules.rag.schemas import EmbeddingVector, TextChunk

logger = logging.getLogger("rag_embeddings")


class BaseEmbeddingProvider(ABC):
    """Abstract interface for dense embedding generation."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generates embedding vector for a single query or text."""
        pass

    @abstractmethod
    def embed_chunks(self, chunks: List[TextChunk]) -> List[EmbeddingVector]:
        """Generates embedding vectors for a list of TextChunks."""
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """Returns embedding vector dimension."""
        pass


class FastEmbedProvider(BaseEmbeddingProvider):
    """
    Local ONNX-based embedding provider using fastembed.
    Uses 'BAAI/bge-small-en-v1.5' (384-dimension dense embeddings).
    100% free, runs locally on CPU with zero PyTorch overhead.
    """

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self._model = None
        self._dimension = 384

    def _get_model(self):
        if self._model is None:
            from fastembed import TextEmbedding
            self._model = TextEmbedding(model_name=self.model_name)
        return self._model

    def get_dimension(self) -> int:
        return self._dimension

    def embed_text(self, text: str) -> List[float]:
        if not text or not text.strip():
            return [0.0] * self._dimension
        model = self._get_model()
        generator = model.embed([text])
        emb = next(generator)
        return emb.tolist() if hasattr(emb, "tolist") else list(emb)

    def embed_chunks(self, chunks: List[TextChunk]) -> List[EmbeddingVector]:
        if not chunks:
            return []
        texts = [chunk.text for chunk in chunks]
        model = self._get_model()
        embeddings_gen = model.embed(texts)
        results: List[EmbeddingVector] = []
        for chunk, emb in zip(chunks, embeddings_gen):
            vec = emb.tolist() if hasattr(emb, "tolist") else list(emb)
            results.append(
                EmbeddingVector(
                    chunk_id=chunk.chunk_id,
                    vector=vec,
                    dimension=len(vec)
                )
            )
        return results


class DeterministicEmbeddingProvider(BaseEmbeddingProvider):
    """
    Fast, deterministic hash-based pseudo-embedding provider.
    Used for unit testing and offline fallbacks without downloading models.
    Generates normalized 384-dimensional unit vectors.
    """

    def __init__(self, dimension: int = 384):
        self._dimension = dimension

    def get_dimension(self) -> int:
        return self._dimension

    def _hash_to_vector(self, text: str) -> List[float]:
        if not text:
            return [0.0] * self._dimension

        words = text.lower().split()
        vec = [0.0] * self._dimension
        for word in words:
            h = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
            for i in range(min(16, self._dimension)):
                idx = (h + i * 31) % self._dimension
                sign = 1.0 if ((h >> i) & 1) else -1.0
                vec[idx] += sign

        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [round(x / norm, 6) for x in vec]
        return vec

    def embed_text(self, text: str) -> List[float]:
        return self._hash_to_vector(text)

    def embed_chunks(self, chunks: List[TextChunk]) -> List[EmbeddingVector]:
        return [
            EmbeddingVector(
                chunk_id=chunk.chunk_id,
                vector=self._hash_to_vector(chunk.text),
                dimension=self._dimension
            )
            for chunk in chunks
        ]


def get_embedding_provider(use_local_model: bool = True) -> BaseEmbeddingProvider:
    """Factory creating the active embedding provider."""
    if use_local_model:
        try:
            return FastEmbedProvider()
        except Exception as exc:
            logger.warning("FastEmbedProvider initialization failed (%s); using deterministic fallback.", exc)
            return DeterministicEmbeddingProvider()
    return DeterministicEmbeddingProvider()
