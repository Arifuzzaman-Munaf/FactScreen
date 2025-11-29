"""Claim Extraction Service Unit Tests.

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


class TestClaimExtractionService:
    """
    Test suite for the claim extraction service.

    Tests extraction and normalization of claims from Google Fact Check API and
    RapidAPI Fact Checker into standardized format.
    """

    @patch("src.app.services.claim_extract.requests.get")
    @patch("src.app.services.claim_extract.requests.post")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fetch_google_claims(self, mock_post, mock_get):
        """
        Test fetching claims from Google Fact Check API.

        Verifies that the function correctly constructs API requests and processes
        responses from Google's fact-checking service.

        Args:
            mock_post: Mocked HTTP POST function.
            mock_get: Mocked HTTP GET function.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {"claims": [{"text": "Test claim"}]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        service = ClaimExtractionService()
        result = service.fetch_google_claims("test query")

        assert "claims" in result
        mock_get.assert_called_once()

    @patch("src.app.services.claim_extract.http.client.HTTPSConnection")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fetch_rapidapi_claims(self, mock_conn_class):
        """
        Test fetching claims from RapidAPI Fact Checker.

        Verifies that the function correctly constructs API requests and processes
        responses from RapidAPI's fact-checking service.

        Args:
            mock_conn_class: Mocked HTTPSConnection class.
        """
        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"data": [{"claim_text": "Test claim"}]}'
        mock_conn.getresponse.return_value = mock_response
        mock_conn_class.return_value = mock_conn

        service = ClaimExtractionService()
        result = service.fetch_rapidapi_claims("test query")

        assert "data" in result
        mock_conn.request.assert_called_once()

    @allure.severity(allure.severity_level.NORMAL)
    def test_map_google_claims(self):
        """
        Test mapping Google API response to standardized format.

        Verifies that Google's API response structure is correctly transformed
        into the application's standard claim format.
        """
        service = ClaimExtractionService()

        google_response = {
            "claims": [
                {
                    "text": "Test claim",
                    "claimant": "Test claimant",
                    "claimDate": "2023-01-01",
                    "claimReview": [
                        {
                            "publisher": {"name": "Test Publisher"},
                            "url": "https://test.com",
                            "textualRating": "False",
                        }
                    ],
                }
            ]
        }

        result = service.map_google_claims(google_response)
        assert len(result) == 1
        assert result[0]["claim"] == "Test claim"
        assert result[0]["rating"] == "False"
        assert result[0]["source_api"] == "Google FactCheckTools"

    @allure.severity(allure.severity_level.NORMAL)
    def test_map_rapidapi_claims(self):
        """
        Test mapping RapidAPI response to standardized format.

        Verifies that RapidAPI's response structure is correctly transformed
        into the application's standard claim format.
        """
        service = ClaimExtractionService()

        rapidapi_response = {
            "data": [
                {
                    "claim_text": "Test claim",
                    "claimant": "Test claimant",
                    "claim_datetime_utc": "2023-01-01",
                    "claim_reviews": [
                        {
                            "publisher": "Test Publisher",
                            "review_link": "https://test.com",
                            "review_text": "True",
                        }
                    ],
                }
            ]
        }

        result = service.map_rapidapi_claims(rapidapi_response)
        assert len(result) == 1
        assert result[0]["claim"] == "Test claim"
        assert result[0]["rating"] == "True"
        assert result[0]["source_api"] == "RapidAPI Fact-Checker"

    @patch("src.app.services.claim_extract.ClaimExtractionService.fetch_google_claims")
    @patch("src.app.services.claim_extract.ClaimExtractionService.fetch_rapidapi_claims")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_combined_claims(self, mock_rapid, mock_google):
        """
        Test combining claims from multiple sources.

        Verifies that claims from both Google and RapidAPI are correctly merged
        into a single list with proper source attribution.

        Args:
            mock_rapid: Mocked RapidAPI fetch function.
            mock_google: Mocked Google fetch function.
        """
        mock_google.return_value = {
            "claims": [{"text": "Google claim", "claimReview": [{"textualRating": "True"}]}]
        }
        mock_rapid.return_value = {
            "data": [{"claim_text": "Rapid claim", "claim_reviews": [{"review_text": "False"}]}]
        }

        service = ClaimExtractionService()
        result = service.get_combined_claims("test query")

        assert len(result) == 2
        assert any("Google" in claim.get("source_api", "") for claim in result)
        assert any("RapidAPI" in claim.get("source_api", "") for claim in result)
