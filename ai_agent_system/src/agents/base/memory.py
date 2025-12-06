from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Deque, Iterable, List


class BaseMemory(ABC):
    """Abstract memory interface for agents."""

    @abstractmethod
    async def add(self, item: Any) -> None:
        ...

    @abstractmethod
    async def get_recent(self, limit: int = 5) -> List[Any]:
        ...

    @abstractmethod
    async def flush(self) -> None:
        ...


class ShortTermMemory(BaseMemory):
    """Simple in-memory buffer for short-lived context."""

    def __init__(self, maxlen: int = 50) -> None:
        self._buffer: Deque[Any] = deque(maxlen=maxlen)
        self._lock = asyncio.Lock()

    async def add(self, item: Any) -> None:
        async with self._lock:
            self._buffer.append(item)

    async def get_recent(self, limit: int = 5) -> List[Any]:
        async with self._lock:
            return list(list(self._buffer)[-limit:])

    async def flush(self) -> None:
        async with self._lock:
            self._buffer.clear()
