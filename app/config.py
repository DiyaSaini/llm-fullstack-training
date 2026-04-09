"""
Application configuration.

Loads all settings from environment variables / .env file.
Import the `settings` singleton anywhere in the app — never read
os.environ directly outside this module.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings object populated from .env at startup."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    llm_api_key: str = ""
    app_env: str = "development"
    log_level: str = "INFO"
    app_title: str = "AI Text Processing API"
    app_version: str = "1.0.0"


# Module-level singleton — import this everywhere.
# # llm_api_key is populated from the environment at runtime by pydantic-settings.
settings: Settings = Settings()
