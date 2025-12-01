# FactScreen API

A comprehensive fact-checking API that combines multiple sources and uses AI for claim analysis and classification.

## Features

- **Multi-source claim extraction**: Integrates Google Fact Check API and RapidAPI Fact-Checker
- **Similarity filtering**: Uses sentence transformers to filter claims by relevance
- **AI-powered classification**: Employs transformer models for claim classification
- **Standardized response format**: Consistent data structure across all sources
- **Production-ready**: Comprehensive testing, documentation, and deployment tools

## Prerequisites

### For All Platforms
- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **API Keys** (create a `.env` file with your keys - see Configuration section below)

### For Windows
- Python installed with "Add Python to PATH" option checked
- Command Prompt or PowerShell
- (Optional) Git for Windows - [Download Git](https://git-scm.com/download/win)

### For macOS/Linux
- Python 3.10+ and pip
- Make utility (usually pre-installed)
- (Optional) Git

## Quick Start

### 🪟 Windows Users

**Simple Method - Using Python Launcher:**

1. **Run the launcher:**
   ```cmd
   python start.py
   ```

2. **Select option 1** to install dependencies (first time only)

**Access the application:**
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Swagger API Docs**: http://localhost:8000/docs (Interactive API documentation)
- **ReDoc**: http://localhost:8000/redoc (Alternative API documentation)
- **OpenAPI Schema**: http://localhost:8000/openapi.json (Raw OpenAPI specification)

3. **Select option 2** to run the full application (Backend + Frontend)

**Menu Options:**
- **Option 1**: Install/Setup (first time only)
- **Option 2**: Run Full Application (Backend + Frontend) - **Recommended**
- **Option 3**: Run Backend Only
- **Option 4**: Run Frontend Only (requires backend running)
- **Option 5**: Run Tests
- **Option 6**: Run Tests with Coverage
- **Option 7**: Run Tests with Allure Report
- **Option 8**: View Allure Report
- **Option 9**: Exit

**Manual Setup (Alternative):**
```cmd
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements-dev.txt

# 4. Run backend
python entrypoint\server.py

# 5. Run frontend (in new terminal)
venv\Scripts\activate
set STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
streamlit run src\app\streamlit\main.py --server.port 8501
```

### 🐧 macOS/Linux Users

**Recommended - Using Make:**

```bash
# 1. Setup development environment (first time only)
make install

# 2. Create .env file with your API keys (see Configuration section)

# 3. Start both backend and frontend together
make run-app
```

**Alternative - Manual Setup:**

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements-dev.txt

# 3. Start backend
python entrypoint/server.py

# 4. Start frontend (in new terminal)
source venv/bin/activate
streamlit run src/app/streamlit/main.py --server.port 8501
```

## Access the Application

Once running, access the application at:

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Swagger API Docs**: http://localhost:8000/docs (Interactive API documentation)
- **ReDoc**: http://localhost:8000/redoc (Alternative API documentation)
- **OpenAPI Schema**: http://localhost:8000/openapi.json (Raw OpenAPI specification)

## Configuration

### Environment Variables (`.env`)

Create a `.env` file in the project root with your API keys:

```
GOOGLE_API_KEY=your-google-factcheck-key
FACT_CHECKER_API_KEY=your-rapidapi-key
GEMINI_API_KEY=your-gemini-key
```

**Note**: Only API keys are stored in `.env`. All other configuration is in `config/local.yaml`.

### Configuration Files

- `config/local.yaml`: Static application settings (URLs, models, thresholds, etc.)
- `config/prompt.yaml`: LLM prompt templates
- `.env`: API keys and secrets (not committed to git)

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
  -d '{"text": "The Eiffel Tower will be demolished next year"}'
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

**Response Example:**
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

## API Documentation

FactScreen provides comprehensive API documentation:

### Swagger UI (Interactive)
- **URL**: http://localhost:8000/docs
- **Features**: 
  - Interactive API testing interface
  - Try out endpoints directly from the browser
  - View request/response schemas
  - See example requests and responses

### ReDoc (Alternative Documentation)
- **URL**: http://localhost:8000/redoc
- **Features**: Clean, readable documentation format, better for printing and sharing

### OpenAPI Schema (Raw JSON)
- **URL**: http://localhost:8000/openapi.json
- **Use cases**: Import into API clients (Postman, Insomnia, etc.), generate client SDKs

**Note**: All documentation is automatically generated from your API code and updates in real-time as you develop.

## Development Commands

### macOS/Linux (using Make)

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

### Windows

Use `start.py` launcher or run commands manually in activated virtual environment:

```cmd
# Option 1: Use launcher
python start.py

# Option 2: Run commands manually
# Activate virtual environment first
venv\Scripts\activate

# Running the Application
python entrypoint\server.py          # Start backend server
streamlit run src\app\streamlit\main.py  # Start frontend

# Testing
pytest tests\ -v                     # Run all tests
pytest tests\integration\test_api_routes.py -v  # Run API route tests
pytest tests\unit\services\ -v       # Run core services tests
pytest tests\unit\pipelines\ -v      # Run data pipeline tests
pytest tests\integration\ -v         # Run integration workflow tests
pytest tests\ --cov=src --cov-report=html --cov-report=term-missing  # Coverage report
pytest tests\ --alluredir=allure-results -v  # Generate Allure results (requires allure-pytest)
pytest tests\ -v -s                  # Run all tests with verbose output

# Code Quality
python -m black src\ tests\           # Format code
python -m flake8 src\ tests\          # Lint code
```

## Testing

The project includes comprehensive testing organized into unit and integration tests:

- **Unit Tests** (`tests/unit/`): Test individual services and pipelines in isolation
  - Service tests: factcheck, fetch, gemini, classify, sentiment, report, claim_extract
  - Pipeline tests: validation, inference, feature_eng
- **Integration Tests** (`tests/integration/`): Test API endpoints and end-to-end workflows

**Run Tests:**

**macOS/Linux:**
```bash
make test             # Run all tests
make test-api         # API route tests
make test-services    # Service unit tests
make test-pipelines   # Pipeline unit tests
make test-integration # Integration workflow tests
make test-coverage    # Coverage report (HTML)
```

**Windows:**
```cmd
# Activate virtual environment first
venv\Scripts\activate

# Run all tests
pytest tests\ -v

# Run specific test categories
pytest tests\integration\test_api_routes.py -v        # API route tests
pytest tests\unit\services\ -v                       # Service unit tests
pytest tests\unit\pipelines\ -v                      # Pipeline unit tests
pytest tests\integration\ -v                          # Integration workflow tests

# Run with coverage report
pytest tests\ --cov=src --cov-report=html --cov-report=term-missing
# Coverage report will be in htmlcov\index.html

# Generate Allure test report (requires allure-pytest installed)
pytest tests\ --alluredir=allure-results -v
# Then generate HTML report (requires Allure CLI installed)
allure generate allure-results -o allure-report --clean
allure open allure-report

# Run with verbose output
pytest tests\ -v -s
```

See [tests/README_TEST.md](tests/README_TEST.md) for detailed testing documentation.

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
│   ├── integration/          # Integration tests
│   ├── conftest.py           # Shared fixtures
│   └── README_TEST.md        # Test documentation
├── start.py                    # Windows launcher (Python-based, cross-platform)
├── Makefile                    # Development commands (macOS/Linux)
├── requirements-dev.txt        # Development dependencies
└── README.md                   # This file
```

## Streamlit Frontend

A lightweight Streamlit presentation layer provides a user-friendly interface for fact-checking.

### Frontend Features

- Interactive claim validation interface
- URL and text input support
- Real-time fact-checking results
- PDF report generation
- Visual verdict display with confidence scores
- Source citations and explanations

**Note**: Environment variables (loaded from `.env`) must include the API keys.  
`FACTSCREEN_API_URL` defaults to `http://localhost:8000` but can be overridden when the backend runs elsewhere.

## Troubleshooting

### Port Already in Use

**Windows:**
```cmd
# Find the process using the port
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual process ID)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Find the process using the port
lsof -ti:8000

# Kill the process
kill -9 $(lsof -ti:8000)
```

### Python Not Found (Windows)

- Make sure Python is installed
- Add Python to your PATH environment variable
- Restart Command Prompt after adding to PATH
- Try using `py` instead of `python` (Windows Python Launcher)

### Virtual Environment Issues

**Windows:**
- Make sure you have Python 3.8+ installed
- Try: `py -m venv venv` instead of `python -m venv venv`
- Make sure you have write permissions in the project directory

**macOS/Linux:**
- Ensure Python 3.8+ is installed: `python3 --version`
- Use `python3` instead of `python` if needed

### Dependencies Installation Fails

**All Platforms:**
- Update pip: `python -m pip install --upgrade pip` (or `python3 -m pip install --upgrade pip`)
- Make sure you have internet connection
- Try installing without cache: `pip install --no-cache-dir -r requirements-dev.txt`

### Module Not Found Errors

**Windows:**
```cmd
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements-dev.txt
```

**macOS/Linux:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements-dev.txt
```

### PowerShell Execution Policy (Windows)

If you get an execution policy error in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Backend Not Starting

- Check if port 8000 is available
- Verify `.env` file exists with valid API keys
- Check logs for error messages
- Ensure all dependencies are installed

### Frontend Not Connecting to Backend

- Verify backend is running on http://localhost:8000
- Check `FACTSCREEN_API_URL` environment variable if set
- Ensure backend health endpoint is accessible: http://localhost:8000/v1/health

## Additional Resources

- API documentation available at http://localhost:8000/docs when server is running
- Check `config/local.yaml` for configuration options
- See [tests/README_TEST.md](tests/README_TEST.md) for testing documentation
- Gemini usage and quota warnings are written to `logs/gemini.log`

## Installation

### From Source

**macOS/Linux:**
```bash
git clone https://github.com/factscreen/factscreen-api.git
cd factscreen-api
make dev
```

**Windows:**
```cmd
git clone https://github.com/factscreen/factscreen-api.git
cd factscreen-api
python start.py
# Select option 1 to install
```

### Using pip
```bash
pip install factscreen-api
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test` (macOS/Linux) or `pytest tests\ -v` (Windows)
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.