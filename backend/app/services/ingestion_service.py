import io
import math
import re
from typing import Optional
from fastapi import HTTPException, UploadFile, status

from backend.app.models.source_model import IngestionResponse, SourceTextInput

# Configuration Limits
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".json": "application/json",
    ".csv": "text/csv"
}


class IngestionService:
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
        raw = payload.content.strip()
        if len(raw) < 5:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Source content too short. Please provide at least 5 characters."
            )

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
        file_ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

        if file_ext not in ALLOWED_EXTENSIONS:
            allowed = ", ".join(ALLOWED_EXTENSIONS.keys())
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file type '{file_ext}'. Allowed formats: {allowed}"
            )

        content_bytes = await file.read()
        file_size = len(content_bytes)

        if file_size > MAX_FILE_SIZE_BYTES:
            max_mb = MAX_FILE_SIZE_BYTES // (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum allowed size of {max_mb} MB."
            )

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )

        extracted_text = ""

        # 1. PDF Extraction
        if file_ext == ".pdf":
            try:
                import pypdf
                pdf_reader = pypdf.PdfReader(io.BytesIO(content_bytes))
                page_texts = []
                for i, page in enumerate(pdf_reader.pages):
                    page_str = page.extract_text() or ""
                    if page_str.strip():
                        page_texts.append(page_str)
                extracted_text = "\n\n".join(page_texts)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Failed to extract text from PDF: {str(e)}"
                )

        # 2. DOCX Extraction
        elif file_ext == ".docx":
            try:
                import docx
                doc = docx.Document(io.BytesIO(content_bytes))
                paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                extracted_text = "\n\n".join(paragraphs)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Failed to extract text from DOCX document: {str(e)}"
                )

        # 3. Plain text / Markdown / JSON / CSV
        else:
            try:
                extracted_text = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    extracted_text = content_bytes.decode("utf-8-sig")
                except UnicodeDecodeError:
                    try:
                        extracted_text = content_bytes.decode("latin-1")
                    except Exception as e:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Encoding error decoding text file: {str(e)}"
                        )

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
