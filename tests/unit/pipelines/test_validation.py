"""Claim Validation Pipeline Unit Tests.

This module contains unit tests for the specific service/pipeline.
All tests use proper mocking to isolate logic from external dependencies.
"""

import pytest
import allure
from unittest.mock import patch
import numpy as np

from src.pipelines.validation_pipeline import (
    validate_text,
    validate_url,
    analyze,
    analyze_detailed,
)
from src.pipelines.inference_pipeline import ClaimClassificationService
from src.pipelines.feature_eng_pipeline import SimilarityFilterService
from src.app.models.schemas import (
    AggregatedResult,
    Verdict,
    AnalyzeRequest,
)


class TestValidationPipeline:
    """
    Test suite for the claim validation pipeline.

    Tests the complete validation workflow including text extraction, provider result
    aggregation, and detailed analysis with sentiment scoring.
    """

    @pytest.mark.asyncio
    @patch("src.pipelines.validation_pipeline._get_provider_results")
    @patch("src.pipelines.validation_pipeline.search_all")
    @patch("src.pipelines.validation_pipeline.aggregate_results")
    async def test_validate_text(self, mock_aggregate, mock_search, mock_provider_results):
        """
        Test text-based claim validation workflow.

        Verifies that text input is properly processed through the validation pipeline,
        including provider result fetching, source searching, and result aggregation.

        Args:
            mock_aggregate: Mocked result aggregation function.
            mock_search: Mocked source search function.
            mock_provider_results: Mocked provider result fetching function.
        """
        mock_provider_results.return_value = []
        mock_search.return_value = []
        mock_aggregate.return_value = AggregatedResult(
            claim_text="Test claim",
            verdict=Verdict.TRUE,
            votes={Verdict.TRUE: 1},
            provider_results=[],
            confidence=0.8,
        )

        result = await validate_text("Test claim text")

        assert isinstance(result, AggregatedResult)
        assert result.claim_text == "Test claim"

    @pytest.mark.asyncio
    @patch("src.pipelines.validation_pipeline._extract_text_from_url")
    @patch("src.pipelines.validation_pipeline._get_provider_results")
    @patch("src.pipelines.validation_pipeline.search_all")
    @patch("src.pipelines.validation_pipeline.aggregate_results")
    async def test_validate_url(
        self, mock_aggregate, mock_search, mock_provider_results, mock_extract
    ):
        """
        Test URL-based claim validation workflow.

        Verifies that URL input triggers page text extraction, which is then processed
        through the validation pipeline with proper provider result aggregation.

        Args:
            mock_aggregate: Mocked result aggregation function.
            mock_search: Mocked source search function.
            mock_provider_results: Mocked provider result fetching function.
            mock_extract: Mocked URL text extraction function.
        """
        mock_extract.return_value = "Extracted text from URL"
        mock_provider_results.return_value = []
        mock_search.return_value = []
        mock_aggregate.return_value = AggregatedResult(
            claim_text="Extracted text from URL",
            verdict=Verdict.TRUE,
            votes={Verdict.TRUE: 1},
            provider_results=[],
            confidence=0.8,
        )

        result = await validate_url("https://example.com/article")

        assert isinstance(result, AggregatedResult)
        mock_extract.assert_called_once()

    @pytest.mark.asyncio
    @patch("src.pipelines.validation_pipeline.validate_text")
    async def test_analyze_with_text(self, mock_validate):
        """
        Test generic analyze function with text input.

        Verifies that the analyze function correctly routes text input to the
        text validation pipeline.

        Args:
            mock_validate: Mocked text validation function.
        """
        mock_result = AggregatedResult(
            claim_text="Test",
            verdict=Verdict.TRUE,
            votes={Verdict.TRUE: 1},
            provider_results=[],
            confidence=0.8,
        )
        mock_validate.return_value = mock_result

        request = AnalyzeRequest(text="Test claim")
        result = await analyze(request)

        assert result.result == mock_result

    @pytest.mark.asyncio
    @patch("src.pipelines.validation_pipeline.validate_url")
    async def test_analyze_with_url(self, mock_validate):
        """
        Test generic analyze function with URL input.

        Verifies that the analyze function correctly routes URL input to the
        URL validation pipeline.

        Args:
            mock_validate: Mocked URL validation function.
        """
        mock_result = AggregatedResult(
            claim_text="Test",
            verdict=Verdict.TRUE,
            votes={Verdict.TRUE: 1},
            provider_results=[],
            confidence=0.8,
        )
        mock_validate.return_value = mock_result

        request = AnalyzeRequest(url="https://example.com")
        result = await analyze(request)

        assert result.result == mock_result

    @pytest.mark.asyncio
    @patch("src.pipelines.validation_pipeline.search_all")
    @patch("src.pipelines.validation_pipeline.fetch_page_text")
    @patch("src.pipelines.validation_pipeline.analyze_texts_sentiment")
    @patch("src.pipelines.validation_pipeline.sentiment_to_label")
    async def test_analyze_detailed(
        self, mock_sentiment_label, mock_sentiment, mock_fetch, mock_search
    ):
        """
        Test detailed analysis pipeline with sentiment scoring.

        Verifies that the detailed analysis pipeline correctly combines source searching,
        page text extraction, sentiment analysis, and label conversion to produce
        comprehensive analysis results.

        Args:
            mock_sentiment_label: Mocked sentiment-to-label conversion function.
            mock_sentiment: Mocked sentiment analysis function.
            mock_fetch: Mocked page text fetching function.
            mock_search: Mocked source search function.
        """
        mock_search.return_value = [
            {
                "snippet": "Test snippet",
                "verdict": "True",
                "rating": "True",
                "source": "Test Source",
                "url": "https://example.com",
                "provider": "Google",
            }
        ]
        mock_fetch.return_value = "Page text content"
        mock_sentiment.return_value = [("POSITIVE", 0.9)]
        mock_sentiment_label.return_value = ("True", 0.9)

        request = AnalyzeRequest(text="Test claim")
        result = await analyze_detailed(request)

        assert result.claim is not None
        assert result.label in ["True", "False", "Unclear"]
        assert result.confidence >= 0.0
        assert result.confidence <= 1.0
