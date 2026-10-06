import math
import re
from typing import Optional
from fastapi import HTTPException, UploadFile, status

from backend.app.modules.ingestion.schemas import IngestionResponse, SourceTextInput
from backend.app.modules.ingestion.validators import validate_text_length, validate_file_metadata
from backend.app.modules.ingestion.extractors import extract_pdf, extract_docx, extract_text
from backend.app.shared.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES


class IngestionService:
    """
    Ingestion Service:
    Normalizes, sanitizes, and extracts content from text inputs and files.
    """

    ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_BYTES

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Cleans and normalizes incoming source content:
        - Replaces Windows CRLF with standard LF
        - Strips zero-width characters and unusual Unicode control codes
        - Trims trailing spaces per line
        - Collapses more than 2 consecutive blank lines
        """
        if not text:
            return ""

        # Remove zero-width spaces and BOM
        cleaned = re.sub(r"[\u200b\u200c\u200d\u200e\u200f\ufeff]", "", text)

        # Standardize line breaks
        cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

        # Trim trailing whitespace on each line
        lines = [line.rstrip() for line in cleaned.split("\n")]

        # Collapse excessive blank lines (max 2 consecutive)
        collapsed_lines = []
        blank_count = 0
        for line in lines:
            if not line:
                blank_count += 1
                if blank_count <= 2:
                    collapsed_lines.append(line)
            else:
                blank_count = 0
                collapsed_lines.append(line)

        return "\n".join(collapsed_lines).strip()

    @staticmethod
    def derive_title(content: str, filename: Optional[str] = None) -> str:
        """
        Intelligently extracts or infers a title from content (e.g. markdown '# Title') or filename.
        """
        if content:
            first_line = content.strip().split("\n")[0].strip()
            first_line_clean = re.sub(r"^#+\s*", "", first_line).strip()
            if 5 <= len(first_line_clean) <= 120 and not first_line_clean.lower().startswith("http"):
                return first_line_clean

        if filename:
            name_part = filename.rsplit(".", 1)[0]
            clean_name = re.sub(r"[-_]+", " ", name_part).strip()
            if len(clean_name) > 3:
                return clean_name.title()

        return "Ingested Source Document"

    @staticmethod
    def calculate_reading_time(word_count: int, wpm: int = 200) -> int:
        """Estimates reading time in minutes based on average reading speed."""
        if word_count <= 0:
            return 0
        return max(1, math.ceil(word_count / wpm))

    @classmethod
    def ingest_text_input(cls, payload: SourceTextInput) -> IngestionResponse:
        """
        Ingests, validates, and normalizes raw text input.
        """
        raw = validate_text_length(payload.content, min_length=5)
        cleaned = cls.normalize_text(raw)
        words = re.findall(r"\b\w+\b", cleaned)
        word_count = len(words)
        char_count = len(cleaned)

        title = payload.title or cls.derive_title(cleaned)

        return IngestionResponse(
            title=title,
            raw_content=raw,
            cleaned_content=cleaned,
            source_type=payload.source_type or "text",
            word_count=word_count,
            char_count=char_count,
            estimated_reading_time_minutes=cls.calculate_reading_time(word_count),
            mime_type="text/plain",
            message=f"Text content ingested successfully ({word_count} words)."
        )

    @classmethod
    async def ingest_uploaded_file(cls, file: UploadFile) -> IngestionResponse:
        """
        Validates, extracts text, and normalizes an uploaded file (.txt, .md, .pdf, .docx, .json, .csv).
        """
        filename = file.filename or "unknown_file.txt"
        content_bytes = await file.read()
        file_size = len(content_bytes)

        file_ext = validate_file_metadata(filename, file_size)

        if file_ext == ".pdf":
            extracted_text = extract_pdf(content_bytes)
        elif file_ext == ".docx":
            extracted_text = extract_docx(content_bytes)
        else:
            extracted_text = extract_text(content_bytes)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No readable text could be extracted from the uploaded document."
            )

        cleaned = cls.normalize_text(extracted_text)
        words = re.findall(r"\b\w+\b", cleaned)
        word_count = len(words)
        char_count = len(cleaned)

        title = cls.derive_title(cleaned, filename=filename)

        return IngestionResponse(
            title=title,
            raw_content=extracted_text,
            cleaned_content=cleaned,
            source_type=file_ext.lstrip(".") or "document",
            word_count=word_count,
            char_count=char_count,
            estimated_reading_time_minutes=cls.calculate_reading_time(word_count),
            filename=filename,
            file_size_bytes=file_size,
            mime_type=file.content_type or ALLOWED_EXTENSIONS.get(file_ext, "application/octet-stream"),
            message=f"File '{filename}' successfully ingested ({word_count} words extracted)."
        )
