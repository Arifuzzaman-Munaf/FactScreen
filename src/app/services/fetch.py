from typing import Any, Dict, Optional

import httpx
from bs4 import BeautifulSoup

from src.app.core.config import settings


async def _http_get(
    url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Make an HTTP GET request.
    Args:
        url: The URL to make the request to
        params: The parameters to pass to the request
        headers: The headers to pass to the request
    Returns:
        The response from the request
    """
    timeout = settings.request_timeout
    try:
        # Make the request
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            # Return the response
            return response.json()
    except Exception:
        # Swallow network/API errors and return empty payload so pipeline can continue
        return {}


async def fetch_google_factcheck(query: str, page_url: Optional[str] = None) -> Dict[str, Any]:
    """Call Google Fact Check Tools API claims:search.

    Args:
        query: The query to search for
        page_url: The URL of the page to search for
    Returns:
        The response from the request
    """
    # If the API key is not set, return an empty dictionary
    if not settings.google_api_key:
        return {}
    # Get the base URL and endpoint from configuration
    base = str(settings.google_factcheck_url).rstrip("/")
    endpoint = settings.google_factcheck_endpoint
    url = f"{base}/{endpoint}"
    # Build the parameters for the request
    params = {
        "key": settings.google_api_key,
        "languageCode": settings.google_factcheck_language_code,
        "pageSize": settings.google_factcheck_page_size,
    }
    # Add the page URL if provided
    if page_url:
        params["pageUrl"] = page_url
    else:
        params["query"] = query
    return await _http_get(url, params=params)


async def fetch_rapid_factchecker(query: str) -> Dict[str, Any]:
    """Call RapidAPI fact-checker.p.rapidapi.com/search.

    Args:
        query: The query to search for
    Returns:
        The response from the request
    """
    # If the API key is not set, return an empty dictionary
    if (
        not settings.fact_checker_api_key
        or not settings.fact_checker_url
        or not settings.fact_checker_host
    ):
        return {}
    # Get the base URL and endpoint from configuration
    base = settings.fact_checker_url.rstrip("/")
    endpoint = settings.fact_checker_endpoint
    url = f"{base}/{endpoint}"
    # Build the headers for the request
    headers = {
        "X-RapidAPI-Key": settings.fact_checker_api_key,
        "X-RapidAPI-Host": settings.fact_checker_host,
    }
    # Build the parameters for the request
    params = {
        "query": query,
        "limit": settings.fact_checker_limit,
        "offset": settings.fact_checker_offset,
        "language": settings.fact_checker_language,
    }
    # Make the request and return the response
    return await _http_get(url, params=params, headers=headers)


async def fetch_page_text(url: str) -> str:
    """Fetch the text from a given URL.

    Args:
        url: The URL to fetch the text from
    Returns:
        The text from the URL
    """
    # Make the request and return the response
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        r = await client.get(url, follow_redirects=True)
        r.raise_for_status()
    # Parse the text and return the response as a string
    soup = BeautifulSoup(r.text, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    return soup.get_text(" ", strip=True)[:8000]
