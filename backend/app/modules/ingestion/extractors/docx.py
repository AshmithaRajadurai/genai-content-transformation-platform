import io
from fastapi import HTTPException, status


def extract_docx(content_bytes: bytes) -> str:
    """Extracts text from paragraphs of a DOCX document using python-docx."""
    try:
        import docx
        doc = docx.Document(io.BytesIO(content_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to extract text from DOCX document: {str(e)}"
        )
