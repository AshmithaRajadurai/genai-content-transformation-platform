from typing import Optional
from fastapi import HTTPException, status
from backend.app.shared.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES


def validate_text_length(text: str, min_length: int = 5) -> str:
    raw = (text or "").strip()
    if len(raw) < min_length:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Source content too short. Please provide at least {min_length} characters."
        )
    return raw


def validate_file_metadata(filename: Optional[str], file_size: int) -> str:
    fname = filename or "unknown_file.txt"
    file_ext = "." + fname.rsplit(".", 1)[-1].lower() if "." in fname else ""

    if file_ext not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(ALLOWED_EXTENSIONS.keys())
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{file_ext}'. Allowed formats: {allowed}"
        )

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

    return file_ext
