"""Compatibility re-export layer for NLP service."""
from backend.app.modules.nlp.service import (
    NLPService,
    STOPWORDS,
    TOPIC_LEXICONS,
)

__all__ = [
    "NLPService",
    "STOPWORDS",
    "TOPIC_LEXICONS",
]
