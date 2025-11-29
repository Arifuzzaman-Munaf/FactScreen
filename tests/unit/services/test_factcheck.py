"""Fact-Checking Aggregation Service Unit Tests.

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



class TestFactcheckService:
    """
    Test suite for the fact-checking aggregation service.

    Tests the core logic for aggregating results from multiple fact-checking providers,
    calculating confidence scores using majority vote, and generating explanations.
    """

    @pytest.mark.asyncio
    @patch("src.app.services.factcheck.generate_explanation_from_sources")
    async def test_aggregate_results_majority_vote(self, mock_explanation):
        """
        Test result aggregation using majority vote algorithm.

        Verifies that when multiple providers return different verdicts, the final verdict
        is determined by majority vote and confidence is calculated correctly.

        Args:
            mock_explanation: Mocked explanation generation function.
        """
        mock_explanation.return_value = "Test explanation"

        provider_results = [
            ProviderResult(
                provider=ProviderName.GOOGLE,
                verdict=Verdict.TRUE,
                rating="True",
                title="Test",
            ),
            ProviderResult(
                provider=ProviderName.RAPID,
                verdict=Verdict.TRUE,
                rating="True",
                title="Test 2",
            ),
            ProviderResult(
                provider=ProviderName.GOOGLE,
                verdict=Verdict.MISLEADING,
                rating="False",
                title="Test 3",
            ),
        ]

        result = await aggregate_results("Test claim", provider_results, sources=[])

        assert result.verdict == Verdict.TRUE
        assert result.confidence > 0.5
        assert result.votes[Verdict.TRUE] == 2
        assert result.votes[Verdict.MISLEADING] == 1

    @pytest.mark.asyncio
    @patch("src.app.services.factcheck.classify_with_gemini")
    async def test_aggregate_results_all_unknown_fallback(self, mock_gemini):
        """
        Test aggregation fallback to Gemini when all provider verdicts are UNKNOWN.

        Verifies that when no providers return a definitive verdict, the system falls back
        to Gemini AI classification for final determination.

        Args:
            mock_gemini: Mocked Gemini classification function.
        """
        mock_gemini.return_value = ("True", 0.8, "Gemini explanation")

        provider_results = [
            ProviderResult(
                provider=ProviderName.GOOGLE,
                verdict=Verdict.UNKNOWN,
                rating="Unclear",
                title="Test",
            ),
        ]

        result = await aggregate_results("Test claim", provider_results, sources=[])

        assert result.verdict == Verdict.TRUE
        assert result.explanation == "Gemini explanation"

    @pytest.mark.asyncio
    @patch("src.app.services.factcheck.search_all")
    async def test_search_all(self, mock_search):
        """
        Test the search_all function for retrieving fact-checking sources.

        Verifies that the function returns a list of sources with proper structure.

        Args:
            mock_search: Mocked search function.
        """
        mock_search.return_value = [
            {"snippet": "Test snippet", "verdict": "True", "source": "Test Source"}
        ]

        result = await search_all("Test claim")
        assert len(result) > 0


