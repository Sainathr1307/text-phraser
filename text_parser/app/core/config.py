from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────────────────────────
    APP_NAME: str = "Text Parser API"
    APP_VERSION: str = "1.0.0"
    ALLOWED_ORIGINS: List[str] = ["*"]

    # ── OpenAI ───────────────────────────────────────────────────────────────
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_TEMPERATURE: float = 0.0   # deterministic output for parsing tasks
    OPENAI_MAX_TOKENS: int = 512

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
