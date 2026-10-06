class AppException(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class IngestionError(AppException):
    """Raised when document ingestion or parsing fails."""

    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        super().__init__(message, status_code=status_code, details=details)


class NLPError(AppException):
    """Raised when NLP analysis or feature extraction fails."""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        super().__init__(message, status_code=status_code, details=details)


class RAGError(AppException):
    """Raised when retrieval-augmented generation operations fail."""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        super().__init__(message, status_code=status_code, details=details)


class ContextError(AppException):
    """Raised when prompt context engineering fails."""

    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        super().__init__(message, status_code=status_code, details=details)


class LLMError(AppException):
    """Raised when LLM invocation or orchestration fails."""

    def __init__(self, message: str, status_code: int = 502, details: dict = None):
        super().__init__(message, status_code=status_code, details=details)


class GenerationError(AppException):
    """Raised when content generation or formatting fails."""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        super().__init__(message, status_code=status_code, details=details)


class DatabaseError(AppException):
    """Raised when database operations fail."""

    def __init__(self, message: str, status_code: int = 503, details: dict = None):
        super().__init__(message, status_code=status_code, details=details)
