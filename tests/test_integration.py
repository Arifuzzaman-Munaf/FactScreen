#!/usr/bin/env python3
"""
Integration tests for FactScreen API endpoints
"""

import requests

# API base URL
BASE_URL = "http://localhost:8000/v1"


class TestAPIHealth:
    """Test health endpoint"""

    def test_health_endpoint(self):
        """Test the health endpoint"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestClaimsSearch:
    """Test claims search endpoint"""

    def test_search_claims_basic(self):
        """Test basic claims search"""
        payload = {"query": "Sugar causes diabetes", "language_code": "en", "page_size": 5}

        response = requests.post(f"{BASE_URL}/claims/search", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "claims" in data
        assert "total_count" in data
        assert "query" in data
        assert data["query"] == "Sugar causes diabetes"
        assert isinstance(data["claims"], list)
        assert data["total_count"] >= 0

    def test_search_claims_validation(self):
        """Test claims search with invalid input"""
        # Test with empty query
        payload = {"query": "", "language_code": "en", "page_size": 5}

        response = requests.post(f"{BASE_URL}/claims/search", json=payload)
        # Should return 422 for validation error
        assert response.status_code == 422

    def test_search_claims_different_queries(self):
        """Test search with different types of queries"""
        test_queries = ["Climate change is a hoax", "Vaccines cause autism", "COVID-19 is fake"]

        for query in test_queries:
            payload = {"query": query, "language_code": "en", "page_size": 3}

            response = requests.post(f"{BASE_URL}/claims/search", json=payload)
            assert response.status_code == 200

            data = response.json()
            assert data["query"] == query
            assert isinstance(data["claims"], list)


class TestFilteredClaims:
    """Test filtered claims endpoint"""

    def test_filtered_claims_basic(self):
        """Test basic filtered claims"""
        payload = {
            "query": "Sugar causes diabetes",
            "language_code": "en",
            "page_size": 5,
            "similarity_threshold": 0.75,
        }

        response = requests.post(f"{BASE_URL}/claims/filtered", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "claims" in data
        assert "total_count" in data
        assert "query" in data
        assert "similarity_threshold" in data
        assert "classification_labels" in data
        assert data["query"] == "Sugar causes diabetes"
        assert data["similarity_threshold"] == 0.75
        assert isinstance(data["claims"], list)
        assert isinstance(data["classification_labels"], list)

    def test_filtered_claims_similarity_threshold(self):
        """Test filtered claims with different similarity thresholds"""
        query = "Sugar causes diabetes"

        for threshold in [0.5, 0.75, 0.9]:
            payload = {
                "query": query,
                "language_code": "en",
                "page_size": 5,
                "similarity_threshold": threshold,
            }

            response = requests.post(f"{BASE_URL}/claims/filtered", json=payload)
            assert response.status_code == 200

            data = response.json()
            assert data["similarity_threshold"] == threshold

            # Higher threshold should generally return fewer or equal results
            if threshold > 0.5:
                # Check that similarity scores are above threshold
                for claim in data["claims"]:
                    if "query_similarity_score" in claim:
                        assert claim["query_similarity_score"] >= threshold

    def test_filtered_claims_classification(self):
        """Test that filtered claims have proper classification"""
        payload = {
            "query": (
                "PM Narendra Modi has announced a Diwali cash gift "
                "worth ₹10,000 for all citizens"
            ),
            "language_code": "en",
            "page_size": 5,
            "similarity_threshold": 0.7,
        }

        response = requests.post(f"{BASE_URL}/claims/filtered", json=payload)
        assert response.status_code == 200

        data = response.json()

        # Check that all claims have normalized_rating
        for claim in data["claims"]:
            assert "normalized_rating" in claim
            assert claim["normalized_rating"] in [
                "True",
                "False or Misleading",
                "Not enough information found",
            ]

            # Check that similarity scores are present and valid
            if "query_similarity_score" in claim:
                assert 0.0 <= claim["query_similarity_score"] <= 1.0


class TestAPIErrorHandling:
    """Test API error handling"""

    def test_invalid_endpoint(self):
        """Test invalid endpoint"""
        response = requests.get(f"{BASE_URL}/invalid")
        assert response.status_code == 404

    def test_invalid_method(self):
        """Test invalid HTTP method"""
        response = requests.get(f"{BASE_URL}/claims/search")
        assert response.status_code == 405  # Method not allowed

    def test_malformed_json(self):
        """Test malformed JSON request"""
        response = requests.post(
            f"{BASE_URL}/claims/search",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422


def run_integration_tests():
    """Run all integration tests manually"""
    print("=" * 60)
    print("FactScreen API Integration Test Suite")
    print("=" * 60)

    try:
        # Test health
        print("Testing health endpoint...")
        test_health = TestAPIHealth()
        test_health.test_health_endpoint()
        print("✅ Health endpoint test passed")

        # Test claims search
        print("\nTesting claims search endpoint...")
        test_search = TestClaimsSearch()
        test_search.test_search_claims_basic()
        print("✅ Claims search basic test passed")

        test_search.test_search_claims_different_queries()
        print("✅ Claims search different queries test passed")

        # Test filtered claims
        print("\nTesting filtered claims endpoint...")
        test_filtered = TestFilteredClaims()
        test_filtered.test_filtered_claims_basic()
        print("✅ Filtered claims basic test passed")

        test_filtered.test_filtered_claims_classification()
        print("✅ Filtered claims classification test passed")

        print("\n" + "=" * 60)
        print("✅ All integration tests passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    run_integration_tests()
