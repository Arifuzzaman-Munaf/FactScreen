from pathlib import Path
from typing import Any, Dict, List

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _load_local_yaml() -> Dict[str, Any]:
    """
    Load static configuration from config/local.yaml.

    This file holds all non-secret/static configuration. API keys and other
    secrets remain in the .env file / environment variables only.
    """
    config_path = Path("config") / "local.yaml"
    if not config_path.exists():
        return {}

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        # Fail gracefully and fall back to in-code defaults
        data = {}
    return data


_YAML_CONFIG = _load_local_yaml()


def _section(name: str) -> Dict[str, Any]:
    return _YAML_CONFIG.get(name, {}) if isinstance(_YAML_CONFIG, dict) else {}


_APP_CFG = _section("app")
_GOOGLE_CFG = _section("google_factcheck")
_RAPID_CFG = _section("rapidapi_fact_checker")
_ML_CFG = _section("ml")
_GEMINI_CFG = _section("gemini")
_SECRETS_CFG = _section("secrets")

_GOOGLE_API_ENV = _SECRETS_CFG.get("google_api_key_env", "GOOGLE_API_KEY")
_FACTCHECK_API_ENV = _SECRETS_CFG.get("fact_checker_api_key_env", "FACT_CHECKER_API_KEY")
_GEMINI_API_ENV = _SECRETS_CFG.get("gemini_api_key_env", "GEMINI_API_KEY")


class Settings(BaseSettings):
    """
    Application settings.

    - Static defaults (URLs, model names, thresholds, etc.) are loaded from
      config/local.yaml.
    - Secrets such as API keys are loaded from the environment / .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",  # Load environment variables from .env file
        env_file_encoding="utf-8",  # Use UTF-8 encoding for .env file
        env_prefix="",  # No prefix required for environment variables
        extra="ignore",  # Ignore extra environment variables not defined in the model
    )

    # Application settings (static parts come from YAML)
    app_name: str = _APP_CFG.get("name", "FactScreen API")
    version: str = _APP_CFG.get("version", "0.1.0")
    cors_origins: List[str] = _APP_CFG.get(
        "cors_origins",
        [
            "http://localhost:5173",
            "http://localhost:3000",
        ],
    )
    request_timeout: int = _APP_CFG.get("request_timeout", 15)

    # Google Fact Check API settings
    # API key is secret -> from env; URL/endpoint are static -> from YAML
    # NOTE: the env var names used here are defined in config/local.yaml under `secrets`.
    google_api_key: str = Field(default="", alias=_GOOGLE_API_ENV)
    google_factcheck_url: str = Field(
        default=_GOOGLE_CFG.get("url", "https://factchecktools.googleapis.com"),
        alias="GOOGLE_FACTCHECK_URL",
    )
    google_factcheck_endpoint: str = Field(
        default=_GOOGLE_CFG.get("endpoint", "v1alpha1/claims:search"),
        alias="GOOGLE_FACTCHECK_ENDPOINT",
    )

    # RapidAPI Fact Checker settings
    fact_checker_api_key: str = Field(default="", alias=_FACTCHECK_API_ENV)
    fact_checker_url: str = Field(
        default=_RAPID_CFG.get("url", "fact-checker.p.rapidapi.com"),
        alias="FACT_CHECKER_URL",
    )
    fact_checker_endpoint: str = Field(
        default=_RAPID_CFG.get("endpoint", "search"),
        alias="FACT_CHECKER_ENDPOINT",
    )
    fact_checker_host: str = Field(
        default=_RAPID_CFG.get("host", "fact-checker.p.rapidapi.com"),
        alias="FACT_CHECKER_HOST",
    )

    # ML Model settings
    similarity_threshold: float = Field(
        default=_ML_CFG.get("similarity_threshold", 0.15),
        alias="SIMILARITY_THRESHOLD",
    )
    sentence_transformer_model: str = Field(
        default=_ML_CFG.get("sentence_transformer_model", "all-MiniLM-L6-v2"),
        alias="SENTENCE_TRANSFORMER_MODEL",
    )
    classification_model: str = Field(
        default=_ML_CFG.get("classification_model", "facebook/bart-large-mnli"),
        alias="CLASSIFICATION_MODEL",
    )

    # Gemini API settings
    gemini_api_key: str = Field(default="", alias=_GEMINI_API_ENV)
    gemini_model: str = Field(
        default=_GEMINI_CFG.get("model", "gemini-2.5-flash"),
        alias="GEMINI_MODEL",
    )


# Instantiate the settings object to be used throughout the application
settings = Settings()
