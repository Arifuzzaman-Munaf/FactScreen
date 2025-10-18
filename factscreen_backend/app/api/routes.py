from fastapi import APIRouter, HTTPException
from app.models.claim_models import (
    ClaimRequest, 
    ClaimResponse, 
    ClaimsListResponse,
    FilteredClaimsRequest,
    FilteredClaimsResponse,
    FilteredClaimResponse
)
from app.services.claim_extract import ClaimExtractionService
from app.services.similarity_filter import SimilarityFilterService
from app.services.claim_classifier import ClaimClassificationService

router = APIRouter()

# Initialize services
claim_extraction_service = ClaimExtractionService()
similarity_filter_service = SimilarityFilterService()
classification_service = ClaimClassificationService()

@router.get("/health", tags=["meta"])
async def health():
    return {"status": "ok"}

@router.post("/claims/search", response_model=ClaimsListResponse, tags=["claims"])
async def search_claims(request: ClaimRequest):
    """
    Search for claims from multiple fact-checking sources
    
    This endpoint fetches claims from Google Fact Check API and RapidAPI Fact-Checker
    and returns them in a standardized format.
    """
    try:
        # Get combined claims from all sources
        combined_claims = claim_extraction_service.get_combined_claims(
            query=request.query,
            language_code=request.language_code,
            page_size=request.page_size
        )
        
        # Convert to response format
        claim_responses = [
            ClaimResponse(**claim) for claim in combined_claims
        ]
        
        return ClaimsListResponse(
            claims=claim_responses,
            total_count=len(claim_responses),
            query=request.query
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching claims: {str(e)}")

@router.post("/claims/filtered", response_model=FilteredClaimsResponse, tags=["claims"])
async def get_filtered_claims(request: FilteredClaimsRequest):
    """
    Search for claims and filter them by similarity and classification
    
    This endpoint:
    1. Fetches claims from multiple fact-checking sources
    2. Filters claims by similarity to the query using sentence transformers
    3. Classifies claims using a transformer model
    4. Returns filtered and classified results
    """
    try:
        # Get combined claims from all sources
        combined_claims = claim_extraction_service.get_combined_claims(
            query=request.query,
            language_code=request.language_code,
            page_size=request.page_size
        )
        
        # Filter by similarity
        filtered_claims = similarity_filter_service.filter_claims_by_similarity(
            claims=combined_claims,
            query=request.query,
            similarity_threshold=request.similarity_threshold
        )
        
        # Classify claims
        classified_claims = classification_service.classify_claims_batch(filtered_claims)
        
        # Convert to response format
        claim_responses = [
            FilteredClaimResponse(**claim) for claim in classified_claims
        ]
        
        return FilteredClaimsResponse(
            claims=claim_responses,
            total_count=len(claim_responses),
            query=request.query,
            similarity_threshold=request.similarity_threshold,
            classification_labels=classification_service.get_classification_labels()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing filtered claims: {str(e)}")