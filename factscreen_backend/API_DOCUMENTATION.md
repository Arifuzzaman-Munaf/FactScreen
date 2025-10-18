# FactScreen API Documentation

## Overview

FactScreen is a fact-checking API that combines multiple sources to provide comprehensive claim verification. The API offers two main endpoints for searching and analyzing claims.

## Features

- **Multi-source claim extraction**: Integrates Google Fact Check API and RapidAPI Fact-Checker
- **Similarity filtering**: Uses sentence transformers to filter claims by relevance
- **AI-powered classification**: Employs transformer models for claim classification
- **Standardized response format**: Consistent data structure across all sources

## API Endpoints

### 1. Search Claims (`/v1/claims/search`)

Fetches raw claims from multiple fact-checking sources without filtering or classification.

**Method**: `POST`

**Request Body**:
```json
{
  "query": "Sugar causes diabetes",
  "language_code": "en",
  "page_size": 10
}
```

**Response**:
```json
{
  "claims": [
    {
      "claim": "Sugar causes diabetes",
      "claimant": "Health expert",
      "claim_date": "2023-01-15",
      "publisher": "FactCheck.org",
      "review_link": "https://example.com/review",
      "rating": "False",
      "source_api": "Google FactCheckTools",
      "other": {}
    }
  ],
  "total_count": 1,
  "query": "Sugar causes diabetes"
}
```

### 2. Filtered Claims (`/v1/claims/filtered`)

Fetches claims, filters them by similarity, and classifies them using AI models.

**Method**: `POST`

**Request Body**:
```json
{
  "query": "Sugar causes diabetes",
  "language_code": "en",
  "page_size": 10,
  "similarity_threshold": 0.75
}
```

**Response**:
```json
{
  "claims": [
    {
      "claim": "Sugar causes diabetes",
      "claimant": "Health expert",
      "claim_date": "2023-01-15",
      "publisher": "FactCheck.org",
      "review_link": "https://example.com/review",
      "rating": "False",
      "source_api": "Google FactCheckTools",
      "query_similarity_score": 0.95,
      "normalized_rating": "False or Misleading",
      "other": {}
    }
  ],
  "total_count": 1,
  "query": "Sugar causes diabetes",
  "similarity_threshold": 0.75,
  "classification_labels": ["True", "False or Misleading", "Not enough information found"]
}
```

## Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | The claim text to search for |
| `language_code` | string | No | "en" | Language code for the search |
| `page_size` | integer | No | 10 | Number of results to return (1-50) |
| `similarity_threshold` | float | No | 0.75 | Minimum similarity score for filtering (0.0-1.0) |

## Response Fields

### Claim Object
| Field | Type | Description |
|-------|------|-------------|
| `claim` | string | The claim text |
| `claimant` | string | Who made the claim |
| `claim_date` | string | Date when the claim was made |
| `publisher` | string | Publisher of the fact-check |
| `review_link` | string | Link to the fact-check review |
| `rating` | string | Original fact-check rating |
| `source_api` | string | Source API that provided this claim |
| `query_similarity_score` | float | Similarity score with query (filtered endpoint only) |
| `normalized_rating` | string | AI-classified rating (filtered endpoint only) |
| `other` | object | Additional metadata |

## Classification Labels

The AI classifier uses three main categories:
- **"True"**: Claim is accurate or correct
- **"False or Misleading"**: Claim is incorrect or misleading
- **"Not enough information found"**: Insufficient information to determine accuracy

## Setup and Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables** (optional):
   ```bash
   export GOOGLE_API_KEY="your_google_api_key"
   export FACT_CHECKER_API_KEY="your_rapidapi_key"
   ```

3. **Run the server**:
   ```bash
   cd factscreen_backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Test the API**:
   ```bash
   python test_api.py
   ```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## Example Usage

### Python
```python
import requests

# Search for claims
response = requests.post("http://localhost:8000/v1/claims/search", json={
    "query": "Climate change is a hoax",
    "page_size": 5
})

claims = response.json()
print(f"Found {claims['total_count']} claims")

# Get filtered and classified claims
response = requests.post("http://localhost:8000/v1/claims/filtered", json={
    "query": "Climate change is a hoax",
    "similarity_threshold": 0.8
})

filtered_claims = response.json()
for claim in filtered_claims['claims']:
    print(f"Claim: {claim['claim']}")
    print(f"Similarity: {claim['query_similarity_score']}")
    print(f"Classification: {claim['normalized_rating']}")
```

### cURL
```bash
# Search claims
curl -X POST "http://localhost:8000/v1/claims/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Vaccines cause autism", "page_size": 5}'

# Filtered claims
curl -X POST "http://localhost:8000/v1/claims/filtered" \
  -H "Content-Type: application/json" \
  -d '{"query": "Vaccines cause autism", "similarity_threshold": 0.75}'
```

## Error Handling

The API returns standard HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid parameters)
- `500`: Internal server error

Error responses include a `detail` field with the error message:
```json
{
  "detail": "Error searching claims: API key not found"
}
```

## Rate Limits

Please be mindful of API rate limits for the external services:
- Google Fact Check API: 1000 requests per day
- RapidAPI Fact-Checker: Depends on your subscription plan

## Support

For issues or questions, please check the API documentation at `/docs` or contact the development team.
