# FactScreen API

A comprehensive fact-checking API that combines multiple sources and uses AI for claim analysis and classification.

## Features

- **Multi-source claim extraction**: Integrates Google Fact Check API and RapidAPI Fact-Checker
- **Similarity filtering**: Uses sentence transformers to filter claims by relevance
- **AI-powered classification**: Employs transformer models for claim classification
- **Standardized response format**: Consistent data structure across all sources
- **Production-ready**: Comprehensive testing, documentation, and deployment tools

## Quick Start

### Option 1: Run Full Application (Frontend + Backend) - Recommended
```bash
# Setup development environment (first time only)
make install

# Start both backend and frontend together
make run-app
```

This will:
- Start the backend API server on http://localhost:8000
- Start the Streamlit frontend on http://localhost:8501
- Automatically handle port conflicts
- Wait for backend to be ready before starting frontend

**Access the application:**
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Swagger API Docs**: http://localhost:8000/docs (Interactive API documentation)
- **ReDoc**: http://localhost:8000/redoc (Alternative API documentation)
- **OpenAPI Schema**: http://localhost:8000/openapi.json (Raw OpenAPI specification)

### Option 2: Run Backend Only
```bash
# Setup development environment
make dev

# Start the backend server only
make run-server

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Option 3: Run Frontend Only (requires backend running)
```bash
# Start the frontend (backend must be running separately)
make run-frontend

# Frontend will be available at: http://localhost:8501
```

### Option 4: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements-dev.txt

# 2. Start the backend server
python entrypoint/server.py

# 3. In another terminal, start the frontend
streamlit run src/app/streamlit/main.py

# 4. Test the API
make test
```

## API Documentation

FactScreen provides comprehensive API documentation through Swagger UI and ReDoc:

### Swagger UI (Interactive)
- **URL**: http://localhost:8000/docs
- **Features**: 
  - Interactive API testing interface
  - Try out endpoints directly from the browser
  - View request/response schemas
  - See example requests and responses
  - Test authentication (if configured)

### ReDoc (Alternative Documentation)
- **URL**: http://localhost:8000/redoc
- **Features**:
  - Clean, readable documentation format
  - Better for printing and sharing
  - Three-column layout with navigation

### OpenAPI Schema (Raw JSON)
- **URL**: http://localhost:8000/openapi.json
- **Use cases**:
  - Import into API clients (Postman, Insomnia, etc.)
  - Generate client SDKs
  - API contract validation
  - Integration with API gateways

**Note**: All documentation is automatically generated from your API code and updates in real-time as you develop.

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

# Running the Application
make run-app          # Start both backend and frontend together (recommended)
make run-server       # Start backend server only
make run-frontend     # Start frontend only (requires backend running)
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

A lightweight Streamlit presentation layer lives in `src/app/streamlit/` that provides a user-friendly interface for fact-checking.

### Running the Frontend

**Recommended**: Use `make run-app` to start both backend and frontend together.

**Alternative**: Run frontend separately (requires backend to be running):

```bash
# Option 1: Using make command
make run-frontend

# Option 2: Direct streamlit command
FACTSCREEN_API_URL=http://localhost:8000 streamlit run src/app/streamlit/main.py
```

**Frontend URL**: http://localhost:8501 (or alternative port if 8501 is in use)

### Frontend Features

- Interactive claim validation interface
- URL and text input support
- Real-time fact-checking results
- PDF report generation
- Visual verdict display with confidence scores
- Source citations and explanations

**Note**: Environment variables (loaded from `.env`) must include the API keys.  
`FACTSCREEN_API_URL` defaults to `http://localhost:8000` but can be overridden when the backend runs elsewhere.

## Running the Application

### Full Stack (Frontend + Backend)
```bash
# Start both frontend and backend together
make run-app
```

This is the recommended way to run the application. It will:
1. Check and free ports 8000 (backend) and 8501 (frontend)
2. Start the backend API server
3. Wait for backend to be fully ready (health check)
4. Start the Streamlit frontend
5. Display all access URLs

**Access Points:**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

### Backend Only
```bash
make dev
make run-server
```

### Frontend Only (requires backend running)
```bash
make run-frontend
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