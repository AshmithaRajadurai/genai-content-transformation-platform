import re
import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from backend.app.modules.rag.schemas import ChunkMetadata, TextChunk


class BaseChunker(ABC):
    """Abstract chunker interface for breaking text into semantic segments."""

    @abstractmethod
    def chunk(
        self,
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        document_id: Optional[str] = None
    ) -> List[TextChunk]:
        pass


class TextChunker(BaseChunker):
    """Clean sliding-window text chunker with paragraph and sentence preservation."""

    def chunk(
        self,
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        document_id: Optional[str] = None
    ) -> List[TextChunk]:
        if not text or not text.strip():
            return []

        cleaned = text.strip()
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", cleaned) if p.strip()]
        chunks: List[TextChunk] = []
        current_text = ""
        char_offset = 0
        chunk_idx = 0

        for para in paragraphs:
            if len(current_text) + len(para) <= chunk_size:
                current_text = f"{current_text}\n\n{para}".strip()
            else:
                if current_text:
                    c_id = str(uuid.uuid4())
                    start = cleaned.find(current_text, char_offset)
                    if start == -1:
                        start = char_offset
                    end = start + len(current_text)
                    char_offset = max(0, end - chunk_overlap)

                    chunks.append(TextChunk(
                        chunk_id=c_id,
                        text=current_text,
                        metadata=ChunkMetadata(
                            document_id=document_id,
                            chunk_index=chunk_idx,
                            char_start=start,
                            char_end=end,
                            token_count=len(current_text.split())
                        )
                    ))
                    chunk_idx += 1
                current_text = para

        if current_text:
            c_id = str(uuid.uuid4())
            start = cleaned.find(current_text, char_offset)
            if start == -1:
                start = char_offset
            end = start + len(current_text)
            chunks.append(TextChunk(
                chunk_id=c_id,
                text=current_text,
                metadata=ChunkMetadata(
                    document_id=document_id,
                    chunk_index=chunk_idx,
                    char_start=start,
                    char_end=end,
                    token_count=len(current_text.split())
                )
            ))

        return chunks
