"""
Pytest configuration and fixtures for FactScreen tests
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def mock_google_api_response():
    """Mock Google Fact Check API response"""
    return {
        "claims": [
            {
                "text": "Test claim from Google",
                "claimant": "Test claimant",
                "claimDate": "2023-01-01",
                "claimReview": [
                    {
                        "publisher": {"name": "Google Publisher"},
                        "url": "https://google-test.com",
                        "textualRating": "False",
                        "reviewDate": "2023-01-02"
                    }
                ]
            }
        ]
    }

@pytest.fixture
def mock_rapidapi_response():
    """Mock RapidAPI Fact-Checker response"""
    return {
        "data": [
            {
                "claim_text": "Test claim from RapidAPI",
                "claimant": "Test claimant",
                "claim_datetime_utc": "2023-01-01",
                "claim_reviews": [
                    {
                        "publisher": "RapidAPI Publisher",
                        "review_link": "https://rapidapi-test.com",
                        "review_text": "True",
                        "review_date": "2023-01-02"
                    }
                ]
            }
        ]
    }

@pytest.fixture
def sample_claims():
    """Sample claims data for testing"""
    return [
        {
            "claim": "Sugar causes diabetes",
            "claimant": "Health expert",
            "claim_date": "2023-01-01",
            "publisher": "Test Publisher",
            "review_link": "https://test.com",
            "rating": "False",
            "source_api": "Google FactCheckTools",
            "other": {}
        },
        {
            "claim": "Water is essential for life",
            "claimant": "Science expert",
            "claim_date": "2023-01-01",
            "publisher": "Test Publisher",
            "review_link": "https://test.com",
            "rating": "True",
            "source_api": "RapidAPI Fact-Checker",
            "other": {}
        }
    ]

@pytest.fixture
def api_base_url():
    """Base URL for API testing"""
    return "http://localhost:8000/v1"

@pytest.fixture(scope="session")
def server_required():
    """Fixture to check if server is required for tests"""
    import requests
    try:
        response = requests.get("http://localhost:8000/v1/health", timeout=5)
        return response.status_code == 200
    except:
        return False

@pytest.fixture
def skip_if_no_server(server_required):
    """Skip test if server is not running"""
    if not server_required:
        pytest.skip("Server not running - skipping integration test")
