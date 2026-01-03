"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Tech Blog AI"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    # API
    api_v1_prefix: str = "/api/v1"

    # Google Gemini
    gemini_api_key: str = ""

    # PostgreSQL
    database_url: str = "postgresql://techblog:techblog@localhost:5432/techblog"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # ChromaDB
    chroma_url: str = "http://localhost:8001"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
