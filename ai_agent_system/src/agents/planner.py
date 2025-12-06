from __future__ import annotations

from typing import Any, List

from src.agents.base.agent import BaseAgent


class PlannerAgent(BaseAgent):
    """Task decomposition agent producing a simple step list."""

    async def think(self, task: str, **kwargs: Any) -> str:
        return f"Decompose task: {task}"

    async def act(self, chain_of_thought: str, **kwargs: Any) -> List[str]:
        # Very simple heuristic decomposition; replace with LLM-driven planner
        task = kwargs.get("task", "") or chain_of_thought
        steps = [f"Analyze: {task}", f"Execute: {task}", f"Summarize: {task}"]
        await self.memory.add({"plan": steps})
        return steps
