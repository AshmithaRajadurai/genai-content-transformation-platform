from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.database.connection import db
from backend.app.modules.ingestion.router import router as source_router
from backend.app.modules.nlp.router import router as nlp_router
from backend.app.modules.context.router import router as context_router
from backend.app.modules.llm.router import router as llm_router
from backend.app.modules.orchestration.router import router as transformation_router
from backend.app.modules.history.router import router as history_router
from backend.app.modules.rag.router import router as rag_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered multi-channel content transformation platform integrating NLP, RAG, Context Engine, LLM (n8n ready), Generative AI, and MongoDB Storage.",
    version=settings.PROJECT_VERSION
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(source_router)
app.include_router(nlp_router)
app.include_router(context_router)
app.include_router(llm_router)
app.include_router(transformation_router)
app.include_router(history_router)
app.include_router(rag_router)


@app.get("/", tags=["System"])
def root():
    return {
        "message": "GenAI Content Transformation Platform API is running",
        "version": "0.2.0",
        "docs_url": "/docs"
    }


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/health/database", tags=["System"])
def database_health_check():
    try:
        db.command("ping")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }