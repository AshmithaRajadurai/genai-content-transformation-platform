from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import db
from backend.app.routes.source_routes import router as source_router

app = FastAPI(
    title="GenAI Content Transformation Platform",
    description="AI-powered multi-channel content transformation platform integrating NLP, Context Engine, LLM, and Generative AI.",
    version="0.2.0"
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