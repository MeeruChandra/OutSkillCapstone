from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings following Single Responsibility Principle.
    Manages all configuration from environment variables.
    """
    database_url: str = "sqlite:///./ecommerce.db"
    secret_key: str = "dev-secret-key-change-in-production-must-be-at-least-32-characters-long"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Dependency injection for settings.
    Cached to avoid reading .env multiple times.
    """
    return Settings()
