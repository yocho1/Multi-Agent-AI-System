from __future__ import annotations

from typing import Any, Dict, List

from src.agents.base.agent import BaseAgent
from src.agents.planner import PlannerAgent
from src.agents.specialized import WriterAgent
from src.agents.weather import WeatherAgent
from src.tools.llm import get_gemini_client
from src.config.logging_config import get_logger


class OrchestratorAgent(BaseAgent):
    """Coordinates planner and specialized agents using Gemini for orchestration."""

    def __init__(self, planner: PlannerAgent, writer: WriterAgent | None = None, weather: WeatherAgent | None = None) -> None:
        super().__init__(
            name="orchestrator",
            role="Coordinator",
            capabilities=["plan", "delegate", "synthesize"],
        )
        self.planner = planner
        self.writer = writer
        self.weather = weather
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

            # Gather plan
            plan_result = chain_of_thought or {}
            plan_text = plan_result.get("plan_details", "") if isinstance(plan_result, dict) else str(plan_result)
            plan_steps: list[str] = []
            if isinstance(plan_result, dict):
                steps = plan_result.get("steps") or plan_result.get("plan", {}).get("steps")
                if isinstance(steps, list):
                    plan_steps = steps[:10]

            # Collect contributions from available agents
            writer_result = None
            if self.writer:
                writer_prompt = (
                    f"Task: {task}\n"
                    f"Plan summary: {plan_text}\n"
                    "Write a concise, user-friendly output that blends planning insights with actionable guidance."
                )
                writer_result = await self.writer.act(task, prompt=writer_prompt, temperature=0.4, max_tokens=400)

            weather_result = None
            location = kwargs.get("location") or kwargs.get("city")
            if self.weather and location:
                weather_result = await self.weather.act(task, location=location)

            # Synthesize final answer using Gemini, referencing other agents' outputs
            synthesis_prompt = f"""You are an expert orchestrator combining multiple agents' insights.

Original Task: {task}

Plan:
{plan_text}

Writer Insight:
{writer_result or "(not provided)"}

Weather Insight (if relevant):
{weather_result or "(not requested)"}

Compose a single response that blends the best of the plan, writer, and weather (if present). Keep it concise, actionable, and clearly attributed to agent perspectives."""

            response = await gemini.generate_content(
                prompt=synthesis_prompt,
                temperature=0.35,
                max_tokens=700,
                system_instruction="Blend multi-agent insights into one coherent answer with bullet points and a short summary."
            )

            synthesis_text = response.get("text", "")

            await self.memory.add({
                "task": task,
                "plan": plan_result,
                "writer": writer_result,
                "weather": weather_result,
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
                "writer": writer_result,
                "weather": weather_result,
                "synthesis": synthesis_text,
                "coordination_summary": "Multi-agent answer blended from planner, writer, and weather (when provided).",
            }

        except Exception as exc:
            self.logger.error("OrchestratorAgent failed", error=str(exc))
            await self.memory.add({"task": task, "error": str(exc)})
            return {
                "status": "completed",
                "task": task,
                "plan": await self.planner.act(task, task=task),
                "synthesis": f"Fallback orchestration (Gemini unavailable): Coordinating agents for: {task}",
                "coordination_summary": "Fallback coordination mode",
            }
