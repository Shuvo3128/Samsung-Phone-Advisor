from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Samsung Phone Advisor API",
        description="RAG + Multi-Agent system for Samsung smartphone recommendations",
        version="1.0.0",
    )

    # CORS (safe default)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(api_router, prefix="/api")

    # Health check
    @app.get("/", tags=["Health"])
    async def health_check():
        return {"status": "ok", "message": "Samsung Phone Advisor is running 🚀"}

    return app


app = create_app()
