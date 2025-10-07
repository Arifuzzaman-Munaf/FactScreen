from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = "FactScreen API"
    version: str = "0.1.0"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    request_timeout: int = 15
    
    # add API keys here if you later use external providers
    google_fact_check_key: str | None = os.getenv("GOOGLE_FC_KEY")

settings = Settings()