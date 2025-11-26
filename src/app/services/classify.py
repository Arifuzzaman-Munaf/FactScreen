from typing import Any, Dict, Optional
import re

from src.app.models.schemas import ProviderName, ProviderResult, Verdict
from src.app.models.schemas import ProviderName, ProviderResult, Verdict


_TRUE_KEYWORDS = [
    "true",
    "mostly true",
    "correct",
    "accurate",
    "verified",
    "supported",
    "evidence supports",
]

_FALSE_KEYWORDS = [
    "false",
    "mostly false",
    "misleading",
    "incorrect",
    "fake",
    "debunked",
    "no evidence",
    "not supported",
    "doesn't cause",
    "does not cause",
    "no direct cause",
    "no direct link",
]


def _normalize_text(text: str) -> str:
    t = (text or "").lower()
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _map_label_from_sentence(text: str) -> Verdict:
    """Map a free-form rating sentence to a Verdict via keyword search.

    This scans for indicative phrases appearing anywhere inside the sentence.
    """
    t = _normalize_text(text)
    if any(k in t for k in _TRUE_KEYWORDS):
        return Verdict.TRUE
    if any(k in t for k in _FALSE_KEYWORDS):
        return Verdict.MISLEADING
    return Verdict.UNKNOWN


def classify_google(payload: Dict[str, Any]) -> Optional[ProviderResult]:
    """Normalize Google Fact Check results.

    Expects a structure similar to Google's Fact Check Tools API.
    We'll take the first item/claimReview if present.
    """
    if not payload:
        return None
    try:
        items = payload.get("claims") or payload.get("items") or []
        first = items[0] if items else None
        if not first:
            return None
        reviews = first.get("claimReview") or []
        # Prefer the review that contains a non-empty rating-like field
        review = None
        for r in reviews:
            if r.get("Rating") or r.get("textualRating") or r.get("rating"):
                review = r
                break
        if review is None and reviews:
            review = reviews[0]
        if review is None:
            return None
        # Google: prefer common rating fields; also check nested reviewRating fields
        text_rating = (
            review.get("Rating")
            or review.get("textualRating")
            or review.get("rating")
            or (review.get("reviewRating") or {}).get("alternateName")
            or ""
        )
        verdict = _map_label_from_sentence(str(text_rating))
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
    """Normalize RapidAPI fact-check response (vendor-dependent heuristic)."""
    if not payload:
        return None
    try:
        # Example API returns list of results; choose one with a non-empty rating-ish field
        candidates = (
            payload
            if isinstance(payload, list)
            else (payload.get("data") or payload.get("items") or payload.get("result") or [])
        )
        chosen = None
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
        verdict = _map_label_from_sentence(str(label))
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
