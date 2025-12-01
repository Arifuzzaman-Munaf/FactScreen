from pathlib import Path
from typing import Any, Dict, List

import os
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _load_local_yaml() -> Dict[str, Any]:
    """
    Load static configuration from config/local.yaml.
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
_CLASSIFY_CFG = _section("classification")
_SERVER_CFG = _section("server")
_LOGGING_CFG = _section("logging")
_SECRETS_CFG = _section("secrets")
_SENTIMENT_CFG = _section("sentiment")

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

    # Application settings (static parts come from YAML only)
    app_name: str = _APP_CFG.get("name")
    version: str = _APP_CFG.get("version")
    cors_origins: List[str] = _APP_CFG.get("cors_origins")
    request_timeout: int = _APP_CFG.get("request_timeout")

    # Server settings (used by entrypoint/server.py for uvicorn)
    # PORT env var can be set for production deployments
    # For local development: uses config/local.yaml or defaults
    server_host: str = Field(
        default=_SERVER_CFG.get("host", "0.0.0.0"),
        alias="HOST"
    )
    # PORT env var is read directly by pydantic from environment
    # If not set, falls back to config/local.yaml or default 8000
    server_port: int = Field(
        default=_SERVER_CFG.get("port", 8000),
        alias="PORT"
    )

    # Logging settings
    log_level: str = _LOGGING_CFG.get("level")
    log_dir: str = _LOGGING_CFG.get("dir")
    log_file: str = _LOGGING_CFG.get("file")

    # Google Fact Check API settings
    # API key is secret -> from env; URL/endpoint are static -> from YAML
    # NOTE: the env var names used here are defined in config/local.yaml under `secrets`.
    google_api_key: str = Field(default="", alias=_GOOGLE_API_ENV)
    google_factcheck_url: str = Field(
        default=_GOOGLE_CFG.get("url"),
        alias="GOOGLE_FACTCHECK_URL",
    )
    google_factcheck_endpoint: str = Field(
        default=_GOOGLE_CFG.get("endpoint"),
        alias="GOOGLE_FACTCHECK_ENDPOINT",
    )
    google_factcheck_language_code: str = _GOOGLE_CFG.get("language_code", "en")
    google_factcheck_page_size: int = _GOOGLE_CFG.get("page_size", 1)

    # RapidAPI Fact Checker settings
    fact_checker_api_key: str = Field(default="", alias=_FACTCHECK_API_ENV)
    fact_checker_url: str = Field(
        default=_RAPID_CFG.get("url"),
        alias="FACT_CHECKER_URL",
    )
    fact_checker_endpoint: str = Field(
        default=_RAPID_CFG.get("endpoint"),
        alias="FACT_CHECKER_ENDPOINT",
    )
    fact_checker_host: str = Field(
        default=_RAPID_CFG.get("host"),
        alias="FACT_CHECKER_HOST",
    )
    fact_checker_limit: int = _RAPID_CFG.get("limit", 20)
    fact_checker_offset: int = _RAPID_CFG.get("offset", 0)
    fact_checker_language: str = _RAPID_CFG.get("language", "en")

    # ML Model settings
    similarity_threshold: float = Field(
        default=_ML_CFG.get("similarity_threshold"),
        alias="SIMILARITY_THRESHOLD",
    )
    sentence_transformer_model: str = Field(
        default=_ML_CFG.get("sentence_transformer_model"),
        alias="SENTENCE_TRANSFORMER_MODEL",
    )
    classification_model: str = Field(
        default=_ML_CFG.get("classification_model"),
        alias="CLASSIFICATION_MODEL",
    )

    # Claim classification vocab/labels (static config)
    classification_candidate_labels: List[str] = _CLASSIFY_CFG.get("candidate_labels")
    classification_true_keywords: List[str] = _CLASSIFY_CFG.get("true_keywords")
    classification_false_keywords: List[str] = _CLASSIFY_CFG.get("false_keywords")
    classification_no_info_keywords: List[str] = _CLASSIFY_CFG.get("no_info_keywords")

    # Gemini API settings
    gemini_api_key: str = Field(default="", alias=_GEMINI_API_ENV)
    gemini_model: str = Field(
        default=_GEMINI_CFG.get("model"),
        alias="GEMINI_MODEL",
    )

    # Sentiment analysis settings
    sentiment_model_id: str = _SENTIMENT_CFG.get(
        "model_id", "distilbert-base-uncased-finetuned-sst-2-english"
    )
    sentiment_model_dir: str = _SENTIMENT_CFG.get("model_dir", "src/app/models/distilbert-sst2")
    sentiment_max_length: int = _SENTIMENT_CFG.get("max_length", 256)
    sentiment_unclear_threshold: float = _SENTIMENT_CFG.get("unclear_threshold", 0.1)
    sentiment_default_unclear_confidence: float = _SENTIMENT_CFG.get(
        "default_unclear_confidence", 0.5
    )
    sentiment_unclear_confidence: float = _SENTIMENT_CFG.get("unclear_confidence", 0.55)
    sentiment_min_confidence: float = _SENTIMENT_CFG.get("min_confidence", 0.6)
    sentiment_max_confidence: float = _SENTIMENT_CFG.get("max_confidence", 0.95)


# Instantiate the settings object to be used throughout the application
settings = Settings()