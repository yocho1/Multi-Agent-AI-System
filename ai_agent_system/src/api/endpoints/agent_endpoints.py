from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from src.agents.orchestrator import OrchestratorAgent
from src.agents.planner import PlannerAgent
from src.agents.specialized import WriterAgent
from src.agents.base.memory import ShortTermMemory
from src.agents.weather import WeatherAgent
from src.utils.firebase_cache import get_firestore_cache
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/agents", tags=["agents"])
security = HTTPBearer()

planner = PlannerAgent(name="planner", role="Task decomposition", capabilities=["plan"])
weather = WeatherAgent(name="weather", role="Weather lookup", capabilities=["forecast"])
writer = WriterAgent(
    name="writer",
    role="Content generation specialist",
    capabilities=["content_generation", "creative_writing", "code_generation"],
    memory=ShortTermMemory()
)
orchestrator = OrchestratorAgent(planner=planner, writer=writer, weather=weather)


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
async def list_agents(user: Dict[str, Any] = Depends(get_current_user)) -> List[Dict[str, Any]]:
    return [
        {"id": "orchestrator", "role": "Coordinator", "capabilities": orchestrator.capabilities},
        {"id": "planner", "role": "Task decomposition", "capabilities": planner.capabilities},
        {"id": "writer", "role": "Content generation specialist", "capabilities": writer.capabilities},
        {"id": "weather", "role": "Weather lookup", "capabilities": weather.capabilities},
    ]


@router.get("/{agent_id}", summary="Get agent details")
async def get_agent(agent_id: str, user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    agents = {
        "orchestrator": {"id": "orchestrator", "role": orchestrator.role},
        "planner": {"id": "planner", "role": planner.role},
        "writer": {"id": "writer", "role": writer.role},
        "weather": {"id": "weather", "role": weather.role},
    }
    if agent_id not in agents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agents[agent_id]


@router.post("/execute", summary="Execute specific agent")
async def execute_agent(payload: AgentExecuteRequest, user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    # Generate cache key from agent_id and task
    cache_key = f"agent:{payload.agent_id}:{hashlib.md5(payload.task.encode()).hexdigest()}"
    
    # Try to get from cache
    cache = get_firestore_cache()
    cached_result = await cache.get_json(cache_key)
    
    if cached_result:
        return {
            "agent_id": payload.agent_id,
            "task": payload.task,
            "status": "completed",
            "result": cached_result,
            "cached": True
        }
    
    # Execute agent based on ID
    params = payload.parameters or {}
    if payload.agent_id == "orchestrator":
        # Orchestrator needs think() first to get chain of thought
        chain_of_thought = await orchestrator.think(payload.task, **params)
        result = await orchestrator.act(chain_of_thought, task=payload.task, **params)
    elif payload.agent_id == "planner":
        result = await planner.act(payload.task, **params)
    elif payload.agent_id == "weather":
        result = await weather.act(payload.task, **params)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    
    # Cache the result for 1 hour
    await cache.set_json(cache_key, result, ttl=3600)
    
    return {
        "agent_id": payload.agent_id,
        "task": payload.task,
        "status": "completed",
        "result": result,
        "cached": False
    }


@router.post("/writer", summary="Execute WriterAgent for content generation")
async def execute_writer(request: WriterRequest, user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Generate content using the WriterAgent powered by Google Gemini.

    - **prompt**: The content prompt or question
    - **temperature**: Creativity level (0.0-1.0)
    - **max_tokens**: Maximum response length
    - **chain_of_thought**: Optional reasoning prefix
    """
    # Generate cache key from prompt and parameters
    cache_data = f"{request.prompt}:{request.temperature}:{request.max_tokens}"
    cache_key = f"writer:{hashlib.md5(cache_data.encode()).hexdigest()}"
    
    # Try to get from cache
    cache = get_firestore_cache()
    cached_result = await cache.get_json(cache_key)
    
    if cached_result:
        return {
            "agent_id": "writer",
            "prompt": request.prompt,
            "status": "completed",
            "result": cached_result,
            "cached": True
        }
    
    # Execute writer agent
    result = await writer.act(
        chain_of_thought=request.chain_of_thought,
        prompt=request.prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    
    # Cache the result for 1 hour
    await cache.set_json(cache_key, result, ttl=3600)
    
    return {
        "agent_id": "writer",
        "prompt": request.prompt,
        "status": "completed",
        "result": result,
        "cached": False
    }
