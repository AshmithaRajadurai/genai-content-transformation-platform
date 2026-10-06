import time
import uuid
from typing import Any, Dict

from backend.app.modules.nlp.schemas import NLPAnalysisRequest
from backend.app.modules.nlp.service import NLPService
from backend.app.modules.context.schemas import ContextBuildRequest
from backend.app.modules.context.service import ContextService
from backend.app.modules.llm.schemas import LLMBatchGenerationRequest
from backend.app.modules.llm.service import LLMService
from backend.app.modules.generation.schemas import (
    TransformationPipelineRequest,
    TransformationPipelineResponse,
)
from backend.app.modules.generation.service import GenerationService
from backend.app.modules.history.service import HistoryService
from backend.app.modules.history.schemas import TransformationRecord


class TransformationPipeline:
    """
    End-to-End Orchestration Pipeline:
    Coordinates Ingestion → NLP → (optional RAG) → Context Engineering → LLM → Multi-Channel Generation → Persistence.
    """

    CHANNEL_MAPPING = {
        "linkedin": "linkedin",
        "twitter": "twitter",
        "advisory": "advisory",
        "executive": "executive_summary",
        "executive_summary": "executive_summary",
        "infographic": "infographic",
        "presentation": "presentation",
        "video": "video_script",
        "video_script": "video_script"
    }

    @classmethod
    def execute(cls, request: TransformationPipelineRequest) -> TransformationPipelineResponse:
        t0 = time.time()

        # Step 1: Ingestion & Normalization
        cleaned_text = request.source_text.strip()

        # Step 2: NLP Analysis (Layer 2)
        nlp_data = NLPService.analyze(
            NLPAnalysisRequest(
                content=cleaned_text,
                title=request.title,
                source_type=request.source_type or "text"
            )
        )

        # Step 3: Optional RAG Integration Point (Hook for future semantic retrieval)
        # rag_context = RAGService.retrieve_relevant_chunks(cleaned_text) if request.use_rag else None

        # Step 4: Context Engineering (Layer 3)
        target_channels = [cls.CHANNEL_MAPPING.get(c, c) for c in request.target_channels]

        detail_param = "balanced"
        if request.detail_level:
            lower_detail = request.detail_level.lower()
            if "concise" in lower_detail:
                detail_param = "concise"
            elif "in-depth" in lower_detail or "comprehensive" in lower_detail:
                detail_param = "comprehensive"

        ctx_req = ContextBuildRequest(
            source_text=cleaned_text,
            title=request.title,
            source_type=request.source_type or "text",
            nlp_analysis=nlp_data,
            target_channels=target_channels,
            audience=request.audience,
            tone=request.tone,
            language=request.language,
            detail_level=detail_param
        )
        context_payload = ContextService.build_context(ctx_req)

        # Step 5: LLM Generation (Layer 4)
        batch_llm_req = LLMBatchGenerationRequest(
            context_payload=context_payload,
            provider=request.provider or "auto"
        )
        llm_batch_response = LLMService.generate_batch(batch_llm_req)

        # Step 6: Generative AI Structuring into Artefacts (Layer 5)
        resolved_title = context_payload.source_title
        artefacts: Dict[str, Any] = {}

        for user_ch_id in request.target_channels:
            llm_ch_id = cls.CHANNEL_MAPPING.get(user_ch_id, user_ch_id)
            llm_output = llm_batch_response.results.get(llm_ch_id)
            raw_text = llm_output.content if llm_output else ""
            artefacts[user_ch_id] = GenerationService.format_channel(
                channel_id=user_ch_id,
                raw_text=raw_text,
                nlp_data=nlp_data,
                title=resolved_title
            )

        latency_ms = round((time.time() - t0) * 1000, 2)
        transformation_id = str(uuid.uuid4())

        # Step 7: Persistence Layer (MongoDB Atlas with in-memory session resilience)
        try:
            record = TransformationRecord(
                transformation_id=transformation_id,
                source_title=resolved_title,
                source_type=request.source_type or "text",
                source_text=cleaned_text[:10000],
                selected_channels=request.target_channels,
                audience=request.audience or "General Enterprise",
                tone=request.tone or "Professional",
                language=request.language or "English",
                detail_level=request.detail_level or "Balanced",
                detected_topic=nlp_data.topic,
                keywords=nlp_data.keywords[:10],
                entities_count=len(nlp_data.entities),
                key_facts_count=len(nlp_data.key_facts),
                artefacts=artefacts,
                total_tokens=llm_batch_response.total_tokens,
                execution_time_ms=latency_ms
            )
            HistoryService.save_transformation(record)
        except Exception:
            pass

        return TransformationPipelineResponse(
            transformation_id=transformation_id,
            source_title=resolved_title,
            source_type=request.source_type or "text",
            nlp_analysis=nlp_data,
            context_payload=context_payload,
            llm_batch_response=llm_batch_response,
            artefacts=artefacts,
            total_tokens=llm_batch_response.total_tokens,
            execution_time_ms=latency_ms
        )
