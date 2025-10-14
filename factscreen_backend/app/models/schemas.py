from typing import Optional, List
from pydantic import BaseModel, HttpUrl

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[HttpUrl] = None

class Evidence(BaseModel):
    snippet: str
    source: Optional[str] = None
    url: Optional[str] = None

class AnalyzeResponse(BaseModel):
    claim: str
    label: str                  # "True" | "False" | "Unclear"
    confidence: float
    evidence: List[Evidence]
    explanation: Optional[str] = None