from collections import Counter
from typing import List, Optional, Dict, Tuple
import asyncio

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.app.models.schemas import AggregatedResult, ProviderName, ProviderResult, Verdict
from src.app.core.config import settings


def aggregate_results(claim_text: str, provider_results: List[ProviderResult]) -> AggregatedResult:
    """Choose a final verdict and compute confidence.

    Rule requested: If ANY provider has a proper label (non-UNKNOWN), show that as the
    final label. Preference order: GOOGLE > RAPID > CLAIMBUSTER. Always include all
    provider sources in the response. If none provide a label, return UNKNOWN.
    """
    votes = Counter(result.verdict for result in provider_results)

    # Pick first explicit verdict by preferred provider order
    preferred_order = [ProviderName.GOOGLE, ProviderName.RAPID, ProviderName.CLAIMBUSTER]
    explicit_final: Optional[Verdict] = None
    for provider in preferred_order:
        for res in provider_results:
            if res.provider == provider and res.verdict != Verdict.UNKNOWN:
                explicit_final = res.verdict
                break
        if explicit_final is not None:
            break

    final = (
        explicit_final
        if explicit_final is not None
        else (votes.most_common(1)[0][0] if votes else Verdict.UNKNOWN)
    )

    providers = [r.provider for r in provider_results]
    # Confidence: agreement ratio, boosted if explicit ratings present
    # If explicit label found from any provider, set high confidence;
    # otherwise use agreement ratio
    total = len(provider_results) if provider_results else 1
    if explicit_final is not None:
        confidence = 0.9
    else:
        agreement = (votes[final] / total) if total else 0.0
        confidence = max(0.0, min(1.0, agreement))

    return AggregatedResult(
        claim_text=claim_text,
        verdict=final,
        votes={k: int(v) for k, v in votes.items()},
        provider_results=provider_results,
        providers_checked=providers,
        confidence=confidence,
    )


Label = str  # "True" | "False" | "Unclear"
NormalizedHit = Dict[str, Optional[str]]  # {verdict, snippet, source, url}


def _normalize_label(raw: str) -> Label:
    r = (raw or "").lower()
    # Positive cues
    if any(
        k in r
        for k in [
            "true",
            "mostly true",
            "accurate",
            "correct",
            "supported",
            "verified",
            "substantiated",
            "well-supported",
        ]
    ):
        return "True"
    # Negative cues (map to False; we'll expose rating separately as "Misleading")
    if any(
        k in r
        for k in [
            "false",
            "mostly false",
            "inaccurate",
            "incorrect",
            "fake",
            "pants",
            "misleading",
            "partly false",
            "unsupported",
            "no evidence",
            "not supported",
            "debunked",
        ]
    ):
        return "False"
    return "Unclear"


def _score(label: Label) -> float:
    return {"True": 0.8, "False": 0.8, "Unclear": 0.5}.get(label, 0.5)


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
async def _google(query: str) -> List[NormalizedHit]:
    if not (
        settings.google_api_key
        and settings.google_factcheck_url
        and settings.google_factcheck_endpoint
    ):
        return []
    base = str(settings.google_factcheck_url).rstrip("/")
    endpoint = str(settings.google_factcheck_endpoint).lstrip("/")
    url = f"{base}/{endpoint}"
    params = {"query": query, "key": settings.google_api_key}
    async with httpx.AsyncClient(timeout=_get_timeout()) as client:
        r = await client.get(url, params=params)
        if r.status_code >= 400:
            return []
        data = r.json()
    claims = data.get("claims", []) if isinstance(data, dict) else []
    hits: List[NormalizedHit] = []
    for c in claims:
        for rev in c.get("claimReview", []) or []:
            verdict_raw = (
                rev.get("textRating")
                or rev.get("reviewRating", {}).get("alternateName")
                or rev.get("textualRating")
            )
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
async def _rapid(query: str) -> List[NormalizedHit]:
    if not (
        settings.fact_checker_api_key
        and settings.fact_checker_url
        and settings.fact_checker_endpoint
    ):
        return []
    host = str(settings.fact_checker_url).strip("/")
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
    items = data if isinstance(data, list) else data.get("results", [])
    hits: List[NormalizedHit] = []
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


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(min=0.5, max=2),
    reraise=True,
    retry=retry_if_exception_type(_transient),
)
async def _claimbuster(query: str) -> List[NormalizedHit]:
    if not (
        settings.claim_buster_api_key
        and settings.claim_buster_url
        and settings.claim_buster_endpoint
    ):
        return []
    base_url = str(settings.claim_buster_url).rstrip("/")
    endpoint = str(settings.claim_buster_endpoint).lstrip("/")
    url = f"{base_url}/{endpoint}"
    headers = {"X-Api-Key": settings.claim_buster_api_key}
    params = {"query": query}
    async with httpx.AsyncClient(timeout=_get_timeout()) as client:
        r = await client.get(url, headers=headers, params=params)
        if r.status_code >= 400:
            return []
        data = r.json()
    matches = (
        data.get("matches") if isinstance(data, dict) else (data if isinstance(data, list) else [])
    )
    hits: List[NormalizedHit] = []
    for m in matches[:5]:
        raw = m.get("rating") or m.get("verdict") or m.get("truth_rating") or "unclear"
        hits.append(
            {
                "provider": "claimbuster",
                "rating": raw,
                "verdict": _normalize_label(raw),
                "snippet": m.get("title") or m.get("text") or "",
                "source": m.get("reviewed_by") or "ClaimBuster",
                "url": m.get("url"),
            }
        )
    return hits


async def search_all(claim: str) -> List[NormalizedHit]:
    results = await asyncio.gather(
        _google(claim), _rapid(claim), _claimbuster(claim), return_exceptions=True
    )
    merged: List[NormalizedHit] = []
    for res in results:
        if isinstance(res, list):
            merged.extend(res)
    # keep only top-5 per provider
    per: Dict[str, List[NormalizedHit]] = {
        "google_factcheck": [],
        "rapidapi_fact_checker": [],
        "claimbuster": [],
    }
    for h in merged:
        prov = h.get("provider") or "unknown"
        if prov not in per:
            per[prov] = []
        if len(per[prov]) < 5:
            per[prov].append(h)
    out: List[NormalizedHit] = []
    for k in ["google_factcheck", "rapidapi_fact_checker", "claimbuster"]:
        out.extend(per.get(k, []))
    return out


def aggregate(hits: List[NormalizedHit]) -> Tuple[Label, float]:
    if not hits:
        return "Unclear", 0.5
    score = {"True": 0.0, "False": 0.0, "Unclear": 0.0}
    for h in hits:
        score[h.get("verdict") or "Unclear"] += _score(h.get("verdict") or "Unclear")
    label = max(score, key=score.get)
    total = sum(score.values()) or 1.0
    confidence = min(0.95, max(0.55, score[label] / total))
    return label, float(confidence)
