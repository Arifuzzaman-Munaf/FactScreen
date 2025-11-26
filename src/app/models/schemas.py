from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, BaseModel, Field


class InputType(str, Enum):
    TEXT = "text"
    URL = "url"
    IMAGE = "image"


class Verdict(str, Enum):
    TRUE = "true"
    MISLEADING = "misleading"
    UNKNOWN = "unknown"


class ProviderName(str, Enum):
    GOOGLE = "google_factcheck"
    RAPID = "rapidapi_fact_checker"
    CLAIMBUSTER = "claimbuster"


class ProviderResult(BaseModel):
    provider: ProviderName
    verdict: Verdict
    rating: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    source_url: Optional[AnyHttpUrl] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AggregatedResult(BaseModel):
    claim_text: str
    verdict: Verdict
    votes: Dict[Verdict, int]
    provider_results: List[ProviderResult]
    providers_checked: List[ProviderName] = Field(default_factory=list)
    confidence: float = 0.0


class TextValidateRequest(BaseModel):
    text: str = Field(min_length=1)


class UrlValidateRequest(BaseModel):
    url: AnyHttpUrl


class ImageValidateRequest(BaseModel):
    image_base64: str = Field(description="Base64-encoded image content")


class ValidateResponse(BaseModel):
    result: AggregatedResult


# Compatibility with existing routes expecting generic analyze endpoint
class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[AnyHttpUrl] = None
    image_base64: Optional[str] = None


class AnalyzeResponse(BaseModel):
    result: AggregatedResult


class Evidence(BaseModel):
    snippet: str
    source: Optional[str] = None
    url: Optional[str] = None


class ProviderRating(BaseModel):
    provider: str
    rating: Optional[str] = None
    label: Optional[str] = None  # "True" | "False" | "Unclear"


class AnalyzeResponseDetailed(BaseModel):
    claim: str
    label: str  # "True" | "False" | "Unclear"
    rating: Optional[str] = None  # e.g., "Misleading", "Accurate", provider-style text rating
    confidence: float
    evidence: List[Evidence]
    providers: Optional[List[ProviderRating]] = None
    explanation: Optional[str] = None
