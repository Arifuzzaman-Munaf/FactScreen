# FactScreen Project Structure

## Overview
FactScreen is a comprehensive fact-checking API that combines multiple sources and uses AI for claim analysis and classification.

## Project Structure

```
FactScreen/
├── factscreen_backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py              # API endpoints
│   │   ├── core/
│   │   │   └── config.py              # Configuration and settings
│   │   ├── models/
│   │   │   └── claim_models.py        # Pydantic models for API
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── claim_extract.py       # Claim extraction from APIs
│   │   │   ├── similarity_filter.py   # Similarity filtering service
│   │   │   └── claim_classifier.py    # AI classification service
│   │   ├── utils/
│   │   └── tests/
│   ├── pyproject.toml
│   └── setup.py
├── requirements.txt                   # Python dependencies
├── start_server.py                   # Server startup script
├── test_api.py                       # API testing script
├── API_DOCUMENTATION.md              # API documentation
├── PROJECT_STRUCTURE.md              # This file
└── README.md
```

## Key Components

### 1. API Endpoints (`app/api/routes.py`)
- **`/v1/claims/search`**: Fetch raw claims from multiple sources
- **`/v1/claims/filtered`**: Fetch, filter, and classify claims
- **`/v1/health`**: Health check endpoint

### 2. Services

#### Claim Extraction Service (`app/services/claim_extract.py`)
- Integrates with Google Fact Check API
- Integrates with RapidAPI Fact-Checker
- Standardizes response format across sources

#### Similarity Filter Service (`app/services/similarity_filter.py`)
- Uses sentence transformers for semantic similarity
- Filters claims based on similarity threshold
- Supports batch processing

#### Classification Service (`app/services/claim_classifier.py`)
- Uses transformer models for claim classification
- Implements keyword-based fast classification
- Provides three classification labels: True, False/Misleading, Not enough info

### 3. Models (`app/models/claim_models.py`)
- **ClaimRequest**: Input validation for search requests
- **ClaimResponse**: Standardized claim format
- **ClaimsListResponse**: Response for raw claims
- **FilteredClaimsResponse**: Response for filtered and classified claims

### 4. Configuration (`app/core/config.py`)
- API keys and endpoints configuration
- ML model settings
- Application settings

## API Workflow

### Raw Claims Endpoint (`/v1/claims/search`)
1. Receive search query
2. Fetch claims from Google Fact Check API
3. Fetch claims from RapidAPI Fact-Checker
4. Standardize and combine results
5. Return unified response

### Filtered Claims Endpoint (`/v1/claims/filtered`)
1. Receive search query and similarity threshold
2. Fetch claims from all sources (same as above)
3. Filter claims by similarity using sentence transformers
4. Classify filtered claims using transformer model
5. Return filtered and classified results

## Dependencies

### Core Dependencies
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### ML/AI Dependencies
- **transformers**: Hugging Face transformers
- **sentence-transformers**: Semantic similarity
- **torch**: PyTorch for ML models
- **scikit-learn**: Machine learning utilities
- **numpy**: Numerical computing
- **pandas**: Data manipulation

### HTTP Dependencies
- **requests**: HTTP client
- **httpx**: Async HTTP client

## Usage

### Starting the Server
```bash
# Option 1: Use the startup script
python start_server.py

# Option 2: Manual start
cd factscreen_backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API
```bash
python test_api.py
```

### API Documentation
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

Optional environment variables (defaults are provided in config.py):
- `GOOGLE_API_KEY`: Google Fact Check API key
- `FACT_CHECKER_API_KEY`: RapidAPI Fact-Checker key
- `SIMILARITY_THRESHOLD`: Default similarity threshold (0.75)
- `SENTENCE_TRANSFORMER_MODEL`: Model name for similarity
- `CLASSIFICATION_MODEL`: Model name for classification

## Features

### Multi-Source Integration
- Google Fact Check API
- RapidAPI Fact-Checker
- Extensible architecture for additional sources

### AI-Powered Analysis
- Semantic similarity filtering
- Automated claim classification
- Keyword-based fast classification

### Production Ready
- Comprehensive error handling
- Input validation
- API documentation
- Health checks
- CORS support

## Future Enhancements

1. **Additional Sources**: Integrate more fact-checking APIs
2. **Caching**: Implement Redis caching for improved performance
3. **Database**: Add persistent storage for claims
4. **Authentication**: Add API key authentication
5. **Rate Limiting**: Implement rate limiting
6. **Monitoring**: Add logging and monitoring
7. **Batch Processing**: Support for batch claim processing
8. **Custom Models**: Allow custom similarity and classification models
