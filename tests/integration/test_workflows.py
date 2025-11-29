"""End-to-End Integration Workflow Tests for FactScreen Application.

This module contains integration tests that verify complete workflows
across multiple components of the FactScreen fact-checking application.
"""

import pytest
import allure
from unittest.mock import patch

from src.pipelines.validation_pipeline import validate_text, validate_url
from src.app.services.factcheck import aggregate_results
from src.app.models.schemas import (
    AggregatedResult,
    ProviderResult,
    Verdict,
    ProviderName,
)


class TestEndToEndValidation:
    """
    Test suite for complete end-to-end validation workflows.

    Tests the full validation pipeline from input to final result, including
    provider API calls, classification, aggregation, and explanation generation.
    """

    @pytest.mark.asyncio
    @patch("src.pipelines.validation_pipeline.fetch_google_factcheck")
    @patch("src.pipelines.validation_pipeline.fetch_rapid_factchecker")
    @patch("src.pipelines.validation_pipeline.classify_google")
    @patch("src.pipelines.validation_pipeline.classify_rapid")
    @patch("src.pipelines.validation_pipeline.search_all")
    @patch("src.pipelines.validation_pipeline.aggregate_results")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_end_to_end_text_validation(
        self,
        mock_aggregate,
        mock_search,
        mock_classify_rapid,
        mock_classify_google,
        mock_rapid,
        mock_google,
    ):
        """
        Test complete text validation workflow from input to result.

        Verifies that the entire validation pipeline correctly processes text input
        through provider API calls, classification, source searching, and result
        aggregation to produce a final fact-checking verdict.

        Args:
            mock_aggregate: Mocked result aggregation function.
            mock_search: Mocked source search function.
            mock_classify_rapid: Mocked RapidAPI classification function.
            mock_classify_google: Mocked Google classification function.
            mock_rapid: Mocked RapidAPI fetch function.
            mock_google: Mocked Google fetch function.
        """
        mock_google.return_value = {"claims": [{"text": "Test claim"}]}
        mock_rapid.return_value = {"data": [{"claim_text": "Test claim"}]}

        mock_classify_google.return_value = ProviderResult(
            provider=ProviderName.GOOGLE,
            verdict=Verdict.TRUE,
            rating="True",
            title="Test",
        )
        mock_classify_rapid.return_value = ProviderResult(
            provider=ProviderName.RAPID,
            verdict=Verdict.TRUE,
            rating="True",
            title="Test 2",
        )

        mock_search.return_value = []
        mock_aggregate.return_value = AggregatedResult(
            claim_text="Test claim",
            verdict=Verdict.TRUE,
            votes={Verdict.TRUE: 2},
            provider_results=[],
            confidence=0.9,
        )

        result = await validate_text("Sugar causes diabetes")

        assert isinstance(result, AggregatedResult)
        assert result.verdict == Verdict.TRUE

    @pytest.mark.asyncio
    @patch("src.pipelines.validation_pipeline.fetch_page_text")
    @patch("src.pipelines.validation_pipeline.fetch_google_factcheck")
    @patch("src.pipelines.validation_pipeline.fetch_rapid_factchecker")
    @patch("src.pipelines.validation_pipeline.classify_google")
    @patch("src.pipelines.validation_pipeline.classify_rapid")
    @patch("src.pipelines.validation_pipeline.search_all")
    @patch("src.pipelines.validation_pipeline.aggregate_results")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_end_to_end_url_validation(
        self,
        mock_aggregate,
        mock_search,
        mock_classify_rapid,
        mock_classify_google,
        mock_rapid,
        mock_google,
        mock_fetch_page,
    ):
        """
        Test complete URL validation workflow from input to result.

        Verifies that the entire validation pipeline correctly processes URL input
        through page text extraction, provider API calls, classification, and result
        aggregation to produce a final fact-checking verdict.

        Args:
            mock_aggregate: Mocked result aggregation function.
            mock_search: Mocked source search function.
            mock_classify_rapid: Mocked RapidAPI classification function.
            mock_classify_google: Mocked Google classification function.
            mock_rapid: Mocked RapidAPI fetch function.
            mock_google: Mocked Google fetch function.
            mock_fetch_page: Mocked page text extraction function.
        """
        mock_fetch_page.return_value = "Extracted article text about diabetes"
        mock_google.return_value = {"claims": []}
        mock_rapid.return_value = {"data": []}

        mock_classify_google.return_value = None
        mock_classify_rapid.return_value = None

        mock_search.return_value = []
        mock_aggregate.return_value = AggregatedResult(
            claim_text="Extracted article text",
            verdict=Verdict.UNKNOWN,
            votes={},
            provider_results=[],
            confidence=0.5,
        )

        result = await validate_url("https://example.com/article")

        assert isinstance(result, AggregatedResult)
        mock_fetch_page.assert_called_once()


class TestServiceIntegration:
    """
    Test suite for service integration scenarios.

    Tests how different services interact with each other, including aggregation
    with multiple providers, fallback mechanisms, and source integration.
    """

    @pytest.mark.asyncio
    @patch("src.app.services.factcheck.generate_explanation_from_sources")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_aggregate_with_provider_results(self, mock_explanation):
        """
        Test result aggregation with multiple provider results.

        Verifies that the aggregation service correctly combines results from
        multiple fact-checking providers and generates comprehensive explanations.

        Args:
            mock_explanation: Mocked explanation generation function.
        """
        mock_explanation.return_value = "Combined explanation from all sources"

        provider_results = [
            ProviderResult(
                provider=ProviderName.GOOGLE,
                verdict=Verdict.TRUE,
                rating="True",
                title="Google Title",
                summary="Google summary",
            ),
            ProviderResult(
                provider=ProviderName.RAPID,
                verdict=Verdict.TRUE,
                rating="True",
                title="Rapid Title",
                summary="Rapid summary",
            ),
        ]

        sources = [{"snippet": "Source snippet", "verdict": "True", "source": "Test Source"}]

        result = await aggregate_results("Test claim", provider_results, sources)

        assert result.verdict == Verdict.TRUE
        assert result.confidence > 0.0
        assert len(result.provider_results) == 2
        assert result.explanation is not None

    @pytest.mark.asyncio
    @patch("src.app.services.factcheck.classify_with_gemini")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_aggregate_fallback_to_gemini(self, mock_gemini):
        """
        Test aggregation fallback to Gemini AI when no provider results available.

        Verifies that when no fact-checking providers return results, the system
        gracefully falls back to Gemini AI for classification and explanation.

        Args:
            mock_gemini: Mocked Gemini classification function.
        """
        mock_gemini.return_value = ("True", 0.85, "Gemini-generated explanation")

        result = await aggregate_results("Test claim", [], [])

        assert result.verdict == Verdict.TRUE
        assert result.explanation == "Gemini-generated explanation"
        assert result.confidence == 0.85


class TestConfidenceCalculation:
    """
    Test suite for confidence score calculation logic.

    Tests the mathematical correctness of confidence calculation algorithms
    including majority vote scenarios and edge cases.
    """

    @pytest.mark.asyncio
    @patch("src.app.services.factcheck.generate_explanation_from_sources")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_confidence_majority_vote(self, mock_explanation):
        """
        Test confidence calculation with majority vote scenario.

        Verifies that confidence is correctly calculated as the ratio of providers
        supporting the final verdict to the total number of non-UNKNOWN verdicts.

        Args:
            mock_explanation: Mocked explanation generation function.
        """
        mock_explanation.return_value = "Explanation"

        provider_results = [
            ProviderResult(provider=ProviderName.GOOGLE, verdict=Verdict.TRUE, rating="True"),
            ProviderResult(provider=ProviderName.RAPID, verdict=Verdict.TRUE, rating="True"),
            ProviderResult(provider=ProviderName.GOOGLE, verdict=Verdict.TRUE, rating="True"),
            ProviderResult(provider=ProviderName.RAPID, verdict=Verdict.MISLEADING, rating="False"),
        ]

        result = await aggregate_results("Test claim", provider_results, [])

        assert result.verdict == Verdict.TRUE
        assert result.confidence == pytest.approx(0.75, abs=0.01)

    @pytest.mark.asyncio
    @patch("src.app.services.factcheck.generate_explanation_from_sources")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_confidence_unanimous(self, mock_explanation):
        """
        Test confidence calculation with unanimous provider agreement.

        Verifies that when all providers agree on a verdict, confidence is
        calculated as 1.0 (100%).

        Args:
            mock_explanation: Mocked explanation generation function.
        """
        mock_explanation.return_value = "Explanation"

        provider_results = [
            ProviderResult(provider=ProviderName.GOOGLE, verdict=Verdict.TRUE, rating="True"),
            ProviderResult(provider=ProviderName.RAPID, verdict=Verdict.TRUE, rating="True"),
        ]

        result = await aggregate_results("Test claim", provider_results, [])

        assert result.verdict == Verdict.TRUE
        assert result.confidence == pytest.approx(1.0, abs=0.01)


class TestErrorHandling:
    """
    Test suite for error handling and resilience.

    Tests how the system handles various error conditions including API failures,
    empty results, and network errors to ensure graceful degradation.
    """

    @pytest.mark.asyncio
    @patch("src.pipelines.validation_pipeline.fetch_google_factcheck")
    @patch("src.pipelines.validation_pipeline.fetch_rapid_factchecker")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_validation_handles_api_errors(self, mock_rapid, mock_google):
        """
        Test that validation pipeline handles API errors gracefully.

        Verifies that when external API calls fail, the validation pipeline
        continues processing and returns a result instead of raising exceptions.

        Args:
            mock_rapid: Mocked RapidAPI fetch function configured to raise exception.
            mock_google: Mocked Google fetch function configured to raise exception.
        """
        mock_google.side_effect = Exception("API Error")
        mock_rapid.return_value = {}

        result = await validate_text("Test claim")
        assert isinstance(result, AggregatedResult)

    @pytest.mark.asyncio
    @patch("src.app.services.factcheck.generate_explanation_from_sources")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_aggregate_handles_empty_providers(self, mock_explanation):
        """
        Test that aggregation handles empty provider results gracefully.

        Verifies that when no provider results are available, the aggregation
        service falls back to alternative methods instead of raising exceptions.

        Args:
            mock_explanation: Mocked explanation generation function.
        """
        mock_explanation.return_value = "Explanation"

        result = await aggregate_results("Test claim", [], [])

        assert isinstance(result, AggregatedResult)
        assert result.claim_text == "Test claim"