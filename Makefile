# FactScreen API Makefile

.PHONY: help install clean test test-unit test-integration test-all run-server stop-server lint format check-deps dev

# Default target
help:
	@echo "FactScreen API - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  install        Install all dependencies"
	@echo "  check-deps     Check if all dependencies are installed"
	@echo ""
	@echo "Development:"
	@echo "  run-server     Start the development server"
	@echo "  stop-server    Stop the development server"
	@echo "  clean          Clean cache files and temporary files"
	@echo ""
	@echo "Testing:"
	@echo "  test           Run all tests"
	@echo "  test-unit      Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-all       Run all tests with verbose output"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code with black"
	@echo ""
	@echo "Quick Start:"
	@echo "  dev            Setup development environment"
	@echo ""

# Setup commands
install:
	@echo "Creating virtual environment..."
	@python3 -m venv venv
	@echo "Installing dependencies..."
	@./venv/bin/pip install -r requirements.txt

check-deps:
	@echo "Checking dependencies..."
	@./venv/bin/python -c "import fastapi, uvicorn, transformers, sentence_transformers; print('✅ All dependencies installed')"

# Development commands
run-server:
	@echo "Starting FactScreen API server..."
	@echo "Server will be available at: http://localhost:8000"
	@echo "API documentation: http://localhost:8000/docs"
	@echo "Press Ctrl+C to stop the server"
	@cd factscreen_backend && ../venv/bin/python utils/start_server.py

stop-server:
	@echo "Stopping server..."
	@pkill -f "uvicorn app.main:app" || echo "No server process found"

clean:
	@echo "Cleaning cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Cache files cleaned!"

# Testing commands
test:
	@echo "Running all tests..."
	@cd factscreen_backend && ../venv/bin/python -m pytest tests/ -v

test-unit:
	@echo "Running unit tests..."
	@cd factscreen_backend && ../venv/bin/python -m pytest tests/test_services.py -v

test-integration:
	@echo "Running integration tests..."
	@cd factscreen_backend && ../venv/bin/python -m pytest tests/test_integration.py -v

test-all:
	@echo "Running all tests with verbose output..."
	@cd factscreen_backend && ../venv/bin/python -m pytest tests/ -v -s

# Code quality commands
lint:
	@echo "Running linting checks..."
	@cd factscreen_backend && ../venv/bin/python -m flake8 app/ tests/ --max-line-length=100 --ignore=E203,W503

format:
	@echo "Formatting code with black..."
	@cd factscreen_backend && ../venv/bin/python -m black app/ tests/ --line-length=100

# Quick development workflow
dev: install
	@echo "Development environment ready!"
	@echo "Run 'make run-server' to start the server"
	@echo "Run 'make test' to run tests"
