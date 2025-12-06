from __future__ import annotations

import asyncio
from typing import Any, Dict

from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.config.settings import settings
from src.config.logging_config import get_logger

logger = get_logger(component="health")


async def check_redis() -> Dict[str, Any]:
    try:
        client = Redis.from_url(str(settings.REDIS_URL))
        await client.ping()
        await client.close()
        return {"redis": "ok"}
    except Exception as exc:  # noqa: BLE001
        logger.warning("redis check failed", error=str(exc))
        return {"redis": f"error: {exc}"}


async def check_database() -> Dict[str, Any]:
    try:
        engine = create_async_engine(str(settings.DATABASE_URL), pool_pre_ping=True)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        await engine.dispose()
        return {"database": "ok"}
    except Exception as exc:  # noqa: BLE001
        logger.warning("database check failed", error=str(exc))
        return {"database": f"error: {exc}"}


async def health_summary() -> Dict[str, Any]:
    redis_task = asyncio.create_task(check_redis())
    db_task = asyncio.create_task(check_database())
    results = await asyncio.gather(redis_task, db_task)
    summary: Dict[str, Any] = {"status": "ok"}
    for result in results:
        summary.update(result)
        for key, value in result.items():
            if isinstance(value, str) and "error" in value:
                summary["status"] = "degraded"
    return summary
