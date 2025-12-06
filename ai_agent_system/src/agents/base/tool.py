from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import BaseModel, ValidationError
from tenacity import AsyncRetrying, RetryError, retry_if_exception_type, stop_after_attempt, wait_exponential

from src.utils.exceptions import ToolExecutionError


class BaseTool(ABC):
    """Abstract base tool supporting validation, retries, and cost tracking."""

    name: str
    description: str
    param_model: Type[BaseModel]
    max_retries: int = 3
    cost_per_call: float = 0.0

    def __init__(
        self,
        name: str,
        description: str,
        param_model: Type[BaseModel],
        max_retries: int = 3,
        cost_per_call: float = 0.0,
    ) -> None:
        self.name = name
        self.description = description
        self.param_model = param_model
        self.max_retries = max_retries
        self.cost_per_call = cost_per_call
        self.last_cost: float = 0.0

    async def execute(self, **kwargs: Any) -> Any:
        try:
            params = self.param_model(**kwargs)
        except ValidationError as exc:
            raise ToolExecutionError(f"Invalid parameters for tool {self.name}: {exc}") from exc

        start = time.perf_counter()
        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
                retry=retry_if_exception_type(ToolExecutionError),
                reraise=True,
            ):
                with attempt:
                    return await self._run(params)
        except RetryError as exc:
            raise ToolExecutionError(f"Tool {self.name} failed after retries: {exc}") from exc
        finally:
            duration = time.perf_counter() - start
            self.last_cost = self.cost_per_call
            await self.on_after_execute(duration)

    async def on_after_execute(self, duration_seconds: float) -> None:
        """Hook for metrics or cost tracking after execution."""

    @abstractmethod
    async def _run(self, params: BaseModel) -> Any:
        """Execute the tool with validated params."""


class NoParams(BaseModel):
    """Default empty params model."""

    pass
