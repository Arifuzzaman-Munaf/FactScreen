# Import FastAPI modules for routing and error handling
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

# Import Pydantic models for claim-related API requests and responses
from src.app.models.claim_models import (
    ClaimRequest,  # Request model for claim search
    ClaimResponse,  # Response model for a single claim
    ClaimsListResponse,  # Response model for list of claims
    FilteredClaimsRequest,  # Request model for filtered claim search
    FilteredClaimsResponse,  # Response model for filtered claims
    FilteredClaimResponse,  # Response model for a single filtered claim
)
from src.app.models.schemas import AnalyzeRequest, AggregatedResult, ValidateResponse

# Import services for claim extraction, similarity filtering, and classification
from src.app.services.claim_extract import ClaimExtractionService
from src.app.services.report import generate_pdf_report
from src.pipelines.feature_eng_pipeline import SimilarityFilterService
from src.pipelines.inference_pipeline import ClaimClassificationService
from src.pipelines.validation_pipeline import validate_text, validate_url

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
    Args:
        request: ClaimRequest - Request model for claim search
    Returns:
        ClaimsListResponse - Response model for list of claims
        HTTPException - Exception if error occurs
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

    Args:
        request: FilteredClaimsRequest - Request model for filtered claim search
    Returns:
        FilteredClaimsResponse - Response model for filtered claims
        HTTPException - Exception if error occurs
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


@router.post("/validate", response_model=ValidateResponse, tags=["validation"])
async def validate_claim(request: AnalyzeRequest):
    """
    Validate a claim using third-party fact-checkers and Gemini explanations.

    The request can include either `text`, or `url`.
    Args:
        request: AnalyzeRequest - Request model for claim validation
    Returns:
        ValidateResponse - Response model for claim validation
        HTTPException - Exception if error occurs
    """
    # if the request does not include any of the required fields, raise an error
    if not (request.text or request.url):
        raise HTTPException(
            status_code=400, detail="Provide at least one of text or url"
        )

    try:
        # if the request includes text, validate the text
        if request.text:
            result = await validate_text(request.text)
        # if the request includes url, validate the url
        elif request.url:
            result = await validate_url(str(request.url))

        return ValidateResponse(result=result)
    # Exception handling for HTTPException
    except HTTPException:
        raise
    # Exception handling for other exceptions
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"Error validating claim: {exc}")


@router.post("/validate/pdf", tags=["validation"])
async def generate_validation_pdf(request: AnalyzeRequest):
    """
    Validate a claim and generate a PDF report.

    The request can include either `text`, or `url`.
    Args:
        request: AnalyzeRequest - Request model for claim validation
    Returns:
        PDF file as response
        HTTPException - Exception if error occurs
    """
    # if the request does not include any of the required fields, raise an error
    if not (request.text or request.url):
        raise HTTPException(
            status_code=400, detail="Provide at least one of text or url"
        )

    try:
        # if the request includes text, validate the text
        if request.text:
            result = await validate_text(request.text)
        # if the request includes url, validate the url
        elif request.url:
            result = await validate_url(str(request.url))

        # Generate PDF report
        pdf_buffer = generate_pdf_report(result)

        # Return PDF as response
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="factcheck-report-{result.verdict.value}.pdf"'
            },
        )
    # Exception handling for HTTPException
    except HTTPException:
        raise
    # Exception handling for HTTPException
    except HTTPException:
        raise
    # Exception handling for other exceptions
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"Error generating PDF report: {exc}")


@router.post("/report/pdf", tags=["validation"])
async def generate_pdf_from_result(result: AggregatedResult):
    """
    Generate a PDF report from an existing AggregatedResult.

    Args:
        result: AggregatedResult - The fact-checking result to generate PDF from
    Returns:
        PDF file as response
        HTTPException - Exception if error occurs
    """
    try:
        # Generate PDF report
        pdf_buffer = generate_pdf_report(result)

        # Return PDF as response
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="factcheck-report-{result.verdict.value}.pdf"'
            },
        )
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"Error generating PDF report: {exc}")