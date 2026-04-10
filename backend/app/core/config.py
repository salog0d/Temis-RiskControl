from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve root .env regardless of where uvicorn is launched from
_ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    app_name: str = "Temis RiskControl API"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./temis.db"
    agent_service_url: str = "http://agent:8001"

    # SMTP — used by the enforcement notification service
    smtp_host: str = "smtp.mailgun.org"
    smtp_port: int = 587
    smtp_use_tls: bool = True
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_address: str = "noreply@temis.io"

    model_config = SettingsConfigDict(env_file=str(_ROOT_ENV), env_file_encoding="utf-8")


settings = Settings()
