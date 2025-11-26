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
        """Fetch claims from Google Fact Check API"""
        try:
            params = {"query": query, "languageCode": language_code, "pageSize": page_size}
            endpoint = f"{self.google_factcheck_url}/{self.google_factcheck_endpoint}"
            response = requests.get(
                endpoint,
                params={**params, "key": self.google_api_key},
                timeout=settings.request_timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Google claims: {e}")
            return {"claims": []}

    def fetch_rapidapi_claims(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Fetch claims from RapidAPI Fact-Checker"""
        try:
            conn = http.client.HTTPSConnection(self.fact_checker_url)
            headers = {
                "x-rapidapi-key": self.fact_checker_api_key,
                "x-rapidapi-host": self.fact_checker_host,
            }
            encoded_query = urllib.parse.quote_plus(query)
            conn.request(
                "GET",
                f"/{self.fact_checker_endpoint}?query={encoded_query}&limit={limit}",
                headers=headers,
            )
            res = conn.getresponse()
            data = res.read()
            return json.loads(data.decode("utf-8"))
        except Exception as e:
            print(f"Error fetching RapidAPI claims: {e}")
            return {"data": []}

    def map_google_claims(self, api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map Google API response to standardized format"""
        output = []
        for claim in api_response.get("claims", []):
            for review in claim.get("claimReview", []):
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
        """Map RapidAPI response to standardized format"""
        output = []
        for claim in api_response.get("data", []):
            for review in claim.get("claim_reviews", []):
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
        """Get combined claims from all available sources"""
        combined_results = []

        # Fetch from Google Fact Check
        google_response = self.fetch_google_claims(query, language_code, page_size)
        combined_results.extend(self.map_google_claims(google_response))

        # Fetch from RapidAPI Fact-Checker
        rapidapi_response = self.fetch_rapidapi_claims(query, page_size)
        combined_results.extend(self.map_rapidapi_claims(rapidapi_response))

        return combined_results
