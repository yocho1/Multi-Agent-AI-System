from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.agents.orchestrator import OrchestratorAgent
from src.agents.planner import PlannerAgent

router = APIRouter(prefix="/agents", tags=["agents"])

planner = PlannerAgent(name="planner", role="Task decomposition", capabilities=["plan"])
orchestrator = OrchestratorAgent(planner=planner)


class AgentExecuteRequest(BaseModel):
    agent_id: str
    task: str
    parameters: Dict[str, Any] | None = None


@router.get("", summary="List available agents")
async def list_agents() -> List[Dict[str, Any]]:
    return [
        {"id": "orchestrator", "role": "Coordinator", "capabilities": orchestrator.capabilities},
        {"id": "planner", "role": "Task decomposition", "capabilities": planner.capabilities},
    ]


@router.get("/{agent_id}", summary="Get agent details")
async def get_agent(agent_id: str) -> Dict[str, Any]:
    agents = {
        "orchestrator": {"id": "orchestrator", "role": orchestrator.role},
        "planner": {"id": "planner", "role": planner.role},
    }
    if agent_id not in agents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agents[agent_id]


@router.post("/execute", summary="Execute specific agent")
async def execute_agent(payload: AgentExecuteRequest) -> Dict[str, Any]:
    if payload.agent_id == "planner":
        result = await planner.execute(payload.task)
    else:
        result = await orchestrator.execute(payload.task)
    return {"agent_id": payload.agent_id, "task": payload.task, "status": "completed", "result": result}
