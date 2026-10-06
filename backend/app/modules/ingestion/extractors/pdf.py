import io
from fastapi import HTTPException, status


def extract_pdf(content_bytes: bytes) -> str:
    """Extracts text from all readable pages of a PDF document using pypdf."""
    try:
        import pypdf
        pdf_reader = pypdf.PdfReader(io.BytesIO(content_bytes))
        page_texts = []
        for page in pdf_reader.pages:
            page_str = page.extract_text() or ""
            if page_str.strip():
                page_texts.append(page_str)
        return "\n\n".join(page_texts)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to extract text from PDF: {str(e)}"
        )
