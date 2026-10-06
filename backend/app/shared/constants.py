"""Global constants for the GenAI Content Transformation Platform."""

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".json": "application/json",
    ".csv": "text/csv",
}

SUPPORTED_CHANNELS = [
    "linkedin",
    "twitter",
    "advisory",
    "executive",
    "infographic",
    "presentation",
    "video",
]
