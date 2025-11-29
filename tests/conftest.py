"""
Pytest configuration and fixtures for FactScreen tests
"""

import pytest
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import requests

from src.app.models.schemas import (
    AggregatedResult,
    ProviderResult,
    Verdict,
    ProviderName,
)


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
                        "reviewDate": "2023-01-02",
                    }
                ],
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
                        "review_date": "2023-01-02",
                    }
                ],
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
            "other": {},
        },
        {
            "claim": "Water is essential for life",
            "claimant": "Science expert",
            "claim_date": "2023-01-01",
            "publisher": "Test Publisher",
            "review_link": "https://test.com",
            "rating": "True",
            "source_api": "RapidAPI Fact-Checker",
            "other": {},
        },
    ]


@pytest.fixture
def api_base_url():
    """Base URL for API testing"""
    return "http://localhost:8000/v1"


@pytest.fixture(scope="session")
def server_required():
    """Fixture to check if server is required for tests"""

    try:
        response = requests.get("http://localhost:8000/v1/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


@pytest.fixture
def skip_if_no_server(server_required):
    """Skip test if server is not running"""
    if not server_required:
        pytest.skip("Server not running - skipping integration test")


@pytest.fixture
def mock_aggregated_result():
    """Create a mock AggregatedResult for testing."""
    # Return a mock AggregatedResult for testing
    return AggregatedResult(
        claim_text="Test claim",
        verdict=Verdict.TRUE,
        votes={Verdict.TRUE: 2, Verdict.MISLEADING: 1},
        provider_results=[
            ProviderResult(
                provider=ProviderName.GOOGLE,
                verdict=Verdict.TRUE,
                rating="True",
                title="Test Title",
                summary="Test Summary",
            ),
            ProviderResult(
                provider=ProviderName.RAPID,
                verdict=Verdict.TRUE,
                rating="True",
                title="Test Title 2",
                summary="Test Summary 2",
            ),
        ],
        providers_checked=[ProviderName.GOOGLE, ProviderName.RAPID],
        confidence=0.85,
        explanation="Test explanation",
    )


@pytest.fixture
def mock_provider_results():
    """Create mock provider results for testing."""
    return [
        ProviderResult(
            provider=ProviderName.GOOGLE,
            verdict=Verdict.TRUE,
            rating="True",
            title="Google Title",
            summary="Google summary",
            source_url="https://google-test.com",
        ),
        ProviderResult(
            provider=ProviderName.RAPID,
            verdict=Verdict.MISLEADING,
            rating="False",
            title="Rapid Title",
            summary="Rapid summary",
            source_url="https://rapid-test.com",
        ),
    ]


@pytest.fixture
def mock_sources():
    """Create mock sources for testing."""
    return [
        {
            "snippet": "Test snippet 1",
            "verdict": "True",
            "rating": "True",
            "source": "Test Source 1",
            "url": "https://example.com/1",
        },
        {
            "snippet": "Test snippet 2",
            "verdict": "False",
            "rating": "False",
            "source": "Test Source 2",
            "url": "https://example.com/2",
        },
    ]