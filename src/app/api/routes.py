# Import FastAPI modules for routing and error handling
from fastapi import APIRouter, HTTPException

# Import Pydantic models for claim-related API requests and responses
from src.app.models.claim_models import (
    ClaimRequest,  # Request model for claim search
    ClaimResponse,  # Response model for a single claim
    ClaimsListResponse,  # Response model for list of claims
    FilteredClaimsRequest,  # Request model for filtered claim search
    FilteredClaimsResponse,  # Response model for filtered claims
    FilteredClaimResponse,  # Response model for a single filtered claim
)

# Import services for claim extraction, similarity filtering, and classification
from src.app.services.claim_extract import ClaimExtractionService
from src.pipelines.feature_eng_pipeline import SimilarityFilterService
from src.pipelines.inference_pipeline import ClaimClassificationService

# Initialize API router
router = APIRouter()

# Initialize services for API endpoints
claim_extraction_service = ClaimExtractionService()
similarity_filter_service = SimilarityFilterService()
classification_service = ClaimClassificationService()


# Health check endpoint to check if the API is running
@router.get("/health", tags=["meta"])
async def health():
    return {"status": "ok"}


@router.post("/claims/search", response_model=ClaimsListResponse, tags=["claims"])
async def search_claims(request: ClaimRequest):
    """
    Search for claims from multiple fact-checking sources

    args:
    - request: ClaimRequest - Request model for claim search
    returns:
    - ClaimsListResponse - Response model for list of claims
    - HTTPException - Exception if error occurs
    """
    try:
        # Get combined claims from all sources
        combined_claims = claim_extraction_service.get_combined_claims(
            query=request.query,  # Search query for claims
            language_code=request.language_code,  # Language code for claims
            page_size=request.page_size,  # Page size for claims
        )

        # Convert claims to response format
        claim_responses = [ClaimResponse(**claim) for claim in combined_claims]

        # Return response with claims and total count
        return ClaimsListResponse(
            claims=claim_responses, total_count=len(claim_responses), query=request.query
        )

    # Exception handling for error searching claims
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching claims: {str(e)}")


@router.post("/claims/filtered", response_model=FilteredClaimsResponse, tags=["claims"])
async def get_filtered_claims(request: FilteredClaimsRequest):
    """
    Search for claims and filter them by similarity and assign classification labels.

    args:
    - request: FilteredClaimsRequest - Request model for filtered claim search
    returns:
    - FilteredClaimsResponse - Response model for filtered claims
    - HTTPException - Exception if error occurs
    """
    try:
        # Get combined claims from all sources
        combined_claims = claim_extraction_service.get_combined_claims(
            query=request.query,  # Search query for claims
            language_code=request.language_code,  # Language code for claims
            page_size=request.page_size,  # Page size for claims
        )

        # Filter claims by similarity to the query using sentence transformers
        filtered_claims = similarity_filter_service.filter_claims_by_similarity(
            claims=combined_claims,
            query=request.query,  # Search query for claims
            similarity_threshold=request.similarity_threshold,  # Similarity threshold for claims
        )

        # Classify claims using a transformer model
        classified_claims = classification_service.classify_claims_batch(filtered_claims)

        # Convert classified claims to response format
        claim_responses = [FilteredClaimResponse(**claim) for claim in classified_claims]

        # Return response with filtered and classified claims
        return FilteredClaimsResponse(
            claims=claim_responses,
            total_count=len(claim_responses),
            query=request.query,
            similarity_threshold=request.similarity_threshold,
            classification_labels=classification_service.get_classification_labels(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing filtered claims: {str(e)}")
