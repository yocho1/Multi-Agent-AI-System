from __future__ import annotations

import asyncio
import time
from collections import defaultdict, deque
from typing import Any, Callable, DefaultDict, Deque, Optional

from fastapi import Request, Response
from redis.asyncio import Redis
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from src.config.settings import settings


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Rate limiter with optional Redis backend (fallback to in-memory)."""

    def __init__(self, app: Any, limit: int = 100, window_seconds: int = 60) -> None:  # type: ignore[override]
        super().__init__(app)
        self.limit = limit
        self.window_seconds = window_seconds
        self.hits: DefaultDict[str, Deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()
        self.redis: Optional[Redis[bytes]] = None

    async def _get_redis(self) -> Optional[Redis[bytes]]:
        if self.redis:
            return self.redis
        try:
            self.redis = Redis.from_url(str(settings.REDIS_URL))  # type: ignore[assignment]
            return self.redis
        except Exception:  # noqa: BLE001
            return None

    async def _redis_allowed(self, key: str) -> bool:
        redis = await self._get_redis()
        if not redis:
            return await self._memory_allowed(key)
        try:
            now_ms = int(time.time() * 1000)
            window_ms = self.window_seconds * 1000
            async with redis.pipeline() as pipe:
                pipe.zremrangebyscore(key, 0, now_ms - window_ms)
                pipe.zadd(key, {str(now_ms): now_ms})
                pipe.zcard(key)
                pipe.expire(key, self.window_seconds)
                removed, _, count, _ = await pipe.execute()
            return count <= self.limit
        except Exception:  # noqa: BLE001
            # Redis failed, fall back to memory
            return await self._memory_allowed(key)

    async def _memory_allowed(self, key: str) -> bool:
        now = time.time()
        async with self._lock:
            window = self.hits[key]
            while window and now - window[0] > self.window_seconds:
                window.popleft()
            if len(window) >= self.limit:
                return False
            window.append(now)
        return True

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        if request.url.path in {"/api/v1/health", "/api/v1/metrics", "/api/v1/ready"}:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        allowed = await self._redis_allowed(client_ip)
        if not allowed:
            return Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
        return await call_next(request)
