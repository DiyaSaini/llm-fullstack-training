"""
Application entry point.

Creates the FastAPI app, registers all routers, and configures
startup behaviour. Run with:

    uv run uvicorn app.main:app --reload
    # or
    python -m uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.api.v1.routers import (
    classify,
    keywords,
    paraphrase,
    qa,
    sentiment,
    summarize,
    translate,
)
from app.config import settings
from app.logging import setup_logging

setup_logging()


def create_app() -> FastAPI:
    """Factory function that builds and returns the FastAPI application."""

    app = FastAPI(
        title=settings.app_title,
        version=settings.app_version,
        description=(
            "A production-structured AI Text Processing API. "
            "Each endpoint is an independent vertical slice built by a separate engineer."
        ),
    )

    api_prefix = "/api/v1"

    app.include_router(summarize.router, prefix=api_prefix, tags=["Summarize"])
    app.include_router(classify.router, prefix=api_prefix, tags=["Classify"])
    app.include_router(keywords.router, prefix=api_prefix, tags=["Keywords"])
    app.include_router(sentiment.router, prefix=api_prefix, tags=["Sentiment"])
    app.include_router(qa.router, prefix=api_prefix, tags=["Q&A"])
    app.include_router(paraphrase.router, prefix=api_prefix, tags=["Paraphrase"])
    app.include_router(translate.router, prefix=api_prefix, tags=["Translate"])

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict[str, str]:
        """Basic liveness probe."""
        return {"status": "ok", "version": settings.app_version}

    return app


app = create_app()
