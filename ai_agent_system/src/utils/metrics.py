from __future__ import annotations

from typing import Callable

from prometheus_client import Counter, Histogram, CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest
from fastapi import Response

request_counter = Counter("api_requests_total", "Total API requests", ["method", "path", "status_code"])
request_latency = Histogram("api_request_latency_seconds", "API request latency", ["method", "path"])


def record_request(method: str, path: str, status_code: int, latency_seconds: float) -> None:
    request_counter.labels(method=method, path=path, status_code=str(status_code)).inc()
    request_latency.labels(method=method, path=path).observe(latency_seconds)


def metrics_response() -> Response:
    payload = generate_latest()
    return Response(content=payload, media_type=CONTENT_TYPE_LATEST)
