#!/usr/bin/env python3
"""
Unit tests for FactScreen services
"""

from src.app.services.claim_extract import ClaimExtractionService
from src.pipelines.feature_eng_pipeline import SimilarityFilterService
from src.pipelines.inference_pipeline import ClaimClassificationService


class TestClaimExtractionService:
    """Test claim extraction service"""

    def test_service_initialization(self):
        """Test that service initializes correctly"""
        service = ClaimExtractionService()
        assert service.google_api_key is not None
        assert service.fact_checker_api_key is not None
        assert service.google_factcheck_url is not None
        assert service.fact_checker_url is not None

    def test_map_google_claims_empty(self):
        """Test mapping empty Google API response"""
        service = ClaimExtractionService()
        result = service.map_google_claims({})
        assert result == []

    def test_map_google_claims_with_data(self):
        """Test mapping Google API response with data"""
        service = ClaimExtractionService()

        mock_response = {
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
                            "otherField": "otherValue",
                        }
                    ],
                }
            ]
        }

        result = service.map_google_claims(mock_response)
        assert len(result) == 1
        assert result[0]["claim"] == "Test claim"
        assert result[0]["claimant"] == "Test claimant"
        assert result[0]["publisher"] == "Test Publisher"
        assert result[0]["rating"] == "False"
        assert result[0]["source_api"] == "Google FactCheckTools"
        assert "otherField" in result[0]["other"]

    def test_map_rapidapi_claims_empty(self):
        """Test mapping empty RapidAPI response"""
        service = ClaimExtractionService()
        result = service.map_rapidapi_claims({})
        assert result == []

    def test_map_rapidapi_claims_with_data(self):
        """Test mapping RapidAPI response with data"""
        service = ClaimExtractionService()

        mock_response = {
            "data": [
                {
                    "claim_text": "Test claim",
                    "claimant": "Test claimant",
                    "claim_datetime_utc": "2023-01-01",
                    "claim_reviews": [
                        {
                            "publisher": "Test Publisher",
                            "review_link": "https://test.com",
                            "review_text": "False",
                            "otherField": "otherValue",
                        }
                    ],
                }
            ]
        }

        result = service.map_rapidapi_claims(mock_response)
        assert len(result) == 1
        assert result[0]["claim"] == "Test claim"
        assert result[0]["claimant"] == "Test claimant"
        assert result[0]["publisher"] == "Test Publisher"
        assert result[0]["rating"] == "False"
        assert result[0]["source_api"] == "RapidAPI Fact-Checker"
        assert "otherField" in result[0]["other"]


class TestSimilarityFilterService:
    """Test similarity filter service"""

    def test_service_initialization(self):
        """Test that service initializes correctly"""
        service = SimilarityFilterService()
        assert service.model is not None
        assert service.model_name is not None

    def test_cosine_similarity(self):
        """Test cosine similarity calculation"""
        service = SimilarityFilterService()

        import numpy as np

        # Test identical vectors
        a = np.array([1, 0, 0])
        b = np.array([1, 0, 0])
        similarity = service.cosine_similarity(a, b)
        assert abs(similarity - 1.0) < 1e-6

        # Test orthogonal vectors
        a = np.array([1, 0, 0])
        b = np.array([0, 1, 0])
        similarity = service.cosine_similarity(a, b)
        assert abs(similarity - 0.0) < 1e-6

    def test_filter_claims_by_similarity_empty(self):
        """Test filtering empty claims list"""
        service = SimilarityFilterService()
        result = service.filter_claims_by_similarity([], "test query")
        assert result == []

    def test_filter_claims_by_similarity_with_data(self):
        """Test filtering claims with data"""
        service = SimilarityFilterService()

        claims = [
            {"claim": "Sugar causes diabetes"},
            {"claim": "Water is wet"},
            {"claim": "The sky is blue"},
        ]

        result = service.filter_claims_by_similarity(claims, "Sugar causes diabetes", 0.5)

        # Should return at least the exact match
        assert len(result) >= 1
        assert "query_similarity_score" in result[0]
        assert result[0]["query_similarity_score"] >= 0.5


class TestClaimClassificationService:
    """Test claim classification service"""

    def test_service_initialization(self):
        """Test that service initializes correctly"""
        service = ClaimClassificationService()
        assert service.classifier is not None
        assert service.candidate_labels is not None
        assert len(service.candidate_labels) == 3

    def test_fast_keyword_classification_true(self):
        """Test keyword classification for true claims"""
        service = ClaimClassificationService()

        test_cases = [
            "This is true",
            "The claim is correct",
            "This is accurate information",
            "Verified fact",
        ]

        for text in test_cases:
            result = service.fast_keyword_classification(text)
            assert result == "True"

    def test_fast_keyword_classification_false(self):
        """Test keyword classification for false claims"""
        service = ClaimClassificationService()

        test_cases = [
            "This is false",
            "The claim is misleading",
            "This is incorrect",
            "Debunked information",
            "This is fake",
        ]

        for text in test_cases:
            result = service.fast_keyword_classification(text)
            assert result == "False or Misleading"

    def test_fast_keyword_classification_no_info(self):
        """Test keyword classification for insufficient information"""
        service = ClaimClassificationService()

        test_cases = [
            "Not enough evidence",
            "No proof available",
            "Inconclusive results",
            "Unclear information",
        ]

        for text in test_cases:
            result = service.fast_keyword_classification(text)
            assert result == "Not enough information found"

    def test_classify_from_original_rating(self):
        """Test classification from original rating"""
        service = ClaimClassificationService()

        # Test false rating
        result = service.classify_from_original_rating("False")
        assert result == "False or Misleading"

        # Test misleading rating
        result = service.classify_from_original_rating("Misleading claim")
        assert result == "False or Misleading"

        # Test true rating
        result = service.classify_from_original_rating("True")
        assert result == "True"

        # Test no info rating
        result = service.classify_from_original_rating("Not enough information")
        assert result == "Not enough information found"

    def test_classify_claim_with_original_rating(self):
        """Test claim classification with original rating priority"""
        service = ClaimClassificationService()

        # Test that original rating takes priority
        result = service.classify_claim("This is true", "False")
        assert result == "False or Misleading"

        result = service.classify_claim("This is false", "True")
        assert result == "True"

    def test_classify_claims_batch(self):
        """Test batch classification"""
        service = ClaimClassificationService()

        claims = [
            {"claim": "This is true", "rating": "True"},
            {"claim": "This is false", "rating": "False"},
            {"claim": "This is unclear", "rating": "Not enough info"},
        ]

        result = service.classify_claims_batch(claims)

        assert len(result) == 3
        assert result[0]["normalized_rating"] == "True"
        assert result[1]["normalized_rating"] == "False or Misleading"
        assert result[2]["normalized_rating"] == "Not enough information found"


def run_unit_tests():
    """Run all unit tests manually"""
    print("=" * 60)
    print("FactScreen Services Unit Test Suite")
    print("=" * 60)

    try:
        # Test claim extraction service
        print("Testing ClaimExtractionService...")
        test_extract = TestClaimExtractionService()
        test_extract.test_service_initialization()
        test_extract.test_map_google_claims_empty()
        test_extract.test_map_google_claims_with_data()
        test_extract.test_map_rapidapi_claims_empty()
        test_extract.test_map_rapidapi_claims_with_data()
        print("✅ ClaimExtractionService tests passed")

        # Test similarity filter service
        print("\nTesting SimilarityFilterService...")
        test_similarity = TestSimilarityFilterService()
        test_similarity.test_service_initialization()
        test_similarity.test_cosine_similarity()
        test_similarity.test_filter_claims_by_similarity_empty()
        test_similarity.test_filter_claims_by_similarity_with_data()
        print("✅ SimilarityFilterService tests passed")

        # Test classification service
        print("\nTesting ClaimClassificationService...")
        test_classifier = TestClaimClassificationService()
        test_classifier.test_service_initialization()
        test_classifier.test_fast_keyword_classification_true()
        test_classifier.test_fast_keyword_classification_false()
        test_classifier.test_fast_keyword_classification_no_info()
        test_classifier.test_classify_from_original_rating()
        test_classifier.test_classify_claim_with_original_rating()
        test_classifier.test_classify_claims_batch()
        print("✅ ClaimClassificationService tests passed")

        print("\n" + "=" * 60)
        print("✅ All unit tests passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    run_unit_tests()
