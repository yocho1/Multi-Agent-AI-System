from __future__ import annotations

from typing import Any, List, Dict

from src.agents.base.agent import BaseAgent
from src.tools.llm import get_gemini_client
from src.config.logging_config import get_logger

logger = get_logger(component="planner_agent")


class PlannerAgent(BaseAgent):
    """Task decomposition agent using Google Gemini for intelligent planning."""

    async def think(self, task: str, **kwargs: Any) -> str:
        return f"Decompose task: {task}"

    async def act(self, chain_of_thought: str, **kwargs: Any) -> Dict[str, Any]:
        task = kwargs.get("task", "") or chain_of_thought
        
        try:
            gemini = get_gemini_client()
            
            # Use Gemini to intelligently decompose the task
            planning_prompt = f"""You are an expert task planner. Break down the following task into clear, actionable steps.
Return a structured plan with numbered steps.

Task: {task}

Provide a detailed breakdown of steps needed to accomplish this task."""
            
            response = await gemini.generate_content(
                prompt=planning_prompt,
                temperature=0.3,  # Lower temperature for deterministic planning
                max_tokens=2000,
                system_instruction="You are an expert task decomposition agent. Break down complex tasks into clear, actionable steps."
            )
            
            plan_text = response.get("text", "")
            
            # Parse the response into steps
            steps = [step.strip() for step in plan_text.split('\n') if step.strip()]
            
            await self.memory.add({
                "task": task,
                "plan": steps,
                "model": response.get("model"),
                "usage": response.get("usage"),
            })
            
            return {
                "task": task,
                "steps": steps,
                "plan_details": plan_text,
                "status": "completed"
            }
            
        except Exception as exc:
            logger.error("PlannerAgent failed", error=str(exc))
            # Fallback to simple decomposition
            simple_steps = [
                f"Analyze: {task}",
                f"Plan: {task}",
                f"Execute: {task}",
                f"Review: {task}"
            ]
            await self.memory.add({
                "task": task,
                "plan": simple_steps,
                "error": str(exc)
            })
            
            return {
                "task": task,
                "steps": simple_steps,
                "plan_details": "Fallback plan (Gemini unavailable)",
                "status": "completed"
            }
