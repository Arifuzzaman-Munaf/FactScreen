"""Gemini AI Service Integration Unit Tests.

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



    @pytest.mark.asyncio
    async def test_classify_with_gemini_no_api_key(self):
        """
        Test Gemini classification when API key is not configured.

        Verifies that the function gracefully handles missing API key configuration
        and returns default values instead of raising exceptions.
        """
        with patch("src.app.services.gemini_service.settings") as mock_settings:
            mock_settings.gemini_api_key = ""
            label, confidence, explanation = await classify_with_gemini("Test claim")

            assert label == "Unclear"
            assert confidence == 0.5
            assert "not configured" in explanation.lower()


