from __future__ import annotations

from typing import Any, Dict, List

from src.agents.base.agent import BaseAgent
from src.agents.planner import PlannerAgent
from src.tools.llm import get_gemini_client
from src.config.logging_config import get_logger


class OrchestratorAgent(BaseAgent):
    """Coordinates planner and specialized agents using Gemini for orchestration."""

    def __init__(self, planner: PlannerAgent) -> None:
        super().__init__(
            name="orchestrator",
            role="Coordinator",
            capabilities=["plan", "delegate", "synthesize"],
        )
        self.planner = planner
        self.logger = get_logger(agent_name=self.name, agent_role=self.role)

    async def think(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        # Include original task in planner output so act() can access it
        plan = await self.planner.act(task, task=task)
        if isinstance(plan, dict):
            plan.setdefault("original_task", task)
        return plan

    async def act(self, chain_of_thought: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        task = kwargs.get("task") or chain_of_thought.get("original_task") or chain_of_thought.get("task", "")
        
        try:
            gemini = get_gemini_client()
            
            # First, get the plan from the planner
            plan_result = chain_of_thought or {}
            plan_text = plan_result.get("plan_details", "") if isinstance(plan_result, dict) else str(plan_result)
            plan_steps = []
            if isinstance(plan_result, dict):
                steps = plan_result.get("steps") or plan_result.get("plan", {}).get("steps")
                if isinstance(steps, list):
                    plan_steps = steps[:10]
            
            # Use Gemini to synthesize a comprehensive solution
            synthesis_prompt = f"""You are an expert orchestrator coordinating multiple agents to solve a complex task.

Original Task: {task}

Proposed Plan:
{plan_text}

Now synthesize a comprehensive solution that:
1. Validates the plan
2. Identifies potential dependencies and risks
3. Suggests optimizations
4. Provides a final action summary

Provide a detailed synthesis that incorporates insights from planning agents."""
            
            response = await gemini.generate_content(
                prompt=synthesis_prompt,
                temperature=0.35,  # Balanced, slightly concise
                max_tokens=700,
                system_instruction="You are an expert orchestration agent. Return a concise synthesis (max ~8 bullets) and a short summary."
            )
            
            synthesis_text = response.get("text", "")
            
            await self.memory.add({
                "task": task,
                "plan": plan_result,
                "synthesis": synthesis_text,
                "model": response.get("model"),
                "usage": response.get("usage"),
            })
            
            return {
                "status": "completed",
                "task": task,
                "plan": {
                    "task": task,
                    "steps": plan_steps,
                    "plan_details": plan_text,
                },
                "synthesis": synthesis_text,
                "coordination_summary": "Multi-agent coordination successful"
            }
            
        except Exception as exc:
            self.logger.error("OrchestratorAgent failed", error=str(exc))
            # Fallback to simple coordination
            await self.memory.add({
                "task": task,
                "error": str(exc)
            })
            
            return {
                "status": "completed",
                "task": task,
                "plan": await self.planner.act(task, task=task),
                "synthesis": f"Fallback orchestration (Gemini unavailable): Coordinating agents for: {task}",
                "coordination_summary": "Fallback coordination mode"
            }
