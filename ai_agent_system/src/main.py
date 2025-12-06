from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from src.api import router as api_router
from src.api.middleware import APIKeyMiddleware, RateLimiterMiddleware, RequestLoggingMiddleware
from src.config import setup_logging
from src.config.settings import settings
from src.config.logging_config import get_logger
from src.utils.health import health_summary
from src.utils.metrics import metrics_response
from src.utils.clients import client_manager
from src.utils.tracing import initialize_tracing, TracingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging(settings.LOG_LEVEL)
    logger = get_logger(app=settings.APP_NAME)
    logger.info("starting application", env=settings.ENV)
    await client_manager.initialize()
    initialize_tracing()
    try:
        yield
    finally:
        logger.info("shutting down application")
        await client_manager.close()


middleware_stack = [
    Middleware(TracingMiddleware),
    Middleware(RequestLoggingMiddleware),
    Middleware(RateLimiterMiddleware, limit=100, window_seconds=60),
    Middleware(APIKeyMiddleware),
]

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    lifespan=lifespan,
    middleware=middleware_stack,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health", tags=["health"])
async def health() -> dict[str, Any]:
    return await health_summary()


@app.get("/api/v1/metrics", tags=["metrics"])
async def metrics():
    return metrics_response()


@app.get("/api/v1/ready", tags=["health"])
async def ready() -> dict[str, Any]:
    return {"status": "ready"}


app.include_router(api_router)
