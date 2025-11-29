"""Claim Classification Inference Pipeline Unit Tests.

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


class TestInferencePipeline:
    """
    Test suite for the claim classification inference pipeline.

    Tests the machine learning-based classification service that uses keyword matching
    and transformer models to classify claims into standardized categories.
    """

    @allure.severity(allure.severity_level.NORMAL)
    def test_classification_service_initialization(self):
        """
        Test that the classification service initializes correctly.

        Verifies that the service loads the transformer model and candidate labels
        properly during initialization.
        """
        service = ClaimClassificationService()
        assert service.classifier is not None
        assert service.candidate_labels is not None
        assert len(service.candidate_labels) > 0

    @allure.severity(allure.severity_level.CRITICAL)
    def test_fast_keyword_classification(self):
        """
        Test fast keyword-based classification algorithm.

        Verifies that the keyword matching algorithm correctly identifies True, False,
        and insufficient information cases based on keyword presence in text.
        """
        service = ClaimClassificationService()

        assert service.fast_keyword_classification("This is true") == "True"
        assert service.fast_keyword_classification("This is correct") == "True"
        assert service.fast_keyword_classification("This is false") == "False or Misleading"
        assert service.fast_keyword_classification("This is misleading") == "False or Misleading"
        assert (
            service.fast_keyword_classification("Not enough information")
            == "Not enough information found"
        )

    @allure.severity(allure.severity_level.CRITICAL)
    def test_classify_from_original_rating(self):
        """
        Test classification based on original provider rating.

        Verifies that original ratings from fact-checking providers are correctly
        mapped to standardized classification labels.
        """
        service = ClaimClassificationService()

        assert service.classify_from_original_rating("True") == "True"
        assert service.classify_from_original_rating("False") == "False or Misleading"
        assert (
            service.classify_from_original_rating("Not enough info")
            == "Not enough information found"
        )

    @allure.severity(allure.severity_level.NORMAL)
    def test_classify_claim_priority(self):
        """
        Test classification priority hierarchy.

        Verifies that original rating takes priority over keyword matching, ensuring
        provider ratings are respected when available.
        """
        service = ClaimClassificationService()

        result = service.classify_claim("This is false", "True")
        assert result == "True"

        result = service.classify_claim("This is true", "False")
        assert result == "False or Misleading"

    @allure.severity(allure.severity_level.NORMAL)
    def test_classify_claims_batch(self):
        """
        Test batch classification of multiple claims.

        Verifies that the service can efficiently process multiple claims in a single
        batch operation with proper normalization of ratings.
        """
        service = ClaimClassificationService()

        claims = [
            {"claim": "This is true", "rating": "True"},
            {"claim": "This is false", "rating": "False"},
            {"claim": "Unclear claim", "rating": "Unclear"},
        ]

        result = service.classify_claims_batch(claims)

        assert len(result) == 3
        assert all("normalized_rating" in claim for claim in result)
        assert result[0]["normalized_rating"] == "True"
        assert result[1]["normalized_rating"] == "False or Misleading"

    @allure.severity(allure.severity_level.NORMAL)
    def test_get_classification_labels(self):
        """
        Test retrieval of available classification labels.

        Verifies that the service correctly returns the list of supported
        classification categories.
        """
        service = ClaimClassificationService()
        labels = service.get_classification_labels()

        assert isinstance(labels, list)
        assert len(labels) > 0
        assert "True" in labels