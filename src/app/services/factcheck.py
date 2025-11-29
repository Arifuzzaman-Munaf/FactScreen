from collections import Counter
from typing import List, Optional, Dict, Tuple
import asyncio

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.app.models.schemas import AggregatedResult, ProviderResult, Verdict
from src.app.core.config import settings
from src.app.services.gemini_service import (
    classify_with_gemini,
    generate_explanation_from_sources,
)


def _check_claim_verdict_alignment(
    claim_text: str, provider_results: List[ProviderResult]
) -> Tuple[bool, float]:
    """
    Check if provider verdicts are aligned with the actual claim.
    
    This function checks if the fact-checking results are about the same claim
    or a related/opposite claim. Returns alignment status and confidence.
    
    Args:
        claim_text: The original claim being verified
        provider_results: List of provider results with verdicts
        
    Returns:
        Tuple of (is_aligned: bool, alignment_confidence: float)
    """
    if not provider_results or not claim_text:
        return True, 1.0  # If no results, consider aligned (will use Gemini)
    
    # Extract key terms from the claim (simple approach)
    claim_lower = claim_text.lower()
    claim_words = set(word for word in claim_lower.split() if len(word) > 3)
    
    # Check each provider result's title/summary for alignment
    aligned_count = 0
    total_checked = 0
    
    for res in provider_results:
        if res.verdict == Verdict.UNKNOWN:
            continue
            
        total_checked += 1
        # Get the text being fact-checked (title or summary)
        fact_checked_text = (res.title or res.summary or "").lower()
        
        if not fact_checked_text:
            # If no text, assume misaligned to be safe
            continue
        
        # Check for direct match or high overlap
        fact_words = set(word for word in fact_checked_text.split() if len(word) > 3)
        
        # Calculate word overlap
        if claim_words and fact_words:
            overlap = len(claim_words.intersection(fact_words))
            overlap_ratio = overlap / max(len(claim_words), len(fact_words))
            
            # Check for opposite claims (e.g., "east" vs "west", "true" vs "false")
            opposite_indicators = [
                ("east", "west"), ("west", "east"),
                ("north", "south"), ("south", "north"),
                ("true", "false"), ("false", "true"),
                ("yes", "no"), ("no", "yes"),
                ("rise", "set"), ("set", "rise"),
                ("up", "down"), ("down", "up"),
                ("increase", "decrease"), ("decrease", "increase"),
                ("more", "less"), ("less", "more"),
            ]
            
            is_opposite = False
            for term1, term2 in opposite_indicators:
                # Check if one term is in claim and the opposite is in fact-checked text
                if (term1 in claim_lower and term2 in fact_checked_text) or \
                   (term2 in claim_lower and term1 in fact_checked_text):
                    is_opposite = True
                    break
            
            # If it's an opposite claim, consider it misaligned
            if is_opposite:
                continue
            
            # Consider aligned if overlap ratio is reasonable (>= 0.3) or exact match
            if overlap_ratio >= 0.3 or claim_lower in fact_checked_text or fact_checked_text in claim_lower:
                aligned_count += 1
    
    # If we checked results, calculate alignment ratio
    if total_checked > 0:
        alignment_ratio = aligned_count / total_checked
        # Consider aligned if at least 50% of results are aligned
        is_aligned = alignment_ratio >= 0.5
        return is_aligned, alignment_ratio
    
    # If no results to check, consider aligned
    return True, 1.0


async def aggregate_results(
    claim_text: str, provider_results: List[ProviderResult], sources: Optional[List[Dict]] = None
) -> AggregatedResult:
    """Choose a final verdict and compute confidence using majority vote

    Rules:
    - Final verdict is determined by majority vote among non-UNKNOWN
      provider verdicts.
    - Confidence is calculated as:
      count_of_providers_supporting_final / count_of_all_non_unknown_verdicts.
    - Always include all provider sources in the response.
    - If no providers return a non-UNKNOWN verdict, fall back to Gemini classification.
    - Explanation is generated from available sources using Gemini.

    Args:
        claim_text: The text of the claim to fact-check.
        provider_results: The provider results to aggregate.
        sources: Optional sources to use for the explanation.

    Returns:
        An AggregatedResult object containing the final verdict, confidence, and explanation.
    """
    # Check if provider verdicts are aligned with the actual claim
    is_aligned, alignment_confidence = _check_claim_verdict_alignment(claim_text, provider_results)
    
    # Count the number of providers supporting each verdict
    votes = Counter(res.verdict for res in provider_results if res.verdict != Verdict.UNKNOWN)
    # Get the most common verdict
    final = votes.most_common(1)[0][0] if votes else Verdict.UNKNOWN
    # Get the providers that supported the final verdict
    providers = [r.provider for r in provider_results]
    # Initialize the explanation to None
    explanation: Optional[str] = None
    # Initialize the sources for the explanation to the sources provided
    sources_for_explanation: List[Dict[str, Optional[str]]] = list(sources or [])

    # If verdicts are not aligned with the claim, fallback to Gemini
    # This handles cases where fact-checkers return results for opposite/related claims
    if not is_aligned and final != Verdict.UNKNOWN:
        # Verdicts exist but don't align with the claim - use Gemini instead
        # Pass sources to Gemini so it can mention if they're about opposite/related claims
        gemini_label, gemini_confidence, gemini_explanation = await classify_with_gemini(
            claim_text, sources
        )
        # Map Gemini label to Verdict enum
        if gemini_label == "True":
            final = Verdict.TRUE
        elif gemini_label == "False":
            final = Verdict.MISLEADING
        else:
            final = Verdict.UNKNOWN

        confidence = gemini_confidence
        explanation = gemini_explanation
        # Keep sources but note they may be about opposite/related claims
        # Gemini will handle this in its explanation
        sources_for_explanation = list(sources or [])
    # If we have aligned verdicts, generate explanation from available sources
    elif provider_results and any(r.verdict != Verdict.UNKNOWN for r in provider_results) and is_aligned:
        # Convert provider results to dict format for explanation generation
        # Include title as it often contains the actual claim being fact-checked
        verdicts_list = []
        # Iterate over the provider results
        for res in provider_results:
            # If the provider result is not UNKNOWN, add it to the verdicts list
            if res.verdict != Verdict.UNKNOWN:
                verdicts_list.append(
                    {
                        "verdict": res.verdict.value,
                        "rating": res.rating,
                        "title": res.title or "",
                        "snippet": res.summary or res.title or "",
                        "source": res.provider.value,
                        "url": str(res.source_url) if res.source_url else None,
                    }
                )

        # If there are verdicts and sources, generate an explanation from the sources
        if verdicts_list and sources:
            # Generate an explanation from the sources
            explanation = await generate_explanation_from_sources(claim_text, sources)
            # Set the sources for the explanation to the sources provided
            sources_for_explanation = list(sources or [])
        # If there are verdicts but no sources, generate an explanation from the provider results
        elif verdicts_list:
            # Have verdicts but no sources dict - generate explanation from provider results
            sources_dict = [
                {
                    "verdict": res.verdict.value,
                    "rating": res.rating,
                    "snippet": res.summary or res.title or "",
                    "source": res.provider.value,
                    "url": str(res.source_url) if res.source_url else None,
                }
                for res in provider_results
                if res.verdict != Verdict.UNKNOWN
            ]
            # If there are sources, generate an explanation from the sources
            if sources_dict:
                explanation = await generate_explanation_from_sources(claim_text, sources_dict)
                sources_for_explanation = sources_dict

    # If no verdicts from third-party, use Gemini classification
    if final == Verdict.UNKNOWN:
        gemini_label, gemini_confidence, gemini_explanation = await classify_with_gemini(
            claim_text, sources
        )
        # Map Gemini label to Verdict enum
        # If the Gemini label is TRUE, set the final verdict to TRUE
        if gemini_label == "True":
            final = Verdict.TRUE
        elif gemini_label == "False":
            final = Verdict.MISLEADING
        else:
            final = Verdict.UNKNOWN

        confidence = gemini_confidence
        explanation = gemini_explanation
        sources_for_explanation = list(sources or [])
    else:
        # If there are verdicts, calculate the confidence
        labeled_total = sum(count for verdict, count in votes.items() if verdict != Verdict.UNKNOWN)
        confidence = votes[final] / labeled_total if labeled_total and final in votes else 0.0
        confidence = float(max(0.0, min(1.0, confidence)))

        # If no explanation generated yet, create one from sources
        if not explanation and sources:
            explanation = await generate_explanation_from_sources(claim_text, sources)
            sources_for_explanation = list(sources or [])
    # Attach the sources to the explanation
    explanation = _attach_sources_block(explanation, sources_for_explanation)
    # Return the aggregated result
    return AggregatedResult(
        claim_text=claim_text,
        verdict=final,
        votes={k: int(v) for k, v in votes.items()},
        provider_results=provider_results,
        providers_checked=providers,
        confidence=confidence,
        explanation=explanation,
    )


def _attach_sources_block(
    explanation: Optional[str], sources: Optional[List[Dict[str, Optional[str]]]]
) -> Optional[str]:
    """Append a bullet list of sources to the explanation.
    Args:
        explanation: The explanation to append the sources to
        sources: The sources to append to the explanation
    Returns:
        The explanation with the sources appended
    """
    # If the explanation is not provided, return the explanation
    if not explanation:
        return explanation

    lines: List[str] = []
    # If the sources are provided, iterate over the sources
    if sources:
        for src in sources:
            source_name = (
                src.get("source") or src.get("provider") or src.get("provider_name") or "Source"
            )
            verdict = src.get("verdict") or src.get("rating")
            url = src.get("url")
            snippet = src.get("snippet")
            parts = [source_name]
            if verdict:
                parts.append(f"verdict: {verdict}")
            if snippet:
                parts.append(f"snippet: {snippet[:120]}{'...' if len(snippet) > 120 else ''}")
            detail = " | ".join(parts)
            if url:
                detail = f"{detail} | {url}"
            # Add the detail to the lines
            lines.append(detail)

    # If there are no lines, return the explanation
    if not lines:
        return explanation
    sources_block = "\n".join(f"- {line}" for line in lines)
    return f"{explanation}\n\nSources:\n{sources_block}"


def _normalize_label(raw: str) -> str:
    """Normalize a raw rating string to a standardized label using keywords from config.

    Args:
        raw: Raw rating text from fact-checking provider.
    Returns:
        A normalized label: "True", "False", or "Unclear".
    """
    # Normalize the raw rating text to lowercase
    r = (raw or "").lower()
    # Get keywords from settings (loaded from config/local.yaml)
    true_keywords = settings.classification_true_keywords or []
    false_keywords = settings.classification_false_keywords or []

    # Check for positive cues
    if any(k in r for k in true_keywords):
        return "True"
    # Check for negative cues (map to False)
    if any(k in r for k in false_keywords):
        return "False"
    return "Unclear"


# Transient exceptions
_transient = (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.RemoteProtocolError)


def _get_timeout() -> int:
    """Get request timeout value."""
    return int(settings.request_timeout or 15)


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(min=0.5, max=2),
    reraise=True,
    retry=retry_if_exception_type(_transient),
)
async def _google(query: str) -> List[Dict[str, Optional[str]]]:
    """Search Google Fact Check for the claim.
    Args:
        query: The claim to search for
    Returns:
        A list of normalized hits
    """

    if not (
        settings.google_api_key
        and settings.google_factcheck_url
        and settings.google_factcheck_endpoint
    ):
        return []
    # Get the base URL and endpoint
    base = str(settings.google_factcheck_url).rstrip("/")
    endpoint = str(settings.google_factcheck_endpoint).lstrip("/")
    # Construct the URL
    url = f"{base}/{endpoint}"
    # Construct the parameters
    params = {"query": query, "key": settings.google_api_key}
    # Make the request
    async with httpx.AsyncClient(timeout=_get_timeout()) as client:
        r = await client.get(url, params=params)
        # If the status code is greater than or equal to 400, return an empty list
        if r.status_code >= 400:
            return []
        data = r.json()
    claims = data.get("claims", []) if isinstance(data, dict) else []
    hits: List[Dict[str, Optional[str]]] = []
    for c in claims:
        for rev in c.get("claimReview", []) or []:
            verdict_raw = (
                rev.get("textRating")
                or rev.get("reviewRating", {}).get("alternateName")
                or rev.get("textualRating")
            )
            # Add the hit to the list
            hits.append(
                {
                    "provider": "google_factcheck",
                    "rating": verdict_raw,
                    "verdict": _normalize_label(verdict_raw or ""),
                    "snippet": rev.get("title") or c.get("text") or "",
                    "source": (rev.get("publisher") or {}).get("name") or "Google Fact Check",
                    "url": rev.get("url"),
                }
            )
    return hits[:5]


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(min=0.5, max=2),
    reraise=True,
    retry=retry_if_exception_type(_transient),
)
async def _rapid(query: str) -> List[Dict[str, Optional[str]]]:
    """Search RapidAPI Fact Check for the claim.
    Args:
        query: The claim to search for
    Returns:
        A list of normalized hits
    """
    if not (
        settings.fact_checker_api_key
        and settings.fact_checker_url
        and settings.fact_checker_endpoint
    ):
        return []
    # Get the host and URL
    host = str(settings.fact_checker_url).strip("/")
    # Construct the URL
    url = f"https://{host}/{str(settings.fact_checker_endpoint).lstrip('/')}"
    headers = {
        "X-RapidAPI-Key": settings.fact_checker_api_key,
        "X-RapidAPI-Host": host,
    }
    params = {"query": query}
    async with httpx.AsyncClient(timeout=_get_timeout()) as client:
        r = await client.get(url, headers=headers, params=params)
        if r.status_code >= 400:
            return []
        data = r.json()
    # Get the items
    items = data if isinstance(data, list) else data.get("results", [])
    hits: List[Dict[str, Optional[str]]] = []
    # Iterate over the items
    for it in items[:5]:
        raw = it.get("verdict") or it.get("label") or it.get("rating") or it.get("textualRating")
        hits.append(
            {
                "provider": "rapidapi_fact_checker",
                "rating": raw,
                "verdict": _normalize_label(raw or ""),
                "snippet": it.get("summary") or it.get("title") or "",
                "source": it.get("source") or "RapidAPI Fact Checker",
                "url": it.get("url") or it.get("link"),
            }
        )
    return hits


async def search_all(claim: str) -> List[Dict[str, Optional[str]]]:
    """Search all fact checkers for the claim.
    Args:
        claim: The claim to search for
    Returns:
        A list of normalized hits
    """
    # Search all fact checkers
    results = await asyncio.gather(_google(claim), _rapid(claim), return_exceptions=True)
    # Merge the results
    merged: List[Dict[str, Optional[str]]] = []
    for res in results:
        if isinstance(res, list):
            merged.extend(res)
    # keep only top-5 per provider
    per: Dict[str, List[Dict[str, Optional[str]]]] = {
        "google_factcheck": [],
        "rapidapi_fact_checker": [],
    }
    # Iterate over the merged results
    for h in merged:
        # Get the provider
        prov = h.get("provider") or "unknown"
        # If the provider is not in the dictionary, add it
        if prov not in per:
            # Add the provider to the dictionary
            per[prov] = []
        if len(per[prov]) < 5:
            per[prov].append(h)
    out: List[Dict[str, Optional[str]]] = []
    # Iterate over the providers
    for k in ["google_factcheck", "rapidapi_fact_checker"]:
        # Add the provider to the list
        out.extend(per.get(k, []))
    return out
