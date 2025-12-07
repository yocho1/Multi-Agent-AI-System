from __future__ import annotations

from typing import Any, Dict, Optional

from src.agents.base.agent import BaseAgent
from src.tools.llm import get_gemini_client
from src.config.logging_config import get_logger

logger = get_logger(component="specialized_agents")


class WriterAgent(BaseAgent):
    """Content generation agent using Google Gemini."""

    async def act(self, chain_of_thought: str, **kwargs: Any) -> str:
        prompt = kwargs.get("prompt", chain_of_thought)
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 1024)
        system_instruction = kwargs.get("system_instruction")
        
        try:
            gemini = get_gemini_client()
            response = await gemini.generate_content(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                system_instruction=system_instruction,
            )
            
            result = response.get("text", "")
            await self.memory.add({
                "generated": result,
                "prompt": prompt,
                "model": response.get("model"),
                "usage": response.get("usage"),
            })
            return result
            
        except Exception as exc:
            logger.error("WriterAgent failed", error=str(exc))
            # Fallback to mock response
            result = f"[Gemini unavailable] Generated content for: {prompt}"
            await self.memory.add({"generated": result, "error": str(exc)})
            return result


class FlightAgent(BaseAgent):
    """Flight booking specialist with mock API integration."""

    async def act(self, chain_of_thought: str, **kwargs: Any) -> Dict[str, Any]:
        origin = kwargs.get("origin", "LAX")
        destination = kwargs.get("destination", "JFK")
        result = {
            "flights": [
                {"id": "AA123", "departure": "10:00", "arrival": "18:00", "price": 250},
                {"id": "AA456", "departure": "14:00", "arrival": "22:00", "price": 220},
            ],
            "origin": origin,
            "destination": destination,
        }
        await self.memory.add({"flight_search": result})
        return result


class WeatherAgent(BaseAgent):
    """Weather checking specialist with mock data."""

    async def act(self, chain_of_thought: str, **kwargs: Any) -> Dict[str, Any]:
        location = kwargs.get("location", "New York")
        result = {
            "location": location,
            "temperature": 72,
            "condition": "Sunny",
            "humidity": 60,
        }
        await self.memory.add({"weather": result})
        return result


class CodeAgent(BaseAgent):
    """Code generation and execution specialist."""

    async def act(self, chain_of_thought: str, **kwargs: Any) -> Dict[str, Any]:
        # Placeholder: integrate with code executor later
        code_task = kwargs.get("code_task", chain_of_thought)
        result = {
            "task": code_task,
            "generated_code": "# TODO: implement",
            "execution": "pending",
        }
        await self.memory.add({"code_generation": result})
        return result
