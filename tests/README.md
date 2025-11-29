# FactScreen Test Suite

Comprehensive test suite for the FactScreen fact-checking application covering all APIs, services, pipelines, and integration scenarios.

## Test File Structure

The test suite is organized into a hierarchical directory structure:

### Directory Organization

```
tests/
├── conftest.py              # Shared pytest fixtures and configuration
├── README.md                # This file
├── unit/                    # Unit tests (isolated component testing)
│   ├── services/           # Service layer unit tests
│   │   ├── test_factcheck.py
│   │   ├── test_fetch.py
│   │   ├── test_sentiment.py
│   │   ├── test_report.py
│   │   ├── test_gemini.py
│   │   ├── test_claim_extract.py
│   │   └── test_classify.py
│   └── pipelines/          # Pipeline unit tests
│       ├── test_validation.py
│       ├── test_inference.py
│       └── test_feature_eng.py
└── integration/           # Integration tests (cross-component testing)
    ├── test_api_routes.py
    └── test_workflows.py
```

### Test File Descriptions

#### Unit Tests (`tests/unit/`)

**Services (`tests/unit/services/`):**
- **`test_factcheck.py`**: Fact-checking aggregation service tests (majority vote, confidence calculation, Gemini fallback)
- **`test_fetch.py`**: Data fetching service tests (Google FactCheck, RapidAPI, page text extraction)
- **`test_sentiment.py`**: Sentiment analysis service tests (label conversion, edge cases)
- **`test_report.py`**: PDF report generation service tests (all verdict types)
- **`test_gemini.py`**: Gemini AI service integration tests (classification, explanation, alignment)
- **`test_claim_extract.py`**: Claim extraction service tests (extraction and mapping from multiple sources)
- **`test_classify.py`**: Provider result classification service tests (normalization)

**Pipelines (`tests/unit/pipelines/`):**
- **`test_validation.py`**: Claim validation pipeline tests (text/URL validation, detailed analysis)
- **`test_inference.py`**: Claim classification inference pipeline tests (keyword matching, batch processing)
- **`test_feature_eng.py`**: Feature engineering and similarity filtering pipeline tests (cosine similarity)

#### Integration Tests (`tests/integration/`)

- **`test_api_routes.py`**: Comprehensive tests for all REST API endpoints
  - Health check, root endpoint
  - Text/URL validation, PDF generation
  - Claims search and filtering
- **`test_workflows.py`**: End-to-end integration workflow tests
  - Complete validation workflows
  - Multi-provider aggregation
  - Confidence calculation logic
  - Error handling and resilience

## Test Fixtures

Available in `conftest.py`:
- `mock_google_api_response`: Mock Google Fact Check API response
- `mock_rapidapi_response`: Mock RapidAPI response
- `sample_claims`: Sample claims data
- `api_base_url`: Base URL for API tests
- `mock_aggregated_result`: Mock AggregatedResult for testing
- `mock_provider_results`: Mock provider results list
- `mock_sources`: Mock sources for explanation generation
- `server_required`: Check if server is running
- `skip_if_no_server`: Skip tests if server unavailable

## Running Tests

### Run All Tests
```bash
pytest tests/
# or
make test
```

### Run by Category

**Unit Tests:**
```bash
# All unit tests
pytest tests/unit/

# All service tests
make test-services
# or
pytest tests/unit/services/

# All pipeline tests
make test-pipelines
# or
pytest tests/unit/pipelines/
```

**Integration Tests:**
```bash
# All integration tests
make test-integration
# or
pytest tests/integration/
```

**API Tests:**
```bash
make test-api
# or
pytest tests/integration/test_api_routes.py
```

### Run Specific Test File
```bash
# Unit tests
pytest tests/unit/services/test_factcheck.py
pytest tests/unit/services/test_fetch.py
pytest tests/unit/pipelines/test_validation.py

# Integration tests
pytest tests/integration/test_api_routes.py
pytest tests/integration/test_workflows.py
```

### Run with Coverage
```bash
make test-coverage
# or
pytest tests/ --cov=src --cov-report=html
```

### Generate Allure Report (Recommended)
```bash
make test-report
```

This generates a beautiful interactive HTML report with:
- Test execution timeline
- Test results with detailed steps
- Graphs and trends
- Screenshots and attachments support
- History tracking

### View Allure Report in Browser
```bash
make test-report-serve
```

This starts a local server and opens the report in your default browser.

### Run Specific Test Class
```bash
pytest tests/integration/test_api_routes.py::TestValidateEndpoint
pytest tests/unit/services/test_factcheck.py::TestFactcheckService
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Debug Mode
```bash
# Run with detailed output
pytest tests/ -v -s --tb=long

# Run specific failing test
pytest tests/integration/test_api_routes.py::TestValidateEndpoint::test_validate_with_text -v -s
```

## Test Coverage

### API Endpoints ✔
- `/v1/health` - Health check
- `/` - Root endpoint
- `/v1/validate` - Text/URL validation
- `/v1/validate/pdf` - PDF generation from validation
- `/v1/report/pdf` - PDF generation from result
- `/v1/claims/search` - Claims search
- `/v1/claims/filtered` - Filtered claims

### Services ✔
- `factcheck.py` - Aggregation, confidence, search
- `fetch.py` - Google/RapidAPI fetching, page text
- `sentiment.py` - Sentiment analysis, label conversion
- `report.py` - PDF generation
- `gemini_service.py` - Classification, explanation, alignment
- `claim_extract.py` - Claim extraction and mapping
- `classify.py` - Provider result classification

### Pipelines ✔
- `validation_pipeline.py` - Text/URL validation, detailed analysis
- `inference_pipeline.py` - Classification service
- `feature_eng_pipeline.py` - Similarity filtering

### Integration ✔
- End-to-end validation workflows
- Service integration scenarios
- Error handling and resilience
- Confidence calculation logic

## Test Requirements

- **Unit Tests**: No server required, all dependencies are mocked
- **Integration Tests**: Can run with or without server (uses mocking by default)
- **Dependencies**: Install test requirements with `pip install -r requirements-dev.txt`

## Test Design Principles

- **Mocking**: All tests use proper mocking to avoid external API calls
- **Independence**: Tests are designed to run independently
- **Isolation**: Each test is isolated and doesn't depend on others
- **Coverage**: Tests cover both success and failure scenarios
- **Organization**: Tests are organized by type (unit vs integration) and domain (services vs pipelines)

## Notes

- All tests use mocking to avoid external API calls
- Tests are designed to run independently
- Integration tests can optionally require a running server
- PDF tests verify structure, not exact content
- Gemini service tests handle missing API keys gracefully

## Adding New Tests

1. **Unit Tests**: Add to appropriate file in `tests/unit/services/` or `tests/unit/pipelines/`
2. **Integration Tests**: Add to appropriate file in `tests/integration/`
3. Follow existing naming conventions: `test_<functionality>`
4. Use proper mocking for external dependencies
5. Update this README with new test information

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running tests from the project root directory
2. **Missing Dependencies**: Install all requirements: `pip install -r requirements-dev.txt`
3. **Test Failures**: Run with verbose output: `pytest tests/ -v -s`
4. **Path Issues**: Use `make test-*` commands which handle paths correctly
