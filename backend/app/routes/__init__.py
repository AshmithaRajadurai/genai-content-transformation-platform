from backend.app.routes.source_routes import router as source_router
from backend.app.routes.nlp_routes import router as nlp_router
from backend.app.routes.context_routes import router as context_router

__all__ = ["source_router", "nlp_router", "context_router"]

