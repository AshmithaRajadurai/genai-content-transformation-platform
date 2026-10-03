from fastapi import FastAPI

from backend.app.database import db

app = FastAPI(
    title="GenAI Content Transformation Platform",
    description="AI-powered content transformation platform using NLP, LLM and Generative AI.",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "GenAI Content Transformation Platform API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/health/database")
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