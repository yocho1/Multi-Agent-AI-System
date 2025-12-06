from __future__ import annotations

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.config.logging_config import get_logger
from src.utils.metrics import record_request


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Structured request logging with latency."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        logger = get_logger(path=request.url.path, method=request.method)
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        duration_ms = duration * 1000
        logger.info("request", status_code=response.status_code, duration_ms=duration_ms)
        record_request(request.method, request.url.path, response.status_code, duration)
        return response
