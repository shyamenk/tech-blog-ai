"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api import research, outline, explain, draft, seo, knowledge, workflow
from app.db.postgres import PostgresPool
from app.db.redis import RedisClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    settings = get_settings()
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Debug mode: {settings.debug}")

    # Initialize database connections
    try:
        await PostgresPool.create_pool()
        print("PostgreSQL connection pool initialized")
    except Exception as e:
        print(f"PostgreSQL not available: {e}")

    try:
        await RedisClient.create_client()
        print("Redis client initialized")
    except Exception as e:
        print(f"Redis not available: {e}")

    yield

    # Shutdown - cleanup connections
    print("Shutting down...")
    try:
        await PostgresPool.close_pool()
        print("PostgreSQL pool closed")
    except Exception:
        pass

    try:
        await RedisClient.close_client()
        print("Redis client closed")
    except Exception:
        pass


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-Powered Technical Content Assistant using LangChain, LangGraph, and RAG",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "app": settings.app_name,
            "version": settings.app_version,
        }

    # Include API routers
    app.include_router(research.router, prefix=settings.api_v1_prefix, tags=["Research"])
    app.include_router(outline.router, prefix=settings.api_v1_prefix, tags=["Outline"])
    app.include_router(explain.router, prefix=settings.api_v1_prefix, tags=["Explain"])
    app.include_router(draft.router, prefix=settings.api_v1_prefix, tags=["Draft"])
    app.include_router(seo.router, prefix=settings.api_v1_prefix, tags=["SEO"])
    app.include_router(knowledge.router, prefix=settings.api_v1_prefix, tags=["Knowledge"])
    app.include_router(workflow.router, prefix=settings.api_v1_prefix, tags=["Workflow"])

    return app


app = create_app()
