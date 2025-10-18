from typing import List, Optional
from pydantic import Field
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
    google_api_key: str = Field(default="AIzaSyDAjGKxAF5288FSdBX3NIlidJ6G6RYZ784", alias="GOOGLE_API_KEY")                
    google_factcheck_url: str = Field(default="https://factchecktools.googleapis.com", alias="GOOGLE_FACTCHECK_URL")  
    google_factcheck_endpoint: str = Field(default="v1alpha1/claims:search", alias="GOOGLE_FACTCHECK_ENDPOINT")

    # RapidAPI Fact Checker settings
    fact_checker_api_key: str = Field(default="71845686f3msh5f5392bd87453d6p1da3d4jsn3be66bc8c5ae", alias="FACT_CHECKER_API_KEY")     
    fact_checker_url: str = Field(default="fact-checker.p.rapidapi.com", alias="FACT_CHECKER_URL")             
    fact_checker_endpoint: str = Field(default="search", alias="FACT_CHECKER_ENDPOINT")   
    fact_checker_host: str = Field(default="fact-checker.p.rapidapi.com", alias="FACT_CHECKER_HOST")

    # ML Model settings
    similarity_threshold: float = Field(default=0.75, alias="SIMILARITY_THRESHOLD")
    sentence_transformer_model: str = Field(default="all-MiniLM-L6-v2", alias="SENTENCE_TRANSFORMER_MODEL")
    classification_model: str = Field(default="facebook/bart-large-mnli", alias="CLASSIFICATION_MODEL")


# Instantiate the settings object to be used throughout the application
settings = Settings()