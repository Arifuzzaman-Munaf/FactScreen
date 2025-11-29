"""Provider Result Classification Service Unit Tests.

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


class TestClassifyService:
    """
    Test suite for the provider result classification service.

    Tests normalization of fact-checking results from different providers into
    standardized verdict format using keyword matching and heuristics.
    """

    @allure.severity(allure.severity_level.CRITICAL)
    def test_classify_google_with_claims(self):
        """
        Test Google API result classification.

        Verifies that Google's textual ratings are correctly mapped to standardized
        verdict enums using keyword matching.
        """
        google_response = {
            "claims": [
                {
                    "text": "Test claim",
                    "claimReview": [
                        {
                            "publisher": {"name": "Test Publisher"},
                            "textualRating": "False",
                            "url": "https://test.com",
                        }
                    ],
                }
            ]
        }

        result = classify_google(google_response)
        assert result is not None
        assert result.provider == ProviderName.GOOGLE
        assert result.verdict == Verdict.MISLEADING

    @allure.severity(allure.severity_level.NORMAL)
    def test_classify_google_empty(self):
        """
        Test Google classification with empty response.

        Verifies that the function returns None when no claims are found in the response.
        """
        result = classify_google({})
        assert result is None

    @allure.severity(allure.severity_level.CRITICAL)
    def test_classify_rapid_with_data(self):
        """
        Test RapidAPI result classification.

        Verifies that RapidAPI's review text is correctly mapped to standardized
        verdict enums using keyword matching.
        """
        rapid_response = {
            "data": [
                {
                    "claim_text": "Test claim",
                    "review_text": "True",
                    "publisher": "Test Publisher",
                    "review_link": "https://test.com",
                }
            ]
        }

        result = classify_rapid(rapid_response)
        assert result is not None
        assert result.provider == ProviderName.RAPID
        assert result.verdict == Verdict.TRUE

    @allure.severity(allure.severity_level.NORMAL)
    def test_classify_rapid_empty(self):
        """
        Test RapidAPI classification with empty response.

        Verifies that the function returns None when no data is found in the response.
        """
        result = classify_rapid({})
        assert result is None
