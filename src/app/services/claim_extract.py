import requests
import json
import http.client
import urllib.parse
from typing import List, Dict, Any
from src.app.core.config import settings


class ClaimExtractionService:
    """Service for extracting claims from Google Fact Check and RapidAPI Fact-Checker"""

    def __init__(self):
        self.google_api_key = settings.google_api_key
        self.google_factcheck_url = settings.google_factcheck_url
        self.google_factcheck_endpoint = settings.google_factcheck_endpoint

        self.fact_checker_api_key = settings.fact_checker_api_key
        self.fact_checker_url = settings.fact_checker_url
        self.fact_checker_host = settings.fact_checker_host
        self.fact_checker_endpoint = settings.fact_checker_endpoint

    def fetch_google_claims(
        self, query: str, language_code: str = "en", page_size: int = 10
    ) -> Dict[str, Any]:
        """Fetch claims from Google Fact Check API
        Args:
            query: The query to search for claims
            language_code: The language code to search for claims
            page_size: The number of claims to return
        Returns:
            A dictionary containing the claims
        """
        # Try to fetch claims from Google Fact Check API
        try:
            # Create the parameters for the request
            params = {"query": query, "languageCode": language_code, "pageSize": page_size}
            # Create the endpoint for the request
            endpoint = f"{self.google_factcheck_url}/{self.google_factcheck_endpoint}"
            # Send the request to the Google Fact Check API
            response = requests.get(
                endpoint,
                params={**params, "key": self.google_api_key},
                timeout=settings.request_timeout,
            )
            # Raise an exception if the request is not successful
            response.raise_for_status()
            # Return the response as a dictionary
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Google claims: {e}")
            return {"claims": []}

    def fetch_rapidapi_claims(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Fetch claims from RapidAPI Fact-Checker
        Args:
            query: The query to search for claims
            limit: The number of claims to return
        Returns:
            A dictionary containing the claims
        """
        # Try to fetch claims from RapidAPI Fact-Checker
        try:
            # Create a connection to the RapidAPI Fact-Checker
            conn = http.client.HTTPSConnection(self.fact_checker_url)
            # Create the headers for the request
            headers = {
                "x-rapidapi-key": self.fact_checker_api_key,
                "x-rapidapi-host": self.fact_checker_host,
            }
            # Encode the query for the request
            encoded_query = urllib.parse.quote_plus(query)
            # Create the endpoint for the request
            endpoint = f"/{self.fact_checker_endpoint}?query={encoded_query}&limit={limit}"
            # Send the request to the RapidAPI Fact-Checker
            conn.request(
                "GET",
                f"/{self.fact_checker_endpoint}?query={encoded_query}&limit={limit}",
                headers=headers,
            )
            # Get the response from the RapidAPI Fact-Checker
            res = conn.getresponse()
            # Read the response data
            data = res.read()
            # Return the response as a dictionary
            return json.loads(data.decode("utf-8"))
        # Raise an exception if the request is not successful
        except Exception as e:
            print(f"Error fetching RapidAPI claims: {e}")
            return {"data": []}

    def map_google_claims(self, api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map Google API response to standardized format
        Args:
            api_response: The response from the Google Fact Check API
        Returns:
            A list of claims
        """
        # Try to map the Google API response to a standardized format
        output = []
        # Iterate over the claims in the API response
        for claim in api_response.get("claims", []):
            # Iterate over the reviews in the claim
            for review in claim.get("claimReview", []):
                # Add the claim to the output list
                output.append(
                    {
                        "claim": claim.get("text"),
                        "claimant": claim.get("claimant"),
                        "claim_date": claim.get("claimDate"),
                        "publisher": review.get("publisher", {}).get("name"),
                        "review_link": review.get("url"),
                        "rating": review.get("textualRating"),
                        "source_api": "Google FactCheckTools",
                        "other": {
                            k: v
                            for k, v in review.items()
                            if k not in ["textualRating", "url", "publisher"]
                        },
                    }
                )
        return output

    def map_rapidapi_claims(self, api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map RapidAPI response to standardized format
        Args:
            api_response: The response from the RapidAPI Fact-Checker
        Returns:
            A list of claims
        """
        # Try to map the RapidAPI API response to a standardized format
        output = []
        # Iterate over the claims in the API response
        for claim in api_response.get("data", []):
            # Iterate over the reviews in the claim
            for review in claim.get("claim_reviews", []):
                # Add the claim to the output list
                output.append(
                    {
                        "claim": claim.get("claim_text"),
                        "claimant": claim.get("claimant"),
                        "claim_date": claim.get("claim_datetime_utc"),
                        "publisher": review.get("publisher"),
                        "review_link": review.get("review_link"),
                        "rating": review.get("review_text"),
                        "source_api": "RapidAPI Fact-Checker",
                        "other": {
                            k: v
                            for k, v in review.items()
                            if k not in ["review_text", "review_link", "publisher"]
                        },
                    }
                )
        return output

    def get_combined_claims(
        self, query: str, language_code: str = "en", page_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Get combined claims from all available sources
        Args:
            query: The query to search for claims
            language_code: The language code to search for claims
            page_size: The number of claims to return
        Returns:
            A list of claims
        """
        # Try to get combined claims from all available sources
        combined_results = []

        # Fetch from Google Fact Check
        google_response = self.fetch_google_claims(query, language_code, page_size)
        combined_results.extend(self.map_google_claims(google_response))

        # Fetch from RapidAPI Fact-Checker
        rapidapi_response = self.fetch_rapidapi_claims(query, page_size)
        combined_results.extend(self.map_rapidapi_claims(rapidapi_response))

        return combined_results