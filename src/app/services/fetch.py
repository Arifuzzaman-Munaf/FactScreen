from typing import Any, Dict, Optional

import httpx
from bs4 import BeautifulSoup

from src.app.core.config import settings


async def _http_get(
    url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    timeout = settings.request_timeout
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception:
        # Swallow network/API errors and return empty payload so pipeline can continue
        return {}


async def fetch_google_factcheck(query: str, page_url: Optional[str] = None) -> Dict[str, Any]:
    """Call Google Fact Check Tools API claims:search.

    If endpoint is not configured, default to v1alpha1 claims search.
    """
    if not settings.google_api_key:
        return {}
    base = (
        str(settings.google_factcheck_url).rstrip("/")
        if settings.google_factcheck_url
        else "https://factchecktools.googleapis.com"
    )
    endpoint = settings.google_factcheck_endpoint or "v1alpha1/claims:search"
    url = f"{base}/{endpoint}"
    params = {
        "key": settings.google_api_key,
        "languageCode": "en",
        "pageSize": 1,
    }
    if page_url:
        params["pageUrl"] = page_url
    else:
        params["query"] = query
    return await _http_get(url, params=params)


async def fetch_rapid_factchecker(query: str) -> Dict[str, Any]:
    """Call RapidAPI example: fact-checker.p.rapidapi.com/search.

    Requires FACT_CHECKER_URL with scheme and FACT_CHECKER_HOST header.
    """
    if (
        not settings.fact_checker_api_key
        or not settings.fact_checker_url
        or not settings.fact_checker_host
    ):
        return {}
    base = settings.fact_checker_url.rstrip("/")
    endpoint = settings.fact_checker_endpoint or "search"
    url = f"{base}/{endpoint}"
    headers = {
        "X-RapidAPI-Key": settings.fact_checker_api_key,
        "X-RapidAPI-Host": settings.fact_checker_host,
    }
    params = {"query": query, "limit": 20, "offset": 0, "language": "en"}
    return await _http_get(url, params=params, headers=headers)


async def fetch_claimbuster(query: str) -> Dict[str, Any]:
    """Call ClaimBuster example: idir.uta.edu/claimbuster/api/v2/query/fact_matcher/{claim}."""
    if not settings.claim_buster_api_key or not settings.claim_buster_url:
        return {}
    base = str(settings.claim_buster_url).rstrip("/")
    endpoint = settings.claim_buster_endpoint or "api/v2/query/fact_matcher"
    # Claim goes in the path according to the example
    url = f"{base}/{endpoint}/{query}"
    headers = {"x-api-key": settings.claim_buster_api_key}
    return await _http_get(url, headers=headers)


async def fetch_page_text(url: str) -> str:
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        r = await client.get(url, follow_redirects=True)
        r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    return soup.get_text(" ", strip=True)[:8000]
