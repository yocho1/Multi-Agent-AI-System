from __future__ import annotations

from typing import Dict, Iterable, Optional

from src.agents.base.tool import BaseTool
from src.utils.exceptions import ToolExecutionError


class ToolRegistry:
    """In-memory tool registry with simple lookup and execution helper."""

    def __init__(self) -> None:
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list(self) -> Iterable[str]:
        return self._tools.keys()

    async def execute(self, name: str, **kwargs):
        tool = self.get(name)
        if not tool:
            raise ToolExecutionError(f"Tool {name} not found")
        return await tool.execute(**kwargs)


tool_registry = ToolRegistry()
