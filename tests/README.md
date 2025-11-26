# FactScreen API Tests

This directory contains comprehensive tests for the FactScreen API.

## Test Structure

### Test Files

- **`test_integration.py`** - Integration tests for API endpoints
- **`test_services.py`** - Unit tests for service classes
- **`test_api.py`** - Legacy test script (backward compatibility)
- **`conftest.py`** - Pytest configuration and fixtures

### Test Categories

#### Integration Tests (`test_integration.py`)
- **TestAPIHealth**: Health endpoint tests
- **TestClaimsSearch**: Claims search endpoint tests
- **TestFilteredClaims**: Filtered claims endpoint tests
- **TestAPIErrorHandling**: Error handling tests

#### Unit Tests (`test_services.py`)
- **TestClaimExtractionService**: Claim extraction service tests
- **TestSimilarityFilterService**: Similarity filtering service tests
- **TestClaimClassificationService**: Classification service tests

## Running Tests

### Using the Test Runner (Recommended)

```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --type unit
python run_tests.py --type integration
python run_tests.py --type manual
python run_tests.py --type legacy

# Verbose output
python run_tests.py --verbose

# Skip pytest, run manual tests only
python run_tests.py --no-pytest
```

### Using Pytest Directly

```bash
cd factscreen_backend

# Run all tests
pytest

# Run specific test files
pytest tests/test_integration.py
pytest tests/test_services.py

# Run with verbose output
pytest -v

# Run specific test classes
pytest tests/test_services.py::TestClaimClassificationService

# Run specific test methods
pytest tests/test_services.py::TestClaimClassificationService::test_fast_keyword_classification_true
```

### Manual Test Execution

```bash
cd factscreen_backend

# Run integration tests manually
python tests/test_integration.py

# Run unit tests manually
python tests/test_services.py

# Run legacy test script
python tests/test_api.py
```

## Test Requirements

### For Integration Tests
- API server must be running on `http://localhost:8000`
- Server can be started with: `python start_server.py`

### For Unit Tests
- No server required
- Tests use mocked data and services

## Test Data

### Fixtures
- **`mock_google_api_response`**: Mock Google Fact Check API response
- **`mock_rapidapi_response`**: Mock RapidAPI Fact-Checker response
- **`sample_claims`**: Sample claims data for testing
- **`api_base_url`**: Base URL for API testing

### Test Cases

#### Integration Test Cases
- Health endpoint functionality
- Claims search with various queries
- Filtered claims with different similarity thresholds
- Error handling for invalid requests
- Response format validation

#### Unit Test Cases
- Service initialization
- Data mapping and transformation
- Similarity calculation
- Keyword-based classification
- Original rating classification
- Batch processing

## Test Configuration

### Pytest Configuration (`pytest.ini`)
- Test discovery patterns
- Output formatting
- Warning filters
- Custom markers

### Test Markers
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.slow`: Slow-running tests

## Continuous Integration

Tests are designed to be run in CI/CD pipelines:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python run_tests.py --type all
```

## Troubleshooting

### Common Issues

1. **Server not running**: Integration tests require the API server to be running
2. **Import errors**: Make sure you're running tests from the correct directory
3. **Network timeouts**: Check API endpoints and network connectivity

### Debug Mode

```bash
# Run with debug output
pytest -v -s --tb=long

# Run specific failing test
pytest tests/test_services.py::TestClaimClassificationService::test_classify_from_original_rating -v -s
```

## Adding New Tests

### For New API Endpoints
1. Add test methods to `TestAPIHealth`, `TestClaimsSearch`, or `TestFilteredClaims`
2. Follow the naming convention: `test_<functionality>`
3. Use appropriate assertions and error handling

### For New Services
1. Create new test class in `test_services.py`
2. Follow the naming convention: `Test<ServiceName>`
3. Test initialization, main methods, and edge cases

### For New Features
1. Add integration tests for API endpoints
2. Add unit tests for service methods
3. Update fixtures if new test data is needed
4. Update documentation

## Test Coverage

Current test coverage includes:
- ✅ API endpoint functionality
- ✅ Service initialization and configuration
- ✅ Data mapping and transformation
- ✅ Similarity filtering
- ✅ Claim classification
- ✅ Error handling
- ✅ Response validation

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Mock External Dependencies**: Use mocks for API calls and external services
3. **Clear Test Names**: Use descriptive test method names
4. **Assertion Clarity**: Use specific assertions with clear error messages
5. **Test Data**: Use fixtures for consistent test data
6. **Error Testing**: Test both success and failure scenarios
