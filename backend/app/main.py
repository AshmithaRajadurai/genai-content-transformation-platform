from fastapi import FastAPI

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