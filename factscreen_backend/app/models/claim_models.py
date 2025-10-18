from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ClaimRequest(BaseModel):
    """Request model for claim search"""
    query: str = Field(..., description="The claim text to search for", min_length=1)
    language_code: str = Field(default="en", description="Language code for the search")
    page_size: int = Field(default=10, description="Number of results to return", ge=1, le=50)


class ClaimResponse(BaseModel):
    """Response model for individual claim"""
    claim: Optional[str] = Field(None, description="The claim text")
    claimant: Optional[str] = Field(None, description="Who made the claim")
    claim_date: Optional[str] = Field(None, description="Date when the claim was made")
    publisher: Optional[str] = Field(None, description="Publisher of the fact-check")
    review_link: Optional[str] = Field(None, description="Link to the fact-check review")
    rating: Optional[str] = Field(None, description="Fact-check rating (e.g., 'True', 'False')")
    source_api: str = Field(..., description="Source API that provided this claim")
    other: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ClaimsListResponse(BaseModel):
    """Response model for list of claims"""
    claims: List[ClaimResponse] = Field(..., description="List of claims")
    total_count: int = Field(..., description="Total number of claims found")
    query: str = Field(..., description="Original search query")


class FilteredClaimResponse(ClaimResponse):
    """Extended response model for filtered and classified claims"""
    query_similarity_score: float = Field(..., description="Similarity score with the query", ge=0.0, le=1.0)
    normalized_rating: str = Field(..., description="Normalized classification result")


class FilteredClaimsResponse(BaseModel):
    """Response model for filtered and classified claims"""
    claims: List[FilteredClaimResponse] = Field(..., description="List of filtered and classified claims")
    total_count: int = Field(..., description="Total number of filtered claims")
    query: str = Field(..., description="Original search query")
    similarity_threshold: float = Field(..., description="Similarity threshold used for filtering")
    classification_labels: List[str] = Field(..., description="Available classification labels")


class FilteredClaimsRequest(ClaimRequest):
    """Request model for filtered claims with classification"""
    similarity_threshold: float = Field(default=0.75, description="Minimum similarity score", ge=0.0, le=1.0)
