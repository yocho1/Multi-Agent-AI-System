from __future__ import annotations

import sys
import os
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

# Set GOOGLE_APPLICATION_CREDENTIALS FIRST before any imports that use Firebase
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    # Try to set it from environment or default location
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")
    if not os.path.isabs(cred_path):
        # Make absolute relative to current working directory
        cred_path = os.path.abspath(cred_path)
    if os.path.exists(cred_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from src.api import router as api_router
from src.api.endpoints.auth_endpoints import router as auth_router
from src.api.endpoints.test_endpoints import router as test_router
from src.api.endpoints.location_endpoints import router as location_router
from src.api.middleware import APIKeyMiddleware, RateLimiterMiddleware, RequestLoggingMiddleware
from src.config import setup_logging
from src.config.settings import settings
from src.config.logging_config import get_logger
from src.utils.health import health_summary
from src.utils.metrics import metrics_response
from src.utils.clients import client_manager
from src.utils.tracing import initialize_tracing, TracingMiddleware
from src.utils.firebase_auth import get_firebase_auth
from src.utils.firebase_cache import get_firestore_cache


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging(settings.LOG_LEVEL)
    logger = get_logger(app=settings.APP_NAME)
    logger.info("starting application", env=settings.ENV)
    logger.info(f"GOOGLE_APPLICATION_CREDENTIALS: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'NOT SET')}")
    logger.info(f"Firebase credentials path from settings: {settings.FIREBASE_CREDENTIALS_PATH}")
    await client_manager.initialize()
    initialize_tracing()
    # Initialize Firebase services
    get_firebase_auth()
    get_firestore_cache()
    logger.info("Firebase services initialized")
    try:
        yield
    finally:
        logger.info("shutting down application")
        await client_manager.close()


middleware_stack = [
    Middleware(CORSMiddleware,
               allow_origins=["*"],
               allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"]),
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
    allow_origins=["*"],
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
app.include_router(auth_router)
app.include_router(test_router)
app.include_router(location_router)
