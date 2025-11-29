"""Feature Engineering and Similarity Filtering Pipeline Unit Tests.

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



class TestFeatureEngPipeline:
    """
    Test suite for the feature engineering and similarity filtering pipeline.

    Tests the sentence transformer-based similarity filtering service that uses
    cosine similarity to filter claims based on semantic similarity to queries.
    """

    @allure.severity(allure.severity_level.NORMAL)
    def test_similarity_filter_service_initialization(self):
        """
        Test that the similarity filter service initializes correctly.

        Verifies that the service loads the sentence transformer model properly
        during initialization.
        """
        service = SimilarityFilterService()
        assert service.model is not None
        assert service.model_name is not None

    @allure.severity(allure.severity_level.NORMAL)
    def test_cosine_similarity(self):
        """
        Test cosine similarity calculation algorithm.

        Verifies that the cosine similarity function correctly calculates similarity
        between vectors, returning 1.0 for identical vectors and 0.0 for orthogonal vectors.
        """
        service = SimilarityFilterService()

        a = np.array([1, 0, 0])
        b = np.array([1, 0, 0])
        similarity = service.cosine_similarity(a, b)
        assert abs(similarity - 1.0) < 1e-6

        a = np.array([1, 0, 0])
        b = np.array([0, 1, 0])
        similarity = service.cosine_similarity(a, b)
        assert abs(similarity - 0.0) < 1e-6

    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_claims_by_similarity_empty(self):
        """
        Test similarity filtering with empty claims list.

        Verifies that the function handles empty input gracefully and returns
        an empty list without errors.
        """
        service = SimilarityFilterService()
        result = service.filter_claims_by_similarity([], "test query")
        assert result == []

    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_claims_by_similarity(self):
        """
        Test similarity filtering with threshold-based filtering.

        Verifies that claims are correctly filtered based on semantic similarity
        scores, with only claims above the threshold being returned.
        """
        service = SimilarityFilterService()

        claims = [
            {"claim": "Sugar causes diabetes"},
            {"claim": "Water is wet"},
            {"claim": "The sky is blue"},
        ]

        result = service.filter_claims_by_similarity(
            claims, "Sugar causes diabetes", similarity_threshold=0.5
        )

        assert len(result) >= 1
        assert all("query_similarity_score" in claim for claim in result)
        assert all(claim["query_similarity_score"] >= 0.5 for claim in result)

    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_claims_by_similarity_threshold(self):
        """
        Test similarity filtering with different threshold values.

        Verifies that higher similarity thresholds result in fewer filtered claims,
        demonstrating proper threshold-based filtering behavior.
        """
        service = SimilarityFilterService()

        claims = [
            {"claim": "Sugar causes diabetes"},
            {"claim": "Water is essential"},
            {"claim": "The sky is blue"},
        ]

        high_threshold = service.filter_claims_by_similarity(
            claims, "Sugar causes diabetes", similarity_threshold=0.9
        )
        low_threshold = service.filter_claims_by_similarity(
            claims, "Sugar causes diabetes", similarity_threshold=0.1
        )

        assert len(low_threshold) >= len(high_threshold)
