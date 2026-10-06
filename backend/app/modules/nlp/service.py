from typing import List, Tuple

from backend.app.modules.nlp.schemas import (
    KeywordItem,
    NamedEntity,
    NLPAnalysisRequest,
    NLPAnalysisResponse,
)
from backend.app.modules.nlp.keyword_extractor import extract_keywords, STOPWORDS
from backend.app.modules.nlp.topic_classifier import identify_topics, TOPIC_LEXICONS
from backend.app.modules.nlp.entity_extractor import extract_named_entities
from backend.app.modules.nlp.fact_extractor import infer_content_type_and_tone, extract_key_facts


class NLPService:
    """
    NLP Analysis Service:
    Orchestrates topic identification, keyword extraction, NER, tone detection,
    and factual assertion extraction.
    """

    STOPWORDS = STOPWORDS
    TOPIC_LEXICONS = TOPIC_LEXICONS

    @classmethod
    def extract_keywords(cls, text: str, top_n: int = 8) -> List[KeywordItem]:
        return extract_keywords(text, top_n=top_n)

    @classmethod
    def identify_topics(cls, text: str) -> Tuple[str, List[str]]:
        return identify_topics(text)

    @classmethod
    def extract_named_entities(cls, text: str) -> List[NamedEntity]:
        return extract_named_entities(text)

    @classmethod
    def infer_content_type_and_tone(cls, text: str, primary_topic: str) -> Tuple[str, str]:
        return infer_content_type_and_tone(text, primary_topic)

    @classmethod
    def extract_key_facts(cls, text: str, top_n: int = 4) -> List[str]:
        return extract_key_facts(text, top_n=top_n)

    @classmethod
    def analyze(cls, payload: NLPAnalysisRequest) -> NLPAnalysisResponse:
        """
        Executes the full NLP semantic extraction pipeline:
        Keywords → Topics → Named Entities → Content Classification → Key Facts → Context Summary.
        """
        text = payload.content.strip()

        # 1. Keywords & Keyphrases
        keyword_items = cls.extract_keywords(text, top_n=8)
        keywords_list = [item.keyword for item in keyword_items]

        # 2. Topic Identification
        primary_topic, all_topics = cls.identify_topics(text)

        # 3. Named Entity Recognition (NER)
        entities = cls.extract_named_entities(text)

        # 4. Content Type & Tone
        content_type, detected_tone = cls.infer_content_type_and_tone(text, primary_topic)

        # 5. Key Facts Extraction
        key_facts = cls.extract_key_facts(text, top_n=4)

        # 6. Context Summary Formulation
        if key_facts:
            summary_context = f"{content_type}: {key_facts[0]}"
        else:
            summary_context = f"{content_type} concerning {primary_topic.lower()} with {len(keywords_list)} salient keywords extracted."

        # 7. Confidence Score
        confidence = min(99.0, max(85.0, 88.0 + (len(keyword_items) * 0.8) + (len(entities) * 0.5)))

        return NLPAnalysisResponse(
            topic=primary_topic,
            topics=all_topics,
            content_type=content_type,
            detected_tone=detected_tone,
            keywords=keywords_list,
            keyword_items=keyword_items,
            entities=entities,
            key_facts=key_facts,
            summary_context=summary_context,
            confidence_score=round(confidence, 1)
        )
