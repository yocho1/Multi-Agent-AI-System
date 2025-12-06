from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import AnyHttpUrl, Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    APP_NAME: str = "AI Agent System"
    ENV: str = "development"
    OPENAI_API_KEY: str = Field(..., description="OpenAI API Key")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, description="Anthropic API Key")
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn
    BROKER_URL: str
    RESULT_BACKEND: str
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    SECRET_KEY: str = Field(..., description="Secret key for cryptographic uses")
    ALLOWED_ORIGINS: List[str] = Field(default_factory=list)
    PROMETHEUS_MULTIPROC_DIR: Optional[str] = None
    TRACING_ENDPOINT: Optional[AnyHttpUrl] = None

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def validate_openai_key(cls, value: str) -> str:
        if not value.startswith("sk-"):
            raise ValueError("Invalid OpenAI API key format")
        return value

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def split_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [item.strip() for item in value.split(",") if item.strip()]

    @classmethod
    def load(cls) -> "Settings":
        """Load settings from environment."""
        return cls()  # type: ignore[call-arg]


settings = Settings.load()
