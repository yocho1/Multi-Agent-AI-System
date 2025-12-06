from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.agents.base.tool import BaseTool
from src.utils.tool_registry import tool_registry

router = APIRouter(prefix="/tools", tags=["tools"])


class ToolExecuteRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]


# Placeholder echo tool for demonstration
class EchoParams(BaseModel):
    text: str


class EchoTool(BaseTool):
    async def _run(self, params: BaseModel):  # type: ignore[override]
        return {"echo": params.dict()}


tool_registry.register(EchoTool(name="echo", description="Echo input", param_model=EchoParams))


@router.post("/execute", summary="Execute a tool directly")
async def execute_tool(payload: ToolExecuteRequest) -> Dict[str, Any]:
    tool = tool_registry.get(payload.tool_name)
    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    result = await tool_registry.execute(payload.tool_name, **payload.parameters)
    return {"tool_name": payload.tool_name, "status": "completed", "result": result}
