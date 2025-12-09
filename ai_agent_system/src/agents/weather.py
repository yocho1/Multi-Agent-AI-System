from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode
from urllib.request import urlopen

from src.agents.base.agent import BaseAgent
from src.config.logging_config import get_logger

logger = get_logger(component="weather_agent")


@dataclass
class WeatherResult:
    location: str
    latitude: float
    longitude: float
    temperature_c: Optional[float]
    precipitation_mm: Optional[float]
    wind_speed_kmh: Optional[float]
    daily: list[Dict[str, Any]]
    provider: str = "open-meteo"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "temperature_c": self.temperature_c,
            "precipitation_mm": self.precipitation_mm,
            "wind_speed_kmh": self.wind_speed_kmh,
            "daily": self.daily,
            "provider": self.provider,
        }


async def _fetch_json(url: str) -> Dict[str, Any]:
    def _blocking() -> Dict[str, Any]:
        with urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))

    return await asyncio.to_thread(_blocking)


class WeatherAgent(BaseAgent):
    """Weather lookup agent using real Open-Meteo data (no API key required)."""

    async def think(self, task: str, **kwargs: Any) -> str:
        location = kwargs.get("location") or task
        return f"Weather lookup for: {location}"

    async def act(self, chain_of_thought: str, **kwargs: Any) -> Dict[str, Any]:
        location = kwargs.get("location") or chain_of_thought
        try:
            if not location:
                raise ValueError("Location is required")

            geo_url = "https://geocoding-api.open-meteo.com/v1/search?" + urlencode(
                {"name": location, "count": 1, "language": "en"}
            )
            geo = await _fetch_json(geo_url)
            first = (geo.get("results") or [None])[0]
            if not first:
                raise ValueError("Location not found")

            lat = first.get("latitude")
            lon = first.get("longitude")
            resolved_name = first.get("name") or location

            forecast_url = "https://api.open-meteo.com/v1/forecast?" + urlencode(
                {
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,precipitation,wind_speed_10m",
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                    "forecast_days": 3,
                    "timezone": "auto",
                }
            )
            forecast = await _fetch_json(forecast_url)

            current = forecast.get("current", {})
            daily = forecast.get("daily", {})
            days = []
            for i, date in enumerate(daily.get("time", [])[:3]):
                days.append(
                    {
                        "date": date,
                        "temp_max_c": (daily.get("temperature_2m_max") or [None])[i],
                        "temp_min_c": (daily.get("temperature_2m_min") or [None])[i],
                        "precip_mm": (daily.get("precipitation_sum") or [None])[i],
                    }
                )

            result = WeatherResult(
                location=resolved_name,
                latitude=lat,
                longitude=lon,
                temperature_c=current.get("temperature_2m"),
                precipitation_mm=current.get("precipitation"),
                wind_speed_kmh=current.get("wind_speed_10m"),
                daily=days,
            )

            await self.memory.add({"location": resolved_name, "forecast": result.to_dict()})
            return result.to_dict()

        except Exception as exc:  # noqa: BLE001
            logger.error("WeatherAgent failed", error=str(exc))
            await self.memory.add({"error": str(exc), "location": location})
            return {
                "location": location,
                "error": str(exc),
                "provider": "open-meteo",
                "note": "Fallback response; please verify input location.",
            }
