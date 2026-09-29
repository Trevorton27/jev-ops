from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JEVOPS_DB_")

    host: str = "localhost"
    port: int = 5433
    user: str = "jevops"
    password: str = "jevops"
    name: str = "jevops"

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JEVOPS_REDIS_")

    host: str = "localhost"
    port: int = 6379
    db: int = 0

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class JevSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JEVOPS_JEV_")

    provider: str = Field(default="mock", description="Provider: mock, typesafe, failure")
    model: str = "jev-latest"
    api_key: str = ""
    timeout: float = 30.0
    max_retries: int = 3


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JEVOPS_SECURITY_")

    api_key_pepper: str = "change-me-in-production"
    cors_origins: list[str] = ["http://localhost:3000"]
    rate_limit_per_minute: int = 60
    max_request_size_bytes: int = 1_048_576  # 1MB


class OtelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JEVOPS_OTEL_")

    enabled: bool = False
    endpoint: str = "http://localhost:4317"
    service_name: str = "jevops-api"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JEVOPS_")

    debug: bool = False
    environment: str = "development"
    log_level: str = "INFO"
    log_format: str = "console"  # "console" or "json"

    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    jev: JevSettings = JevSettings()
    security: SecuritySettings = SecuritySettings()
    otel: OtelSettings = OtelSettings()


def get_settings() -> Settings:
    return Settings()
