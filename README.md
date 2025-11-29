# FactScreen API

A comprehensive fact-checking API that combines multiple sources and uses AI for claim analysis and classification.

## Features

- **Multi-source claim extraction**: Integrates Google Fact Check API and RapidAPI Fact-Checker
- **Similarity filtering**: Uses sentence transformers to filter claims by relevance
- **AI-powered classification**: Employs transformer models for claim classification
- **Standardized response format**: Consistent data structure across all sources
- **Production-ready**: Comprehensive testing, documentation, and deployment tools

## Quick Start

### Option 1: Using Make (Recommended)
```bash
# Setup development environment
make dev

# Start the server
make run-server

# Run tests
make test
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements-dev.txt

# 2. Start the server
python entrypoint/server.py

# 3. Test the API
make test
```

### 4. Access Documentation
- **Interactive docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## API Endpoints

### Search Claims
```bash
curl -X POST "http://localhost:8000/v1/claims/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Climate change is a hoax", "page_size": 5}'
```

### Filtered Claims
```bash
curl -X POST "http://localhost:8000/v1/claims/filtered" \
  -H "Content-Type: application/json" \
  -d '{"query": "Climate change is a hoax", "similarity_threshold": 0.75}'
```

### Validate Claims (text / url)
```bash
curl -X POST "http://localhost:8000/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{
        "text": "The Eiffel Tower will be demolished next year"
      }'
```

### Generate PDF Report
```bash
curl -X POST "http://localhost:8000/v1/report/pdf" \
  -H "Content-Type: application/json" \
  -d '{
        "claim_text": "The Eiffel Tower will be demolished next year",
        "verdict": "misleading",
        "confidence": 0.91,
        "explanation": "..."
      }'
```

**Response (excerpt)**
```json
{
  "result": {
    "claim_text": "The Eiffel Tower will be demolished next year",
    "verdict": "misleading",
    "confidence": 0.91,
    "explanation": "Google Fact Check and RapidAPI sources explain that no such demolition is planned. Gemini confirmed the claim is false."
  }
}
```

The validation endpoint automatically combines third-party fact-checking providers and Gemini 2.5 Flash to generate:
- `verdict` — final label (true/misleading/unknown)
- `confidence` — confidence score
- `explanation` — natural-language reasoning citing sources or Gemini fallback

## Project Structure

```
FactScreen/
├── config/                     # Configuration files
│   ├── local.yaml             # Static configuration (URLs, models, thresholds)
├── entrypoint/                 # Application entrypoints
│   └── server.py              # Server startup script
├── src/                        # Main source code
│   ├── app/                    # Application code
│   │   ├── api/               # API routes
│   │   ├── core/              # Configuration and logging
│   │   ├── models/            # Data models and schemas
│   │   ├── services/          # Business logic services
│   │   │   ├── factcheck.py  # Result aggregation
│   │   │   ├── fetch.py      # Data fetching
│   │   │   ├── gemini_service.py  # Gemini AI integration
│   │   │   ├── classify.py   # Provider result classification
│   │   │   ├── sentiment.py  # Sentiment analysis
│   │   │   ├── report.py     # PDF report generation
│   │   │   └── claim_extract.py  # Claim extraction
│   │   └── streamlit/         # Streamlit frontend
│   │       ├── main.py        # Frontend entry point
│   │       ├── components/    # Page components
│   │       ├── helpers.py     # Helper functions
│   │       └── styles/        # CSS styling modules
│   ├── pipelines/             # ML pipelines
│   │   ├── feature_eng_pipeline.py    # Similarity filtering
│   │   ├── inference_pipeline.py      # Classification service
│   │   └── validation_pipeline.py     # Validation pipeline
│   └── utils.py               # Utility functions
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   │   ├── services/         # Service unit tests
│   │   └── pipelines/        # Pipeline unit tests
│   ├── integration/          # Integration tests
│   ├── conftest.py           # Shared fixtures
│   └── README_TEST.md        # Test documentation
├── Makefile                    # Development commands
├── requirements-dev.txt        # Development dependencies
└── README.md                   # This file
```

## Development Commands

```bash
# Setup
make install          # Install dependencies
make dev              # Setup development environment

# Development
make run-server       # Start development server
make stop-server      # Stop development server
make clean            # Clean cache files

# Testing
make test             # Run all tests
make test-api         # Run API route tests
make test-services    # Run core services tests
make test-pipelines   # Run data pipeline tests
make test-integration # Run integration workflow tests
make test-coverage    # Run tests with coverage report
make test-report      # Generate Allure test report
make test-all         # Run all tests with verbose output

# Code Quality
make lint             # Run linting checks
make format           # Format code with black
```

## Documentation

- [API Documentation](API_DOCUMENTATION.md) - Complete API reference
- [Project Structure](PROJECT_STRUCTURE.md) - Detailed project overview
- [Testing Guide](TESTING_GUIDE.md) - Testing documentation and examples

## Configuration

Configuration is managed through two sources:

### 1. Static Configuration (`config/local.yaml`)
All static settings (URLs, endpoints, model names, thresholds, etc.) are stored in `config/local.yaml`. This includes:
- API endpoints and URLs
- ML model identifiers
- Similarity thresholds
- Classification keywords
- Logging configuration
- Server host/port settings

### 2. Environment Variables (`.env`)
API keys and secrets are stored in `.env` file. Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your-google-factcheck-key
FACT_CHECKER_API_KEY=your-rapidapi-key
GEMINI_API_KEY=your-gemini-key
```

**Note**: Only API keys are stored in `.env`. All other configuration is in `config/local.yaml`.

### Key Configuration Files
- `config/local.yaml`: Static application settings
- `config/prompt.yaml`: LLM prompt templates
- `.env`: API keys and secrets (not committed to git)

Gemini usage and quota warnings are written to `logs/gemini.log`, including token counts and quota/invalid-key errors.

## Testing

The project includes comprehensive testing organized into unit and integration tests:

- **Unit Tests** (`tests/unit/`): Test individual services and pipelines in isolation
  - Service tests: factcheck, fetch, gemini, classify, sentiment, report, claim_extract
  - Pipeline tests: validation, inference, feature_eng
- **Integration Tests** (`tests/integration/`): Test API endpoints and end-to-end workflows

```bash
# Run all tests
make test

# Run specific test categories
make test-api         # API route tests
make test-services    # Service unit tests
make test-pipelines   # Pipeline unit tests
make test-integration # Integration workflow tests

# Generate test reports
make test-coverage    # Coverage report (HTML)
make test-report      # Allure test report

# Run with verbose output
make test-all
```

See [tests/README_TEST.md](tests/README_TEST.md) for detailed testing documentation.

## Streamlit Frontend

A lightweight Streamlit presentation layer lives in `src/app/streamlit/`.

### Run locally

```bash
# activate venv if not already done
make install

# Option 1: Using make command (recommended)
make run-frontend

# Option 2: Direct streamlit command
# The code automatically handles Python path, works on any device
FACTSCREEN_API_URL=http://localhost:8000 streamlit run src/app/streamlit/main.py
```

Environment variables (loaded from `.env`) must include the API keys noted above.  
`FACTSCREEN_API_URL` defaults to `http://localhost:8000` but can be overridden when the backend runs elsewhere.

## Running the Application

### Development
```bash
make dev
make run-server
```

## Installation

### From Source
```bash
git clone https://github.com/factscreen/factscreen-api.git
cd factscreen-api
make dev
```

### Using pip
```bash
pip install factscreen-api
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.