from typing import Any, Dict, Optional
import re

from src.app.core.config import settings
from src.app.models.schemas import ProviderName, ProviderResult, Verdict


def _normalize_text(text: str) -> str:
    # Normalize the text by converting it to lowercase and removing extra spaces
    t = (text or "").lower()
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _map_label_from_sentence(text: str) -> Verdict:
    """Map a free-form rating sentence to a Verdict via keyword search
    Args:
        text: The text to map to a Verdict
    Returns:
        A Verdict
    """

    t = _normalize_text(text)
    # Get the true and false keywords from the settings
    true_keywords = settings.classification_true_keywords or []
    false_keywords = settings.classification_false_keywords or []
    # If any of the true keywords are in the text, return TRUE
    if any(k in t for k in true_keywords):
        # Return TRUE
        return Verdict.TRUE
    if any(k in t for k in false_keywords):
        # Return MISLEADING
        return Verdict.MISLEADING
    # Return UNKNOWN
    return Verdict.UNKNOWN


def classify_google(payload: Dict[str, Any]) -> Optional[ProviderResult]:
    """
    Normalize Google Fact Check results
    Args:
        payload: The payload to classify
    Returns:
        A ProviderResult object
    """
    # If the payload is not provided, return None
    if not payload:
        # Return None
        return None
    try:
        # Get the claims from the payload
        items = payload.get("claims") or payload.get("items") or []
        # Get the first claim from the items
        first = items[0] if items else None
        # If the first claim is not provided, return None
        if not first:
            return None
        reviews = first.get("claimReview") or []
        # Prefer the review that contains a non-empty rating-like field
        review = None
        # Iterate over the reviews
        for r in reviews:
            # If the review contains a non-empty rating-like field,
            # set the review to the current review
            if r.get("Rating") or r.get("textualRating") or r.get("rating"):
                review = r
                break
        # If the review is not found, set the review to the first review
        if review is None and reviews:
            review = reviews[0]
        # If the review is not found, return None
        if review is None:
            # Return None
            return None
        # Get the text rating from the review
        text_rating = (
            review.get("Rating")
            or review.get("textualRating")
            or review.get("rating")
            or (review.get("reviewRating") or {}).get("alternateName")
            or ""
        )
        # Map the text rating to a Verdict
        verdict = _map_label_from_sentence(str(text_rating))
        # Return a ProviderResult object
        return ProviderResult(
            provider=ProviderName.GOOGLE,
            verdict=verdict,
            rating=str(text_rating) if text_rating else None,
            title=review.get("title"),
            summary=review.get("summary"),
            source_url=(review.get("url") or review.get("publisher", {}).get("site")),
            metadata={"raw": review},
        )
    except Exception:
        return None


def classify_rapid(payload: Dict[str, Any]) -> Optional[ProviderResult]:
    """Normalize RapidAPI fact-check response (vendor-dependent heuristic).
    Args:
        payload: The payload to classify
    Returns:
        A ProviderResult object
    """
    # If the payload is not provided, return None
    if not payload:
        return None
    try:
        # Example API returns list of results; choose one with a non-empty rating-ish field
        candidates = (
            payload
            if isinstance(payload, list)
            else (payload.get("data") or payload.get("items") or payload.get("result") or [])
        )
        # Get the chosen claim from the candidates
        chosen = None
        # If the candidates is a list, iterate over the candidates
        if isinstance(candidates, list):
            for it in candidates:
                if (
                    it.get("review_text")
                    or it.get("label")
                    or it.get("verdict")
                    or it.get("rating")
                    or it.get("textualRating")
                ):
                    chosen = it
                    break
            # If the chosen claim is not found, set the chosen claim to the first claim
            if chosen is None and candidates:
                chosen = candidates[0]
        else:
            chosen = payload
        # RapidAPI: prefer review_text if provided, else label/verdict/rating
        label = (
            chosen.get("review_text")
            or chosen.get("label")
            or chosen.get("verdict")
            or chosen.get("rating")
            or chosen.get("textualRating")
            or ""
        )
        # Map the label to a Verdict
        verdict = _map_label_from_sentence(str(label))
        # Return a ProviderResult object
        return ProviderResult(
            provider=ProviderName.RAPID,
            verdict=verdict,
            rating=str(label) if label else None,
            title=chosen.get("title"),
            summary=chosen.get("summary"),
            source_url=chosen.get("url") or chosen.get("source"),
            metadata={"raw": chosen},
        )
    except Exception:
        return None
