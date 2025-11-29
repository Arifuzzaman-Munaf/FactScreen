"""Sentiment Analysis Service Unit Tests.

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



class TestSentimentService:
    """
    Test suite for the sentiment analysis service.

    Tests sentiment classification of text using transformer models and aggregation
    of sentiment results into fact-checking labels.
    """

    @pytest.mark.asyncio
    async def test_analyze_texts_sentiment(self):
        """
        Test sentiment analysis on multiple text inputs.

        Verifies that the function correctly processes a list of texts and returns
        sentiment labels with confidence scores.
        """
        texts = ["This is great!", "This is terrible!", "This is okay."]
        result = await analyze_texts_sentiment(texts)

        assert len(result) == 3
        assert all(isinstance(r, tuple) and len(r) == 2 for r in result)
        assert all(r[0] in ["POSITIVE", "NEGATIVE"] for r in result)

    @pytest.mark.asyncio
    async def test_analyze_texts_sentiment_empty(self):
        """
        Test sentiment analysis with empty input list.

        Verifies that the function handles empty input gracefully and returns
        an empty list.
        """
        result = await analyze_texts_sentiment([])
        assert result == []

    @allure.severity(allure.severity_level.NORMAL)
    def test_sentiment_to_label_positive(self):
        """
        Test sentiment aggregation for predominantly positive results.

        Verifies that when sentiment results are mostly positive, the function
        returns "True" label with appropriate confidence score.
        """
        results = [("POSITIVE", 0.9), ("POSITIVE", 0.8), ("NEGATIVE", 0.2)]
        label, confidence = sentiment_to_label(results)

        assert label == "True"
        assert confidence >= 0.6

    @allure.severity(allure.severity_level.NORMAL)
    def test_sentiment_to_label_negative(self):
        """
        Test sentiment aggregation for predominantly negative results.

        Verifies that when sentiment results are mostly negative, the function
        returns "False" label with appropriate confidence score.
        """
        results = [("NEGATIVE", 0.9), ("NEGATIVE", 0.8), ("POSITIVE", 0.2)]
        label, confidence = sentiment_to_label(results)

        assert label == "False"
        assert confidence >= 0.6

    @allure.severity(allure.severity_level.NORMAL)
    def test_sentiment_to_label_unclear(self):
        """
        Test sentiment aggregation for balanced/unclear results.

        Verifies that when sentiment results are balanced between positive and negative,
        the function returns "Unclear" label with default confidence.
        """
        results = [("POSITIVE", 0.5), ("NEGATIVE", 0.5)]
        label, confidence = sentiment_to_label(results)

        assert label == "Unclear"
        assert confidence == pytest.approx(0.55, abs=0.01)

    @allure.severity(allure.severity_level.NORMAL)
    def test_sentiment_to_label_empty(self):
        """
        Test sentiment aggregation with empty results list.

        Verifies that when no sentiment results are provided, the function returns
        default "Unclear" label with default confidence.
        """
        label, confidence = sentiment_to_label([])
        assert label == "Unclear"
        assert confidence == 0.5


