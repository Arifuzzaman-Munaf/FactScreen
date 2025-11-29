"""REST API Route Integration Tests for FactScreen Application.

This module contains integration tests that verify complete workflows
across multiple components of the FactScreen fact-checking application.
"""

import pytest
import allure
from unittest.mock import patch
from fastapi.testclient import TestClient
from io import BytesIO

from src.app.main import app
from src.app.models.schemas import (
    AggregatedResult,
    ProviderResult,
    Verdict,
    ProviderName,
    AnalyzeRequest,
)
from src.app.models.claim_models import ClaimRequest, FilteredClaimsRequest


@pytest.fixture
def client():
    """
    Create and return a FastAPI test client instance.

    Returns:
        TestClient: Configured test client for the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def mock_aggregated_result():
    """
    Create a mock AggregatedResult object for testing purposes.

    Returns:
        AggregatedResult: Mock fact-checking result with sample data from multiple providers.
    """
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
def mock_claims_data():
    """
    Create mock claims data for testing search and filtering endpoints.

    Returns:
        list: List of dictionaries containing sample claim data from different sources.
    """
    return [
        {
            "claim": "Sugar causes diabetes",
            "claimant": "Health expert",
            "claim_date": "2023-01-01",
            "publisher": "Test Publisher",
            "review_link": "https://test.com",
            "rating": "False",
            "source_api": "Google FactCheckTools",
        },
        {
            "claim": "Water is essential for life",
            "claimant": "Science expert",
            "claim_date": "2023-01-01",
            "publisher": "Test Publisher 2",
            "review_link": "https://test2.com",
            "rating": "True",
            "source_api": "RapidAPI Fact-Checker",
        },
    ]


class TestHealthEndpoint:
    """
    Test suite for the health check endpoint.

    Verifies that the application health monitoring endpoint returns correct status
    information indicating the API is operational.
    """

    @allure.severity(allure.severity_level.NORMAL)
    def test_health_endpoint(self, client):
        """
        Verify that the health endpoint returns a successful status response.

        Args:
            client: FastAPI test client fixture.
        """
        response = client.get("/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestRootEndpoint:
    """
    Test suite for the root application endpoint.

    Verifies that the root endpoint returns application metadata including name,
    version, and health check endpoint information.
    """

    @allure.severity(allure.severity_level.NORMAL)
    def test_root_endpoint(self, client):
        """
        Verify that the root endpoint returns application information.

        Args:
            client: FastAPI test client fixture.
        """
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "health" in data


class TestValidateEndpoint:
    """
    Test suite for the claim validation endpoint.

    Tests the /v1/validate endpoint which accepts text or URL inputs and returns
    aggregated fact-checking results from multiple providers.
    """

    @patch("src.app.api.routes.validate_text")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_validate_with_text(self, mock_validate, client, mock_aggregated_result):
        """
        Test claim validation with text input.

        Verifies that text-based validation requests are processed correctly and
        return proper aggregated results.

        Args:
            mock_validate: Mocked validate_text function.
            client: FastAPI test client fixture.
            mock_aggregated_result: Mock aggregated result fixture.
        """
        mock_validate.return_value = mock_aggregated_result

        request = AnalyzeRequest(text="Sugar causes diabetes")
        response = client.post("/v1/validate", json=request.model_dump())

        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert data["result"]["claim_text"] == "Test claim"
        assert data["result"]["verdict"] == "true"

    @patch("src.app.api.routes.validate_url")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_validate_with_url(self, mock_validate, client, mock_aggregated_result):
        """
        Test claim validation with URL input.

        Verifies that URL-based validation requests extract content from the provided
        URL and return proper aggregated results.

        Args:
            mock_validate: Mocked validate_url function.
            client: FastAPI test client fixture.
            mock_aggregated_result: Mock aggregated result fixture.
        """
        mock_validate.return_value = mock_aggregated_result

        request = AnalyzeRequest(url="https://example.com/article")
        response = client.post("/v1/validate", json=request.model_dump(mode="json"))

        assert response.status_code == 200
        data = response.json()
        assert "result" in data

    @allure.severity(allure.severity_level.NORMAL)
    def test_validate_without_text_or_url(self, client):
        """
        Test validation endpoint error handling when no input is provided.

        Verifies that the endpoint returns a 400 Bad Request error when neither
        text nor URL is provided in the request.

        Args:
            client: FastAPI test client fixture.
        """
        request = AnalyzeRequest()
        response = client.post("/v1/validate", json=request.model_dump())

        assert response.status_code == 400
        assert "text or url" in response.json()["detail"].lower()

    @patch("src.app.api.routes.validate_text")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validate_error_handling(self, mock_validate, client):
        """
        Test validation endpoint error handling for internal exceptions.

        Verifies that internal errors during validation are properly caught and
        returned as 500 Internal Server Error responses.

        Args:
            mock_validate: Mocked validate_text function configured to raise exception.
            client: FastAPI test client fixture.
        """
        mock_validate.side_effect = Exception("Test error")

        request = AnalyzeRequest(text="Test claim")
        response = client.post("/v1/validate", json=request.model_dump())

        assert response.status_code == 500
        assert "error" in response.json()["detail"].lower()


class TestValidatePDFEndpoint:
    """
    Test suite for the PDF report generation endpoint from validation.

    Tests the /v1/validate/pdf endpoint which validates a claim and generates
    a PDF report containing the fact-checking results.
    """

    @patch("src.app.api.routes.validate_text")
    @patch("src.app.api.routes.generate_pdf_report")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validate_pdf_with_text(
        self, mock_generate_pdf, mock_validate, client, mock_aggregated_result
    ):
        """
        Test PDF generation with text input.

        Verifies that text-based validation requests generate PDF reports with
        correct content type and filename headers.

        Args:
            mock_generate_pdf: Mocked PDF generation function.
            mock_validate: Mocked validate_text function.
            client: FastAPI test client fixture.
            mock_aggregated_result: Mock aggregated result fixture.
        """
        mock_validate.return_value = mock_aggregated_result
        mock_pdf = BytesIO(b"fake pdf content")
        mock_generate_pdf.return_value = mock_pdf

        request = AnalyzeRequest(text="Sugar causes diabetes")
        response = client.post("/v1/validate/pdf", json=request.model_dump())

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "factcheck-report" in response.headers["content-disposition"]

    @patch("src.app.api.routes.validate_url")
    @patch("src.app.api.routes.generate_pdf_report")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validate_pdf_with_url(
        self, mock_generate_pdf, mock_validate, client, mock_aggregated_result
    ):
        """
        Test PDF generation with URL input.

        Verifies that URL-based validation requests generate PDF reports correctly.

        Args:
            mock_generate_pdf: Mocked PDF generation function.
            mock_validate: Mocked validate_url function.
            client: FastAPI test client fixture.
            mock_aggregated_result: Mock aggregated result fixture.
        """
        mock_validate.return_value = mock_aggregated_result
        mock_pdf = BytesIO(b"fake pdf content")
        mock_generate_pdf.return_value = mock_pdf

        request = AnalyzeRequest(url="https://example.com/article")
        response = client.post("/v1/validate/pdf", json=request.model_dump(mode="json"))

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

    @allure.severity(allure.severity_level.NORMAL)
    def test_validate_pdf_without_input(self, client):
        """
        Test PDF generation endpoint error handling when no input is provided.

        Verifies that the endpoint returns a 400 Bad Request error when neither
        text nor URL is provided.

        Args:
            client: FastAPI test client fixture.
        """
        request = AnalyzeRequest()
        response = client.post("/v1/validate/pdf", json=request.model_dump())

        assert response.status_code == 400


class TestReportPDFEndpoint:
    """
    Test suite for the PDF report generation endpoint from existing results.

    Tests the /v1/report/pdf endpoint which generates PDF reports from pre-existing
    AggregatedResult objects without re-running validation.
    """

    @patch("src.app.api.routes.generate_pdf_report")
    @allure.severity(allure.severity_level.NORMAL)
    def test_generate_pdf_from_result(self, mock_generate_pdf, client, mock_aggregated_result):
        """
        Test PDF generation from existing aggregated result.

        Verifies that PDF reports can be generated from existing AggregatedResult
        objects with correct content type and filename headers.

        Args:
            mock_generate_pdf: Mocked PDF generation function.
            client: FastAPI test client fixture.
            mock_aggregated_result: Mock aggregated result fixture.
        """
        mock_pdf = BytesIO(b"fake pdf content")
        mock_generate_pdf.return_value = mock_pdf

        response = client.post(
            "/v1/report/pdf", json=mock_aggregated_result.model_dump(mode="json")
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "factcheck-report" in response.headers["content-disposition"]

    @patch("src.app.api.routes.generate_pdf_report")
    @allure.severity(allure.severity_level.NORMAL)
    def test_generate_pdf_error_handling(self, mock_generate_pdf, client, mock_aggregated_result):
        """
        Test PDF generation endpoint error handling for internal exceptions.

        Verifies that errors during PDF generation are properly caught and returned
        as 500 Internal Server Error responses.

        Args:
            mock_generate_pdf: Mocked PDF generation function configured to raise exception.
            client: FastAPI test client fixture.
            mock_aggregated_result: Mock aggregated result fixture.
        """
        mock_generate_pdf.side_effect = Exception("PDF generation failed")

        response = client.post(
            "/v1/report/pdf", json=mock_aggregated_result.model_dump(mode="json")
        )

        assert response.status_code == 500
        assert "error" in response.json()["detail"].lower()


class TestClaimsSearchEndpoint:
    """
    Test suite for the claims search endpoint.

    Tests the /v1/claims/search endpoint which searches for fact-checked claims
    from multiple sources based on a query string.
    """

    @patch("src.app.api.routes.claim_extraction_service")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_claims_success(self, mock_service, client, mock_claims_data):
        """
        Test successful claims search operation.

        Verifies that the search endpoint returns properly formatted results with
        correct claim data and metadata.

        Args:
            mock_service: Mocked claim extraction service.
            client: FastAPI test client fixture.
            mock_claims_data: Mock claims data fixture.
        """
        mock_service.get_combined_claims.return_value = mock_claims_data

        request = ClaimRequest(query="Sugar causes diabetes", language_code="en", page_size=10)
        response = client.post("/v1/claims/search", json=request.model_dump())

        assert response.status_code == 200
        data = response.json()
        assert "claims" in data
        assert "total_count" in data
        assert "query" in data
        assert data["total_count"] == 2

    @patch("src.app.api.routes.claim_extraction_service")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_claims_empty(self, mock_service, client):
        """
        Test claims search with no matching results.

        Verifies that the endpoint handles empty result sets gracefully and returns
        appropriate response structure.

        Args:
            mock_service: Mocked claim extraction service configured to return empty list.
            client: FastAPI test client fixture.
        """
        mock_service.get_combined_claims.return_value = []

        request = ClaimRequest(query="Nonexistent claim", language_code="en", page_size=10)
        response = client.post("/v1/claims/search", json=request.model_dump())

        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 0
        assert len(data["claims"]) == 0

    @patch("src.app.api.routes.claim_extraction_service")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_claims_error(self, mock_service, client):
        """
        Test claims search endpoint error handling for service exceptions.

        Verifies that errors during claims extraction are properly caught and returned
        as 500 Internal Server Error responses.

        Args:
            mock_service: Mocked claim extraction service configured to raise exception.
            client: FastAPI test client fixture.
        """
        mock_service.get_combined_claims.side_effect = Exception("API error")

        request = ClaimRequest(query="Test query", language_code="en", page_size=10)
        response = client.post("/v1/claims/search", json=request.model_dump())

        assert response.status_code == 500
        assert "error" in response.json()["detail"].lower()


class TestFilteredClaimsEndpoint:
    """
    Test suite for the filtered claims endpoint.

    Tests the /v1/claims/filtered endpoint which searches for claims, filters them
    by similarity, and assigns classification labels using ML models.
    """

    @patch("src.app.api.routes.classification_service")
    @patch("src.app.api.routes.similarity_filter_service")
    @patch("src.app.api.routes.claim_extraction_service")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filtered_claims_success(
        self, mock_extract, mock_filter, mock_classify, client, mock_claims_data
    ):
        """
        Test successful filtered claims request with similarity filtering and classification.

        Verifies that the endpoint properly chains claim extraction, similarity filtering,
        and classification services to return enriched claim data.

        Args:
            mock_extract: Mocked claim extraction service.
            mock_filter: Mocked similarity filter service.
            mock_classify: Mocked classification service.
            client: FastAPI test client fixture.
            mock_claims_data: Mock claims data fixture.
        """
        mock_extract.get_combined_claims.return_value = mock_claims_data
        mock_filter.filter_claims_by_similarity.return_value = mock_claims_data
        mock_classify.classify_claims_batch.return_value = [
            {**claim, "normalized_rating": "False or Misleading", "query_similarity_score": 0.8}
            for claim in mock_claims_data
        ]
        mock_classify.get_classification_labels.return_value = [
            "True",
            "False or Misleading",
            "Not enough information found",
        ]

        request = FilteredClaimsRequest(
            query="Sugar causes diabetes",
            language_code="en",
            page_size=10,
            similarity_threshold=0.5,
        )
        response = client.post("/v1/claims/filtered", json=request.model_dump())

        assert response.status_code == 200
        data = response.json()
        assert "claims" in data
        assert "total_count" in data
        assert "similarity_threshold" in data
        assert "classification_labels" in data

    @patch("src.app.api.routes.claim_extraction_service")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filtered_claims_error(self, mock_service, client):
        """
        Test filtered claims endpoint error handling for processing exceptions.

        Verifies that errors during claim processing are properly caught and returned
        as 500 Internal Server Error responses.

        Args:
            mock_service: Mocked claim extraction service configured to raise exception.
            client: FastAPI test client fixture.
        """
        mock_service.get_combined_claims.side_effect = Exception("Processing error")

        request = FilteredClaimsRequest(
            query="Test query", language_code="en", page_size=10, similarity_threshold=0.5
        )
        response = client.post("/v1/claims/filtered", json=request.model_dump())

        assert response.status_code == 500
        assert "error" in response.json()["detail"].lower()