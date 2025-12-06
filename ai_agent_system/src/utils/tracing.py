from __future__ import annotations

from typing import Any, Callable, Optional

from fastapi import Request, Response
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from starlette.middleware.base import BaseHTTPMiddleware

from src.config.settings import settings
from src.config.logging_config import get_logger

tracer: Optional[trace.Tracer] = None


def initialize_tracing() -> None:
    """Initialize OpenTelemetry tracing."""
    global tracer
    if not settings.TRACING_ENDPOINT:
        return
    try:
        exporter = OTLPSpanExporter(endpoint=str(settings.TRACING_ENDPOINT))
        trace.set_tracer_provider(TracerProvider())
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))
        tracer = trace.get_tracer(__name__)
        logger = get_logger(component="tracing")
        logger.info("tracing initialized", endpoint=str(settings.TRACING_ENDPOINT))
    except Exception as exc:  # noqa: BLE001
        logger = get_logger(component="tracing")
        logger.error("tracing init failed", error=str(exc))


class TracingMiddleware(BaseHTTPMiddleware):
    """OpenTelemetry tracing middleware."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        if not tracer:
            return await call_next(request)

        with tracer.start_as_current_span(f"{request.method} {request.url.path}") as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", str(request.url))
            response = await call_next(request)
            span.set_attribute("http.status_code", response.status_code)
            return response
