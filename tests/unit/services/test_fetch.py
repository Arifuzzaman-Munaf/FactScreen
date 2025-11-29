"""Data Fetching Service Unit Tests.

This module contains unit tests for the specific service/pipeline.
All tests use proper mocking to isolate logic from external dependencies.
"""

import pytest
import allure
from unittest.mock import AsyncMock, MagicMock, patch
from io import BytesIO

from src.app.models.schemas import (
    AggregatedResult,
    ProviderResult,
    Verdict,
    ProviderName,
)
from src.app.services.factcheck import aggregate_results, search_all
from src.app.services.fetch import (
    fetch_google_factcheck,
    fetch_rapid_factchecker,
    fetch_page_text,
    _http_get,
)
from src.app.services.sentiment import analyze_texts_sentiment, sentiment_to_label
from src.app.services.report import generate_pdf_report
from src.app.services.gemini_service import (
    classify_with_gemini,
    generate_explanation_from_sources,
)
from src.app.services.claim_extract import ClaimExtractionService
from src.app.services.classify import classify_google, classify_rapid


@pytest.fixture
def mock_aggregated_result():
    """
    Create a mock AggregatedResult object for testing purposes.

    Returns:
        AggregatedResult: Mock fact-checking result with sample data from Google provider.
    """
    return AggregatedResult(
        claim_text="Test claim",
        verdict=Verdict.TRUE,
        votes={Verdict.TRUE: 2},
        provider_results=[
            ProviderResult(
                provider=ProviderName.GOOGLE,
                verdict=Verdict.TRUE,
                rating="True",
                title="Test Title",
                summary="Test Summary",
            )
        ],
        providers_checked=[ProviderName.GOOGLE],
        confidence=0.85,
        explanation="Test explanation",
    )



class TestFetchService:
    """
    Test suite for the data fetching service.

    Tests HTTP client functionality for fetching data from Google Fact Check API,
    RapidAPI Fact Checker, and web page text extraction.
    """

    @pytest.mark.asyncio
    @patch("src.app.services.fetch._http_get")
    async def test_fetch_google_factcheck(self, mock_get):
        """
        Test Google Fact Check API data fetching.

        Verifies that the function correctly calls the Google API and returns
        properly formatted claim data.

        Args:
            mock_get: Mocked HTTP GET function.
        """
        mock_get.return_value = {"claims": [{"text": "Test claim"}]}

        result = await fetch_google_factcheck("test query")
        assert "claims" in result

    @pytest.mark.asyncio
    @patch("src.app.services.fetch._http_get")
    async def test_fetch_google_factcheck_with_page_url(self, mock_get):
        """
        Test Google Fact Check API fetch with page URL parameter.

        Verifies that when a page URL is provided, it is correctly included in
        the API request parameters.

        Args:
            mock_get: Mocked HTTP GET function.
        """
        mock_get.return_value = {"claims": []}

        await fetch_google_factcheck("test query", page_url="https://example.com")
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "pageUrl" in call_args[1]["params"]

    @pytest.mark.asyncio
    @patch("src.app.services.fetch._http_get")
    async def test_fetch_rapid_factchecker(self, mock_get):
        """
        Test RapidAPI Fact Checker data fetching.

        Verifies that the function correctly calls the RapidAPI and returns
        properly formatted claim data.

        Args:
            mock_get: Mocked HTTP GET function.
        """
        mock_get.return_value = {"data": [{"claim_text": "Test claim"}]}

        result = await fetch_rapid_factchecker("test query")
        assert "data" in result

    @pytest.mark.asyncio
    @patch("src.app.services.fetch.BeautifulSoup")
    @patch("httpx.AsyncClient")
    async def test_fetch_page_text(self, mock_client_class, mock_bs4_class):
        """
        Test web page text extraction functionality.

        Verifies that HTML content is properly parsed and text is extracted
        with script and style tags removed.

        Args:
            mock_client_class: Mocked HTTPX async client class.
            mock_bs4_class: Mocked BeautifulSoup class.
        """
        mock_response = MagicMock()
        mock_response.text = "<html><body>Test content</body></html>"
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        mock_tag_list = [MagicMock(decompose=MagicMock()) for _ in range(3)]

        class CallableSoupMock(MagicMock):
            def __call__(self, *args, **kwargs):
                if args and isinstance(args[0], list):
                    return mock_tag_list
                return super().__call__(*args, **kwargs)

        mock_soup_instance = CallableSoupMock()
        mock_soup_instance.get_text.return_value = "Test content"
        mock_bs4_class.return_value = mock_soup_instance

        result = await fetch_page_text("https://example.com")
        assert "Test content" in result
        mock_bs4_class.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_http_get_success(self, mock_client_class):
        """
        Test successful HTTP GET request handling.

        Verifies that the HTTP client correctly processes successful responses
        and returns JSON data.

        Args:
            mock_client_class: Mocked HTTPX async client class.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        result = await _http_get("https://example.com")
        assert result == {"data": "test"}

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_http_get_error_handling(self, mock_client_class):
        """
        Test HTTP GET request error handling.

        Verifies that network errors are gracefully handled and an empty dictionary
        is returned instead of raising exceptions.

        Args:
            mock_client_class: Mocked HTTPX async client class configured to raise exception.
        """
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get.side_effect = Exception("Network error")
        mock_client_class.return_value = mock_client

        result = await _http_get("https://example.com")
        assert result == {}


