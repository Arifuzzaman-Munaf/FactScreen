from typing import List, Optional
from asyncio import gather
import asyncio

from src.app.models.schemas import (
    AggregatedResult,
    ProviderResult,
    ValidateResponse,
    AnalyzeRequest,
    AnalyzeResponseDetailed,
    Evidence,
    ProviderRating,
    ProviderName,
    Verdict,
)
from src.utils import extract_key_claim, extract_claim
from src.app.services.fetch import (
    fetch_google_factcheck,
    fetch_rapid_factchecker,
    fetch_page_text,
)
from src.app.services.classify import classify_google, classify_rapid
from src.app.services.factcheck import aggregate_results, search_all
from src.app.services.sentiment import analyze_texts_sentiment, sentiment_to_label
from src.app.services.claim_extract import ClaimExtractionService
from src.pipelines.feature_eng_pipeline import SimilarityFilterService
from src.pipelines.inference_pipeline import ClaimClassificationService
from src.app.core.config import settings

_claim_extraction_service = ClaimExtractionService()
_similarity_filter_service = SimilarityFilterService()
_classification_service = ClaimClassificationService()


async def validate_text(text: str) -> AggregatedResult:
    """Validate text using the provider results"""
    claim_for_display = extract_key_claim(text)
    raw_query = text.strip() or claim_for_display
    results = await _get_provider_results(raw_query, page_url=None)

    # Get sources for Gemini explanation
    sources = await search_all(claim_for_display)
    return await aggregate_results(claim_for_display, results, sources)


async def validate_url(url: str) -> AggregatedResult:
    # Ensure URL is properly preserved
    if not url or not url.strip():
        raise ValueError("URL cannot be empty")
    
    url = url.strip()
    
    # Use the URL for Google's pageUrl param to improve hit rate
    claim_source = await _extract_text_from_url(url)
    
    # For URL validation, prefer using the full URL as claim_for_display
    # Only use extracted text if it's meaningful (not empty and longer than just the URL)
    if claim_source and len(claim_source.strip()) > len(url) + 50:
        # Use extracted text if it's substantially longer than the URL
        claim_for_display = extract_key_claim(claim_source)
    else:
        # Use the full URL as the claim
        claim_for_display = url
    
    raw_query = url or claim_for_display
    results = await _get_provider_results(raw_query, page_url=url)

    # Get sources for Gemini explanation - use full URL for better search results
    sources = await search_all(claim_for_display)
    return await aggregate_results(claim_for_display, results, sources)


async def analyze(req) -> ValidateResponse:
    """Generic analyzer that accepts text or url.

    Returns a unified ValidateResponse with the aggregated result.
    """
    if getattr(req, "text", None):
        result = await validate_text(req.text)
    elif getattr(req, "url", None):
        # Get the full URL string - Pydantic v2 AnyHttpUrl uses unicode_string()
        url_str = req.url.unicode_string() if hasattr(req.url, 'unicode_string') else str(req.url)
        result = await validate_url(url_str)
    else:
        # Should be validated at route level, but keep a safe default
        result = await validate_text("")
    return ValidateResponse(result=result)


async def _fetch_all(claim: str, page_url: str | None):
    """Fetch concurrently from all fact-checking sources
    Args:
        claim: The claim to fetch
        page_url: The URL of the page to fetch

    Returns:
        A tuple of the Google and Rapid API results
    """
    return await gather(
        fetch_google_factcheck(claim, page_url),
        fetch_rapid_factchecker(claim),
    )


def _classify_all(google_raw, rapid_raw) -> List[ProviderResult]:
    """Classify all the provider results
    Args:
        google_raw: The Google API result
        rapid_raw: The Rapid API result

    Returns:
        A list of provider results
    """
    results: List[ProviderResult] = []
    g = classify_google(google_raw)
    if g:
        results.append(g)
    r = classify_rapid(rapid_raw)
    if r:
        results.append(r)
    return results


async def _get_provider_results(query: str, page_url: Optional[str]) -> List[ProviderResult]:
    """Get the provider results
    Args:
        query: The query to get the provider results
        page_url: The URL of the page to get the provider results

    Returns:
        A list of provider results
    """
    filtered_results = await asyncio.to_thread(_filtered_provider_results_sync, query)
    if filtered_results:
        return filtered_results
    # Fetch the provider results concurrently
    google_raw, rapid_raw = await _fetch_all(query, page_url)
    # Classify the provider results
    return _classify_all(google_raw, rapid_raw)


def _filtered_provider_results_sync(query: str) -> List[ProviderResult]:
    """Get the filtered provider results
    Args:
        query: The query to get the filtered provider results

    Returns:
        A list of filtered provider results
    """
    try:
        combined = _claim_extraction_service.get_combined_claims(query=query)
    except Exception:
        # If error getting combined claims, return an empty list
        return []
    # If no combined claims, return an empty list
    if not combined:
        return []

    try:
        # Filter the claims by similarity
        filtered = _similarity_filter_service.filter_claims_by_similarity(
            claims=combined,
            query=query,
            similarity_threshold=settings.similarity_threshold,
        )
    except Exception:
        return []
    if not filtered:
        return []

    classified = _classification_service.classify_claims_batch(filtered)
    # Classify the claims
    provider_results: List[ProviderResult] = []
    for cls in classified:
        # Map the provider name
        provider_enum = (
            ProviderName.GOOGLE
            if cls.get("source_api") == "Google FactCheckTools"
            else ProviderName.RAPID
        )
        # Map the normalized rating to a verdict
        verdict = _map_normalized_rating(cls.get("normalized_rating"))
        # Add the provider result to the list
        provider_results.append(
            ProviderResult(
                provider=provider_enum,
                verdict=verdict,
                rating=cls.get("normalized_rating"),
                title=cls.get("claim"),
                summary=cls.get("claim"),
                source_url=cls.get("review_link"),
                metadata={"source_api": cls.get("source_api")},
            )
        )
    return provider_results


def _map_normalized_rating(label: Optional[str]) -> Verdict:
    """Map the normalized rating to a verdict
    Args:
        label: The normalized rating

    Returns:
        A verdict
    """
    text = (label or "").lower()
    if "true" in text and "false" not in text and "misleading" not in text:
        return Verdict.TRUE
    if "false" in text or "misleading" in text:
        return Verdict.MISLEADING
    return Verdict.UNKNOWN


async def _extract_text_from_url(url: str) -> str:
    """Extract text from the URL
    Args:
        url: The URL to extract text from

    Returns:
        The text from the URL
    """
    try:
        # Fetch the text from the URL
        return await fetch_page_text(url)
    except Exception:
        return ""


async def analyze_detailed(req: AnalyzeRequest) -> AnalyzeResponseDetailed:
    """Analyze the detailed request
    Args:
        req: The request to analyze

    Returns:
        A detailed analysis response
    """
    # Get the raw text from the request
    raw_text = req.text or ""
    # If no raw text and there is a URL, fetch the text from the URL
    if not raw_text and req.url:
        # Get the full URL string - Pydantic v2 AnyHttpUrl uses unicode_string()
        url_str = req.url.unicode_string() if hasattr(req.url, 'unicode_string') else str(req.url)
        raw_text = await fetch_page_text(url_str)
    if not raw_text:
        raw_text = "No text provided."

    claim = extract_claim(raw_text)
    hits = await search_all(claim)

    # Build sentiment corpus: rating/label sentence + snippet + fetched page text
    # for top-5 per provider
    texts: List[str] = []
    # Gather up to 15 URLs (5 per provider); fetch sequentially to avoid
    # rate limits/timeouts
    for h in hits:
        snippet = " ".join(
            [str(h.get("rating") or h.get("verdict") or ""), str(h.get("snippet") or "")]
        ).strip()
        texts.append(snippet.strip())
        if h.get("url"):
            try:
                page_text = await fetch_page_text(str(h.get("url")))
                if page_text:
                    texts.append(page_text)
            except Exception:
                pass

    sent = await analyze_texts_sentiment(texts[:30])
    label, confidence = sentiment_to_label(sent)

    # Build an explanation: sentiment breakdown and provider rating summaries
    pos_sum = sum(score for label, score in sent if str(label).upper().startswith("POS"))
    neg_sum = sum(score for label, score in sent if str(label).upper().startswith("NEG"))
    provider_first_rating: dict[str, str] = {}
    for h in hits:
        prov = h.get("provider")
        if prov and prov not in provider_first_rating:
            provider_first_rating[prov] = str(h.get("rating") or h.get("verdict") or "")
    provider_summary = ", ".join(f"{p}='{r}'" for p, r in provider_first_rating.items() if r)

    # Build the evidence
    evidence = [
        Evidence(snippet=h.get("snippet", ""), source=h.get("source"), url=h.get("url"))
        for h in hits[:5]
    ]

    # Collate per-provider ratings (first available per provider)
    seen = set()
    providers: List[ProviderRating] = []
    for h in hits:
        provider_name = h.get("provider")
        if not provider_name or provider_name in seen:
            continue
        seen.add(provider_name)
        providers.append(
            ProviderRating(
                provider=provider_name,
                rating=h.get("rating"),
                label=h.get("verdict"),
            )
        )

    # Add a user-facing rating derived from the label, preserving "Misleading" wording
    rating = {
        "True": "Accurate",
        "False": "Misleading",
        "Unclear": "Unclear",
    }.get(label, "Unclear")

    explanation_text = (
        f"Sentiment aggregation on {len(texts)} texts: POS={pos_sum:.2f}, NEG={neg_sum:.2f}. "
        f"Per-provider first ratings: {provider_summary}. "
        f"Final label from DistilBERT sentiment with confidence {confidence:.2f}."
    )

    return AnalyzeResponseDetailed(
        claim=claim,
        label=label,
        rating=rating,
        confidence=confidence,
        evidence=evidence,
        providers=providers,
        explanation=explanation_text,
    )