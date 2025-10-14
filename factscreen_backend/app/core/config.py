from typing import List, Optional
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Settings class for application configuration using Pydantic BaseSettings.
# Loads settings from .env file (if present), environment variables, or defaults below.
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",               # Load environment variables from .env file
        env_file_encoding="utf-8",     # Use UTF-8 encoding for .env file
        env_prefix=""                  # No prefix required for environment variables
    )

    # Application settings
    app_name: str = "FactScreen API"   # Name of the application
    version: str = "0.1.0"             # Version of the API
    cors_origins: List[str] = [        # Allowed CORS origins for frontend
        "http://localhost:5173",
        "http://localhost:3000"
    ]
    request_timeout: int = 15          # Request timeout in seconds

    # Google Fact Check API settings
    google_api_key: Optional[str] = Field(default=None, alias="GOOGLE_API_KEY")                
    google_factcheck_url: Optional[AnyHttpUrl] = Field(default=None, alias="GOOGLE_FACTCHECK_URL")  
    google_factcheck_endpoint: Optional[str] = Field(default=None, alias="GOOGLE_FACTCHECK_ENDPOINT")

    # RapidAPI Fact Checker settings
    fact_checker_api_key: Optional[str] = Field(default=None, alias="FACT_CHECKER_API_KEY")     
    fact_checker_url: Optional[str] = Field(default=None, alias="FACT_CHECKER_URL")             
    fact_checker_endpoint: Optional[str] = Field(default=None, alias="FACT_CHECKER_ENDPOINT")   

    # ClaimBuster API settings
    claim_buster_api_key: Optional[str] = Field(default=None, alias="CLAIM_BUSTER_API_KEY")     
    claim_buster_url: Optional[AnyHttpUrl] = Field(default=None, alias="CLAIM_BUSTER_URL")      
    claim_buster_endpoint: Optional[str] = Field(default=None, alias="CLAIM_BUSTER_ENDPOINT")   

# Instantiate the settings object to be used throughout the application
settings = Settings()
