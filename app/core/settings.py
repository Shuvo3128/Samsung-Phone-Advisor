"""
Global Settings for Samsung Phone Advisor
Production-ready, env-driven configuration
"""

import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


# ==================================================
# BASE PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

# ==================================================
# ENV-BASED SETTINGS (Pydantic)
# ==================================================

class Settings(BaseSettings):
    # -----------------------------
    # PROJECT META
    # -----------------------------
    PROJECT_NAME: str = "Samsung Phone Advisor"
    PROJECT_MODE: str = Field(default="local", description="local | staging | prod")

    # -----------------------------
    # DATABASE (PostgreSQL)
    # -----------------------------
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "samsung_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # -----------------------------
    # LLM CONFIG
    # -----------------------------
    LLM_PROVIDER: str = Field(default="ollama", description="ollama | openai | azure")

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:1b"

    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 1024

    # -----------------------------
    # RAG CONFIG
    # -----------------------------
    RAG_MODE: str = Field(default="sql", description="sql | hybrid | vector")
    CONFIDENCE_THRESHOLD: float = 0.4

    # -----------------------------
    # MEMORY (future-ready)
    # -----------------------------
    MEMORY_ENABLED: bool = False
    MEMORY_WINDOW: int = 4

    # -----------------------------
    # API / SERVER
    # -----------------------------
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    # -----------------------------
    # STREAMLIT UI
    # -----------------------------
    UI_TITLE: str = "Samsung Phone Advisor"
    UI_ICON: str = "📱"
    UI_LAYOUT: str = "centered"

    # -----------------------------
    # SAFETY
    # -----------------------------
    ALLOW_GUESSING: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton settings object
settings = Settings()
