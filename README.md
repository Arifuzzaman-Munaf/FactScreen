# FactScreen API

A comprehensive fact-checking API that combines multiple sources and uses AI for claim analysis and classification.

## 🚀 Features

- **Multi-source claim extraction**: Integrates Google Fact Check API and RapidAPI Fact-Checker
- **Similarity filtering**: Uses sentence transformers to filter claims by relevance
- **AI-powered classification**: Employs transformer models for claim classification
- **Standardized response format**: Consistent data structure across all sources
- **Production-ready**: Comprehensive testing, documentation, and deployment tools

## ⚡ Quick Start

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

## 📡 API Endpoints

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

## 🏗️ Project Structure

```
FactScreen/
├── config/                      # Configuration files
│   └── local.yaml              # Local configuration
├── entrypoint/                 # Application entrypoints
│   └── server.py              # Server startup script
├── notebooks/                  # Jupyter notebooks (for future use)
├── src/                        # Main source code
│   ├── app/                    # Application code
│   │   ├── api/               # API routes
│   │   ├── core/              # Configuration
│   │   ├── models/            # Data models
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utility functions
│   ├── pipelines/             # ML pipelines
│   │   ├── feature_eng_pipeline.py    # Feature engineering
│   │   ├── inference_pipeline.py      # Inference/classification
│   │   └── validation_pipeline.py     # Validation pipeline
│   └── utils.py               # Utility functions
├── tests/                      # Test suite
├── Makefile                    # Development commands
├── requirements-dev.txt        # Development dependencies
└── README.md                   # This file
```

## 🛠️ Development Commands

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
make test-unit        # Run unit tests only
make test-integration # Run integration tests only
make test-all         # Run all tests with verbose output

# Code Quality
make lint             # Run linting checks
make format           # Format code with black
```

## 📚 Documentation

- [API Documentation](API_DOCUMENTATION.md) - Complete API reference
- [Project Structure](PROJECT_STRUCTURE.md) - Detailed project overview
- [Testing Guide](TESTING_GUIDE.md) - Testing documentation and examples

## 🔧 Configuration

Configuration is managed through `config/local.yaml` and environment variables.

Key configuration options:
- `GOOGLE_API_KEY`: Google Fact Check API key
- `FACT_CHECKER_API_KEY`: RapidAPI Fact-Checker key
- `SIMILARITY_THRESHOLD`: Default similarity threshold (0.75)
- `SENTENCE_TRANSFORMER_MODEL`: Model for similarity (all-MiniLM-L6-v2)
- `CLASSIFICATION_MODEL`: Model for classification (facebook/bart-large-mnli)

## 🧪 Testing

The project includes comprehensive testing:

- **Unit Tests**: Test individual services in isolation
- **Integration Tests**: Test API endpoints end-to-end
- **Legacy Tests**: Backward compatibility tests

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration

# Run with verbose output
make test-all
```

## 🚀 Running the Application

### Development
```bash
make dev
make run-server
```

## 📦 Installation

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [API Documentation](API_DOCUMENTATION.md)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/factscreen/factscreen-api/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/factscreen/factscreen-api/discussions)