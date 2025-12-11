from __future__ import annotations

from typing import Optional

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.config.logging_config import get_logger
from src.config.settings import settings


class ClientManager:
    """Manages persistent connections to Redis and PostgreSQL."""

    def __init__(self) -> None:
        self.redis: Optional[Redis] = None
        self.db_engine: Optional[AsyncEngine] = None
        self.logger = get_logger(component="client_manager")

    async def initialize(self) -> None:
        """Initialize all client connections."""
        # Only initialize Redis if URL is configured
        if settings.REDIS_URL:
            try:
                self.redis = Redis.from_url(str(settings.REDIS_URL))
                await self.redis.ping()
                self.logger.info("redis initialized")
            except Exception as exc:  # noqa: BLE001
                self.logger.error("redis init failed", error=str(exc))
                self.redis = None
        else:
            self.logger.info("redis not configured, skipping initialization")

        # Only initialize database if URL is configured
        if settings.DATABASE_URL:
            try:
                self.db_engine = create_async_engine(
                    str(settings.DATABASE_URL),
                    echo=settings.ENV == "development",
                    pool_pre_ping=True,
                )
                async with self.db_engine.connect() as conn:
                    from sqlalchemy import text
                    await conn.execute(text("SELECT 1"))
                self.logger.info("database initialized")
            except Exception as exc:  # noqa: BLE001
                self.logger.error("database init failed", error=str(exc))
                self.db_engine = None
        else:
            self.logger.info("database not configured, skipping initialization")

    async def close(self) -> None:
        """Close all client connections."""
        if self.redis:
            await self.redis.close()
            self.logger.info("redis closed")
        if self.db_engine:
            await self.db_engine.dispose()
            self.logger.info("database closed")

    async def get_redis(self) -> Optional[Redis]:
        """Get Redis client with lazy initialization."""
        if not self.redis:
            try:
                self.redis = Redis.from_url(settings.REDIS_URL)
                await self.redis.ping()
            except Exception:  # noqa: BLE001
                return None
        return self.redis

    async def get_db_engine(self) -> Optional[AsyncEngine]:
        """Get database engine."""
        return self.db_engine


client_manager = ClientManager()
