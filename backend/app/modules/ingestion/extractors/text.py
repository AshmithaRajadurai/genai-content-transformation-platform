from fastapi import HTTPException, status


def extract_text(content_bytes: bytes) -> str:
    """Extracts text from plain text, Markdown, JSON, or CSV bytes with encoding fallbacks."""
    try:
        return content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return content_bytes.decode("utf-8-sig")
        except UnicodeDecodeError:
            try:
                return content_bytes.decode("latin-1")
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Encoding error decoding text file: {str(e)}"
                )
