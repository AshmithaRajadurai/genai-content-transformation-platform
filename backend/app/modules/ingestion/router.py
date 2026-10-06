from fastapi import APIRouter, File, UploadFile, status

from backend.app.modules.ingestion.schemas import IngestionResponse, SourceTextInput
from backend.app.modules.ingestion.service import IngestionService
from backend.app.shared.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES

router = APIRouter(prefix="/api/v1/source", tags=["Source Ingestion Layer"])


@router.post(
    "/text",
    response_model=IngestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest Raw Source Text",
    description="Validates, normalizes, and prepares raw text, articles, incident reports, or prompts for downstream NLP analysis."
)
def ingest_text_endpoint(payload: SourceTextInput):
    return IngestionService.ingest_text_input(payload)


@router.post(
    "/upload",
    response_model=IngestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest Source Document / File Upload",
    description="Accepts document uploads (.pdf, .docx, .txt, .md, .json, .csv), validates file constraints, and extracts normalized text."
)
async def ingest_upload_endpoint(file: UploadFile = File(...)):
    return await IngestionService.ingest_uploaded_file(file)


@router.get(
    "/supported-formats",
    summary="List Supported Ingestion Formats",
    description="Returns metadata about supported file formats, size limits, and ingestion rules."
)
def get_supported_formats():
    return {
        "status": "active",
        "max_file_size_mb": MAX_FILE_SIZE_BYTES // (1024 * 1024),
        "supported_extensions": list(ALLOWED_EXTENSIONS.keys()),
        "format_details": {
            "pdf": "Extracts text from all readable pages via pypdf",
            "docx": "Extracts structured text from paragraphs and tables via python-docx",
            "txt": "Plain UTF-8 text with automatic fallback decoding",
            "markdown": "Markdown documents with header and section parsing",
            "json": "Raw structured JSON content",
            "csv": "Comma-separated tabular datasets"
        }
    }
