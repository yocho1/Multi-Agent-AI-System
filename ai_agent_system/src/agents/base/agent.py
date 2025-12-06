from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.agents.base.memory import BaseMemory, ShortTermMemory
from src.agents.base.tool import BaseTool
from src.config.logging_config import get_logger
from src.utils.exceptions import AgentExecutionError


class BaseAgent(ABC):
    """Abstract base agent defining common capabilities."""

    def __init__(
        self,
        name: str,
        role: str,
        capabilities: List[str],
        memory: Optional[BaseMemory] = None,
    ) -> None:
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.tools: Dict[str, BaseTool] = {}
        self.memory = memory or ShortTermMemory()
        self.metrics: Dict[str, float] = {"invocations": 0, "last_latency_ms": 0.0}
        self.logger = get_logger(agent_name=self.name, agent_role=self.role)

    def register_tool(self, tool: BaseTool) -> None:
        self.tools[tool.name] = tool
        self.logger.debug("registered tool", tool=tool.name)

    async def execute(self, task: str, **kwargs: Any) -> Any:
        self.metrics["invocations"] += 1
        start = time.perf_counter()
        try:
            chain = await self.think(task, **kwargs)
            result = await self.act(chain, **kwargs)
            await self.memory.add({"task": task, "result": result})
            return result
        except Exception as exc:  # noqa: BLE001
            await self.recover(exc, task)
            raise AgentExecutionError(f"Agent {self.name} failed: {exc}") from exc
        finally:
            self.metrics["last_latency_ms"] = (time.perf_counter() - start) * 1000

    @abstractmethod
    async def act(self, chain_of_thought: str, **kwargs: Any) -> Any:
        """Perform the action step given a plan/chain of thought."""

    async def think(self, task: str, **kwargs: Any) -> str:
        """Produce a chain of thought; override for LLM-backed reasoning."""
        return f"Plan for task: {task}"

    async def self_reflect(self, observation: str) -> None:
        await self.memory.add({"reflection": observation})

    async def recover(self, error: Exception, task: str) -> None:
        self.logger.error("execution error", task=task, error=str(error))
        await self.memory.add({"error": str(error), "task": task})

    async def aggregate_tool_results(self, results: List[Any]) -> Any:
        """Aggregate multiple tool outputs; override with domain logic."""
        return results
