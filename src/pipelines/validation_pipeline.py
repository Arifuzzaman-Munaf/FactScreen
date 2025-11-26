from typing import List
from asyncio import gather

from src.app.models.schemas import (
    AggregatedResult,
    ProviderResult,
    ValidateResponse,
    AnalyzeRequest,
    AnalyzeResponseDetailed,
    Evidence,
    ProviderRating,
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
from src.app.utils.ocr import extract_text_from_base64_image


async def validate_text(text: str) -> AggregatedResult:
    claim = extract_key_claim(text)
    google_raw, rapid_raw = await _fetch_all(claim, None)
    results = _classify_all(google_raw, rapid_raw)
    # Get sources for Gemini explanation
    sources = await search_all(claim)
    return await aggregate_results(claim, results, sources)


async def validate_url(url: str) -> AggregatedResult:
    # Use the URL for Google's pageUrl param to improve hit rate
    claim = extract_key_claim(url)
    google_raw, rapid_raw = await _fetch_all(claim, url)
    results = _classify_all(google_raw, rapid_raw)
    # Get sources for Gemini explanation
    sources = await search_all(claim)
    return await aggregate_results(claim, results, sources)


async def validate_image(image_base64: str) -> AggregatedResult:
    extracted = extract_text_from_base64_image(image_base64)
    claim = extract_key_claim(extracted)
    google_raw, rapid_raw = await _fetch_all(claim, None)
    results = _classify_all(google_raw, rapid_raw)
    # Get sources for Gemini explanation
    sources = await search_all(claim)
    return await aggregate_results(claim, results, sources)


async def analyze(req) -> ValidateResponse:
    """Generic analyzer that accepts text, url, or image_base64.

    Returns a unified ValidateResponse with the aggregated result.
    """
    if getattr(req, "text", None):
        result = await validate_text(req.text)
    elif getattr(req, "url", None):
        result = await validate_url(str(req.url))
    elif getattr(req, "image_base64", None):
        result = await validate_image(req.image_base64)
    else:
        # Should be validated at route level, but keep a safe default
        result = await validate_text("")
    return ValidateResponse(result=result)


async def _fetch_all(claim: str, page_url: str | None):
    """Fetch concurrently from all fact-checking sources"""
    return await gather(
        fetch_google_factcheck(claim, page_url),
        fetch_rapid_factchecker(claim),
    )


def _classify_all(google_raw, rapid_raw) -> List[ProviderResult]:
    results: List[ProviderResult] = []
    g = classify_google(google_raw)
    if g:
        results.append(g)
    r = classify_rapid(rapid_raw)
    if r:
        results.append(r)
    return results


async def analyze_detailed(req: AnalyzeRequest) -> AnalyzeResponseDetailed:
    raw_text = req.text or ""
    if not raw_text and req.url:
        raw_text = await fetch_page_text(str(req.url))
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
