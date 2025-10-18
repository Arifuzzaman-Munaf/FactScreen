from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Request model for initiating a claim search
class ClaimRequest(BaseModel):
    # The claim/query text the user wants to fact-check
    query: str = Field(..., description="The claim text to search for", min_length=1)
    # Language code for searching claims (default is "en")
    language_code: str = Field(default="en", description="Language code for the search")
    # Maximum number of results to return in the search
    page_size: int = Field(default=10, description="Number of results to return", ge=1, le=50)

# Response model for an individual claim result retrieved from a fact-check source
class ClaimResponse(BaseModel):
    # The text of the claim reported by the source
    claim: Optional[str] = Field(None, description="The claim text")
    # The person or entity reported to have made the claim
    claimant: Optional[str] = Field(None, description="Who made the claim")
    # Date on which the claim was made (if available)
    claim_date: Optional[str] = Field(None, description="Date when the claim was made")
    # Publisher/source that performed the fact-check
    publisher: Optional[str] = Field(None, description="Publisher of the fact-check")
    # Link to the full fact-check review article/webpage
    review_link: Optional[str] = Field(None, description="Link to the fact-check review")
    # The verdict/rating given by the fact-checker (e.g. "True", "False")
    rating: Optional[str] = Field(None, description="Fact-check rating")
    # The API/source from which this particular claim entry was retrieved
    source_api: str = Field(..., description="Source API that provided this claim")
    # Any additional data/metadata included with the claim from the source
    other: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

# Response model wrapping a batch/list of claims and the original query
class ClaimsListResponse(BaseModel):
    # List of claims matching the user's query
    claims: List[ClaimResponse] = Field(..., description="List of claims")
    # The total number of claims returned
    total_count: int = Field(..., description="Total number of claims found")
    # Copy of the user's search query
    query: str = Field(..., description="Original search query")

# Extended response model for an individual filtered/classified claim
class FilteredClaimResponse(ClaimResponse):
    # Score representing semantic similarity between this claim and the query in [0.0, 1.0]
    query_similarity_score: float = Field(..., description="Similarity score with the query", ge=0.0, le=1.0)
    # Normalized rating/classification label for the claim (e.g. "SUPPORTED", "REFUTED", etc.)
    normalized_rating: str = Field(..., description="Normalized classification result")

# Response model wrapping filtered/classified claims and metadata about the filtering 
class FilteredClaimsResponse(BaseModel):
    # List of claims that passed filtering and classification
    claims: List[FilteredClaimResponse] = Field(..., description="List of filtered and classified claims")
    # Total number of claims in the filtered/classified result set
    total_count: int = Field(..., description="Total number of filtered claims")
    # Original user query
    query: str = Field(..., description="Original search query")
    # Similarity threshold used in the filtering step
    similarity_threshold: float = Field(..., description="Similarity threshold used for filtering")
    # List of possible classification labels/ratings produced by the model or defined in the system
    classification_labels: List[str] = Field(..., description="Available classification labels")

# Request model for filtered/classified claims API (adds a similarity threshold filter)
class FilteredClaimsRequest(ClaimRequest):
    # The minimum similarity score required for a claim to be included
    similarity_threshold: float = Field(default=0.75, description="Minimum similarity score", ge=0.0, le=1.0)
