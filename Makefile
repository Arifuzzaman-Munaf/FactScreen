# FactScreen API Makefile

.PHONY: help install clean _clean test test-unit test-integration test-all run-server stop-server lint format check-deps dev run-frontend run-app

FACTSCREEN_API_URL ?= http://localhost:8000

# Frontend commands
run-frontend:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Starting Streamlit frontend..."
	@echo "Backend URL: $(FACTSCREEN_API_URL)"
	@FACTSCREEN_API_URL=$(FACTSCREEN_API_URL) ./venv/bin/streamlit run streamlit_app.py

run-app:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Starting backend and frontend together..."
	@FACTSCREEN_API_URL=$(FACTSCREEN_API_URL) ./venv/bin/python entrypoint/server.py &
	@BACKEND_PID=$$!; \
		sleep 3; \
		echo "Backend started with PID $$BACKEND_PID"; \
		echo "Launching Streamlit frontend..."; \
		FACTSCREEN_API_URL=$(FACTSCREEN_API_URL) ./venv/bin/streamlit run streamlit_app.py || EXIT_CODE=$$?; \
		echo "Shutting down backend..."; \
		kill $$BACKEND_PID >/dev/null 2>&1 || true; \
		exit $${EXIT_CODE:-0}
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
	@echo "Upgrading pip, setuptools, and wheel..."
	@PIP_PROGRESS_BAR=on ./venv/bin/pip install --upgrade pip setuptools wheel
	@echo "Installing dependencies (progress shown below)..."
	@PIP_PROGRESS_BAR=on ./venv/bin/pip install -r requirements-dev.txt
	@echo "✅ Virtual environment created and dependencies installed!"
	@$(MAKE) _clean

check-deps:
	@echo "Checking dependencies..."
	@./venv/bin/python -c "import fastapi, uvicorn, transformers, sentence_transformers; print('✅ All dependencies installed')"
	@$(MAKE) _clean

# Development commands
run-server:
	@$(MAKE) _clean
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Creating it now..."; \
		python3 -m venv venv; \
		echo "Installing dependencies (progress shown below)..."; \
		PIP_PROGRESS_BAR=on ./venv/bin/pip install --upgrade pip setuptools wheel; \
		PIP_PROGRESS_BAR=on ./venv/bin/pip install -r requirements-dev.txt; \
		echo "✅ Virtual environment created and dependencies installed!"; \
	elif ! ./venv/bin/python -c "import uvicorn" 2>/dev/null; then \
		echo "Dependencies not installed. Installing now (progress shown below)..."; \
		PIP_PROGRESS_BAR=on ./venv/bin/pip install --upgrade pip setuptools wheel; \
		PIP_PROGRESS_BAR=on ./venv/bin/pip install -r requirements-dev.txt; \
		echo "✅ Dependencies installed!"; \
	fi
	@./venv/bin/python entrypoint/server.py

stop-server:
	@echo "Stopping server..."
	@pkill -f "uvicorn src.app.main:app" || echo "No server process found"
	@$(MAKE) _clean

# Internal cleanup function (used by other commands)
_clean:
	@find . -type d -name "__pycache__" -not -path "./venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -not -path "./venv/*" -delete 2>/dev/null || true
	@find . -name "*.pyo" -not -path "./venv/*" -delete 2>/dev/null || true
	@find . -name ".pytest_cache" -not -path "./venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".mypy_cache" -not -path "./venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".coverage" -not -path "./venv/*" -delete 2>/dev/null || true
	@find . -name "htmlcov" -not -path "./venv/*" -exec rm -rf {} + 2>/dev/null || true

# Public clean command
clean:
	@echo "Cleaning cache files..."
	@$(MAKE) _clean
	@echo "✅ Cache files cleaned!"

# Testing commands
test:
	@if [ ! -d "venv" ] || ! ./venv/bin/python -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Running all tests..."
	@./venv/bin/python -m pytest tests/ -v
	@$(MAKE) _clean

test-unit:
	@if [ ! -d "venv" ] || ! ./venv/bin/python -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Running unit tests..."
	@./venv/bin/python -m pytest tests/test_services.py -v
	@$(MAKE) _clean

test-integration:
	@if [ ! -d "venv" ] || ! ./venv/bin/python -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Running integration tests..."
	@./venv/bin/python -m pytest tests/test_integration.py -v
	@$(MAKE) _clean

test-all:
	@if [ ! -d "venv" ] || ! ./venv/bin/python -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Running all tests with verbose output..."
	@./venv/bin/python -m pytest tests/ -v -s
	@$(MAKE) _clean

# Code quality commands
lint:
	@if [ ! -d "venv" ] || ! ./venv/bin/python -c "import flake8" 2>/dev/null; then \
		echo "Virtual environment or flake8 not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Running linting checks..."
	@./venv/bin/python -m flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503 --exclude=venv
	@$(MAKE) _clean

format:
	@if [ ! -d "venv" ] || ! ./venv/bin/python -c "import black" 2>/dev/null; then \
		echo "Virtual environment or black not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Formatting code with black..."
	@./venv/bin/python -m black src/ tests/ --line-length=100 --exclude=venv
	@$(MAKE) _clean

# Quick development workflow
dev: install
	@echo "Development environment ready!"
	@echo "Run 'make run-server' to start the server"
	@echo "Run 'make test' to run tests"
	@$(MAKE) _clean
