from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.agents.orchestrator import OrchestratorAgent
from src.agents.planner import PlannerAgent
from src.agents.specialized import WriterAgent
from src.agents.base.memory import ShortTermMemory
from src.agents.weather import WeatherAgent

router = APIRouter(prefix="/agents", tags=["agents"])

planner = PlannerAgent(name="planner", role="Task decomposition", capabilities=["plan"])
orchestrator = OrchestratorAgent(planner=planner)
weather = WeatherAgent(name="weather", role="Weather lookup", capabilities=["forecast"])
writer = WriterAgent(
    name="writer",
    role="Content generation specialist",
    capabilities=["content_generation", "creative_writing", "code_generation"],
    memory=ShortTermMemory()
)


class AgentExecuteRequest(BaseModel):
    agent_id: str
    task: str
    parameters: Dict[str, Any] | None = None


class WriterRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1000
    chain_of_thought: str = ""


@router.get("", summary="List available agents")
async def list_agents() -> List[Dict[str, Any]]:
    return [
        {"id": "orchestrator", "role": "Coordinator", "capabilities": orchestrator.capabilities},
        {"id": "planner", "role": "Task decomposition", "capabilities": planner.capabilities},
        {"id": "weather", "role": "Weather lookup", "capabilities": weather.capabilities},
    ]


@router.get("/{agent_id}", summary="Get agent details")
async def get_agent(agent_id: str) -> Dict[str, Any]:
    agents = {
        "orchestrator": {"id": "orchestrator", "role": orchestrator.role},
        "planner": {"id": "planner", "role": planner.role},
        "weather": {"id": "weather", "role": weather.role},
    }
    if agent_id not in agents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agents[agent_id]


@router.post("/execute", summary="Execute specific agent")
async def execute_agent(payload: AgentExecuteRequest) -> Dict[str, Any]:
    if payload.agent_id == "planner":
        result = await planner.execute(payload.task)
    elif payload.agent_id == "weather":
        loc = payload.parameters.get("location") if payload.parameters else payload.task
        result = await weather.execute(payload.task, location=loc)
    else:
        result = await orchestrator.execute(payload.task)
    return {
        "agent_id": payload.agent_id,
        "task": payload.task,
        "status": "completed",
        "result": result
    }


@router.post("/writer", summary="Execute WriterAgent for content generation")
async def execute_writer(request: WriterRequest) -> Dict[str, Any]:
    """
    Generate content using the WriterAgent powered by Google Gemini.

    - **prompt**: The content prompt or question
    - **temperature**: Creativity level (0.0-1.0)
    - **max_tokens**: Maximum response length
    - **chain_of_thought**: Optional reasoning prefix
    """
    result = await writer.act(
        chain_of_thought=request.chain_of_thought,
        prompt=request.prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return {
        "agent_id": "writer",
        "prompt": request.prompt,
        "status": "completed",
        "result": result
    }
