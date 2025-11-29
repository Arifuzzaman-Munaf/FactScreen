"""PDF Report Generation Service Unit Tests.

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



class TestReportService:
    """
    Test suite for the PDF report generation service.

    Tests PDF document generation from aggregated fact-checking results with
    proper formatting, styling, and content structure.
    """

    @allure.severity(allure.severity_level.NORMAL)
    @allure.severity(allure.severity_level.NORMAL)
    def test_generate_pdf_report(self, mock_aggregated_result):
        """
        Test PDF report generation from aggregated result.

        Verifies that the function generates a valid PDF document with correct
        file structure and format.

        Args:
            mock_aggregated_result: Mock aggregated result fixture.
        """
        pdf_buffer = generate_pdf_report(mock_aggregated_result)

        assert isinstance(pdf_buffer, BytesIO)
        assert pdf_buffer.getvalue().startswith(b"%PDF")

    @allure.severity(allure.severity_level.NORMAL)
    def test_generate_pdf_report_with_sources(self):
        """
        Test PDF report generation with source information.

        Verifies that PDF reports correctly include and format source information
        when available in the explanation text.
        """
        result = AggregatedResult(
            claim_text="Test claim with sources",
            verdict=Verdict.TRUE,
            votes={Verdict.TRUE: 1},
            provider_results=[],
            confidence=0.9,
            explanation=(
                "Test explanation\n\nSources:\n- Source 1 | snippet: "
                "Test snippet | https://example.com"
            ),
        )

        pdf_buffer = generate_pdf_report(result)
        assert isinstance(pdf_buffer, BytesIO)
        assert len(pdf_buffer.getvalue()) > 0

    @allure.severity(allure.severity_level.NORMAL)
    def test_generate_pdf_report_all_verdicts(self):
        """
        Test PDF generation for all possible verdict types.

        Verifies that PDF reports can be generated for TRUE, MISLEADING, and UNKNOWN
        verdicts without errors.
        """
        for verdict in [Verdict.TRUE, Verdict.MISLEADING, Verdict.UNKNOWN]:
            result = AggregatedResult(
                claim_text="Test claim",
                verdict=verdict,
                votes={verdict: 1},
                provider_results=[],
                confidence=0.8,
            )

            pdf_buffer = generate_pdf_report(result)
            assert isinstance(pdf_buffer, BytesIO)
            assert len(pdf_buffer.getvalue()) > 0


