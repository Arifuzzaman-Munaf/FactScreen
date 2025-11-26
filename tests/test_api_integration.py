#!/usr/bin/env python3
"""
Test script for FactScreen API endpoints
"""

import requests

# API base URL
BASE_URL = "http://localhost:8000/v1"


def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_search_claims():
    """Test the search claims endpoint"""
    print("Testing search claims endpoint...")

    payload = {"query": "Sugar causes diabetes", "language_code": "en", "page_size": 10}

    response = requests.post(f"{BASE_URL}/claims/search", json=payload)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Total claims found: {data['total_count']}")
        print(f"Query: {data['query']}")

        # Print first few claims
        for i, claim in enumerate(data["claims"][:3]):
            print(f"\nClaim {i + 1}:")
            print(f"  Text: {claim.get('claim', 'N/A')}")
            print(f"  Claimant: {claim.get('claimant', 'N/A')}")
            print(f"  Rating: {claim.get('rating', 'N/A')}")
            print(f"  Source: {claim.get('source_api', 'N/A')}")
    else:
        print(f"Error: {response.text}")
    print()


def test_filtered_claims():
    """Test the filtered claims endpoint"""
    print("Testing filtered claims endpoint...")

    payload = {
        "query": "Sugar causes diabetes",
        "language_code": "en",
        "page_size": 10,
        "similarity_threshold": 0.75,
    }

    response = requests.post(f"{BASE_URL}/claims/filtered", json=payload)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Total filtered claims: {data['total_count']}")
        print(f"Query: {data['query']}")
        print(f"Similarity threshold: {data['similarity_threshold']}")
        print(f"Classification labels: {data['classification_labels']}")

        # Print first few claims
        for i, claim in enumerate(data["claims"][:3]):
            print(f"\nFiltered Claim {i + 1}:")
            print(f"  Text: {claim.get('claim', 'N/A')}")
            print(f"  Claimant: {claim.get('claimant', 'N/A')}")
            print(f"  Rating: {claim.get('rating', 'N/A')}")
            print(f"  Source: {claim.get('source_api', 'N/A')}")
            print(f"  Similarity Score: {claim.get('query_similarity_score', 'N/A')}")
            print(f"  Normalized Rating: {claim.get('normalized_rating', 'N/A')}")
    else:
        print(f"Error: {response.text}")
    print()


def main():
    """Run all tests"""
    print("=" * 50)
    print("FactScreen API Test Suite")
    print("=" * 50)

    try:
        test_health()
        test_search_claims()
        test_filtered_claims()

        print("=" * 50)
        print("All tests completed!")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
