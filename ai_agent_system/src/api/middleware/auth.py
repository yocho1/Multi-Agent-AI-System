from __future__ import annotations

from typing import Callable

from fastapi import Request, Response
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from src.config.settings import settings
from src.utils.auth import api_key_store, decode_access_token


class APIKeyMiddleware(BaseHTTPMiddleware):
    """API key and JWT authentication via X-API-Key or Authorization header."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        # Allow health, metrics, docs, and OpenAPI spec without auth
        if request.url.path in {"/api/v1/health", "/api/v1/metrics", "/api/v1/ready", "/docs", "/openapi.json", "/redoc"}:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")
        auth_header = request.headers.get("Authorization", "")

        is_valid = False
        if api_key and api_key_store.validate_key(api_key):
            is_valid = True
        elif auth_header.startswith("Bearer "):
            token = auth_header[7:]
            payload = decode_access_token(token)
            is_valid = payload is not None

        if settings.SECRET_KEY and not is_valid:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        return await call_next(request)
