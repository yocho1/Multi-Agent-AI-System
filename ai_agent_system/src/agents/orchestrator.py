from __future__ import annotations

from typing import Any, Dict, List

from src.agents.base.agent import BaseAgent
from src.agents.planner import PlannerAgent
from src.config.logging_config import get_logger


class OrchestratorAgent(BaseAgent):
    """Coordinates planner and specialized agents (placeholder)."""

    def __init__(self, planner: PlannerAgent) -> None:
        super().__init__(
            name="orchestrator",
            role="Coordinator",
            capabilities=["plan", "delegate", "synthesize"],
        )
        self.planner = planner
        self.logger = get_logger(agent_name=self.name, agent_role=self.role)

    async def think(self, task: str, **kwargs: Any) -> List[str]:
        return await self.planner.act(task, task=task)

    async def act(self, chain_of_thought: List[str], **kwargs: Any) -> Dict[str, Any]:
        # Placeholder: in future, dispatch to specialized agents in parallel
        results: Dict[str, Any] = {"plan": chain_of_thought}
        await self.memory.add({"orchestrator_plan": chain_of_thought})
        return {"status": "completed", "results": results}
