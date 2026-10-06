# GenAI Content Transformation Platform — Modular Architecture

## 1. Overview
The GenAI Content Transformation Platform transforms raw content (articles, incident reports, technical advisories, research briefs) into 7 publication-ready, format-specialized artefacts for diverse distribution channels.

The architecture is refactored into domain-driven modules:
1. **NLP**: Topic classification, Salient keywords, Named Entity Recognition (NER), Factual assertion extraction.
2. **RAG**: Retrieval-Augmented Generation interfaces (Chunking, Embeddings, Vector Store, Semantic Retriever).
3. **Context Engineering**: Audience & tone persona alignment, factual grounding, and channel prompt compilation.
4. **LLM**: Multi-provider LLM interface (Gemini, OpenAI, Local Fallback, n8n Orchestrator).
5. **n8n Workflow Orchestration**: Webhook client and payload contracts for external workflow orchestration.
6. **Generative AI / Structuring**: Channel-specialized formatters for LinkedIn, Twitter, Advisory, Executive Summary, Infographic, Presentation, and Video Script.
7. **MongoDB Storage & History**: Persistence to MongoDB Atlas with resilient in-memory session caching.

---

## 2. Target Architecture Directory Layout

```text
backend/app/
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── logging.py
│   └── exceptions.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── repositories/
│       ├── __init__.py
│       └── transformation_repository.py
│
├── modules/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── validators.py
│   │   └── extractors/
│   │       ├── __init__.py
│   │       ├── pdf.py
│   │       ├── docx.py
│   │       └── text.py
│   │
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── keyword_extractor.py
│   │   ├── entity_extractor.py
│   │   ├── topic_classifier.py
│   │   └── fact_extractor.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── context/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── providers/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── gemini.py
│   │       ├── openai.py
│   │       ├── fallback.py
│   │       └── n8n.py
│   │
│   ├── generation/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── generators/
│   │       ├── __init__.py
│   │       ├── linkedin.py
│   │       ├── twitter.py
│   │       ├── advisory.py
│   │       ├── executive.py
│   │       ├── infographic.py
│   │       ├── presentation.py
│   │       └── video.py
│   │
│   ├── orchestration/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── pipeline.py
│   │
│   ├── n8n/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── webhooks.py
│   │   └── workflows/
│   │       └── __init__.py
│   │
│   └── history/
│       ├── __init__.py
│       ├── router.py
│       ├── schemas.py
│       └── service.py
│
└── shared/
    ├── __init__.py
    ├── constants.py
    ├── schemas/
    └── utilities/
```

---

## 3. End-to-End Orchestration Flow

```text
SOURCE CONTENT (Text / Uploaded Document)
   │
   ▼
[modules/ingestion] (Validation, extraction via pypdf/docx/text, sanitization)
   │
   ▼
[modules/nlp] (Topic classification, keywords, NER, tone, key facts)
   │
   ▼
[modules/rag] (Optional semantic retrieval against domain vector store)
   │
   ▼
[modules/context] (Grounding, anti-hallucination guardrails, channel prompts)
   │
   ▼
[modules/llm] ───► [modules/llm/providers/n8n.py] ───► [modules/n8n/client.py]
   │                                                             │
   │                                                             ▼
   │                                                   n8n Webhook / Ollama
   │                                                             │
   ◄─────────────────────────────────────────────────────────────┘
   │
   ▼
[modules/generation] (Formatting via 7 dedicated channel generators)
   │
   ▼
[modules/history] & [database] (MongoDB Atlas persistence + session fallback)
```

---

## 4. Next Phase Roadmaps

### n8n Integration (Next Phase)
- Configure `N8N_WEBHOOK_URL` in `.env`.
- Deploy n8n workflow listening on webhook, passing prompt to local Ollama or hosted LLM.
- Return structured content back to `N8nLLMProvider` through `modules/n8n/client.py`.

### RAG Integration (Next Phase)
- Connect embedding provider (e.g., SentenceTransformers, OpenAI embeddings).
- Bind vector store (e.g., Qdrant, Chroma, or MongoDB Atlas Vector Search).
- Inject semantic context passages into `modules/context/service.py` to augment fact grounding.
