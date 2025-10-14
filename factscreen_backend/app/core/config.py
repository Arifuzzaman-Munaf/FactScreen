# app/core/config.py

from typing import List, Optional
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings  # <-- v2-compatible

class Settings(BaseSettings):
    # Application metadata and CORS
    app_name: str = "FactScreen API"
    version: str = "0.1.0"
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]  # Allowed frontend origins
    request_timeout: int = 15  # Default timeout (seconds) for HTTP requests out

    # Google Fact Check API configuration
    google_api_key: Optional[str] = None
    google_factcheck_url: Optional[AnyHttpUrl] = None
    google_factcheck_endpoint: Optional[str] = None

    # RapidAPI Fact Checker configuration
    fact_checker_api_key: Optional[str] = None
    fact_checker_url: Optional[str] = None  # Hostname or full URL
    fact_checker_endpoint: Optional[str] = None

    # ClaimBuster API configuration
    claim_buster_api_key: Optional[str] = None
    claim_buster_url: Optional[AnyHttpUrl] = None
    claim_buster_endpoint: Optional[str] = None

    class Config:
        # Loads variables from .env file in UTF-8 encoding
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance for import throughout the app
settings = Settings()