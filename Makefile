# FactScreen API Makefile
# OS-agnostic Makefile for cross-platform compatibility

.PHONY: help install clean _clean test test-api test-services test-pipelines test-integration test-coverage test-all test-report test-report-serve run-server stop-server lint format check-deps dev run-frontend run-app

FACTSCREEN_API_URL ?= http://localhost:8000

# Detect Python executable (OS-agnostic)
PYTHON := $(shell if [ -f "venv/bin/python" ]; then echo "venv/bin/python"; elif [ -f "venv/Scripts/python.exe" ]; then echo "venv/Scripts/python.exe"; else echo "python3"; fi)
PIP := $(shell if [ -f "venv/bin/pip" ]; then echo "venv/bin/pip"; elif [ -f "venv/Scripts/pip.exe" ]; then echo "venv/Scripts/pip.exe"; else echo "pip3"; fi)

# Frontend commands
run-frontend:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Starting Streamlit frontend..."
	@STREAMLIT_SERVER_FILE_WATCHER_TYPE=none $(PYTHON) -m streamlit run src/app/streamlit/main.py --server.port 8501

run-app:
	@$(MAKE) _clean
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Creating it now..."; \
		python3 -m venv venv || python -m venv venv; \
		echo "Installing dependencies..."; \
		$(PIP) install --upgrade pip setuptools wheel; \
		$(PIP) install -r requirements-dev.txt; \
		echo "✔ Virtual environment created and dependencies installed!"; \
	elif ! $(PYTHON) -c "import uvicorn, streamlit" 2>/dev/null; then \
		echo "Dependencies not installed. Installing now..."; \
		$(PIP) install --upgrade pip setuptools wheel; \
		$(PIP) install -r requirements-dev.txt; \
		echo "✔ Dependencies installed!"; \
	fi
	@echo "Starting FactScreen application (backend + frontend)..."
	@STREAMLIT_SERVER_FILE_WATCHER_TYPE=none $(PYTHON) -m streamlit run src/app/streamlit/main.py --server.port 8501 &
	@sleep 2
	@echo "Backend will start automatically when frontend makes first request"
	@echo "Frontend available at: http://localhost:8501"
	@wait || $(MAKE) _clean

# Setup commands
install:
	@echo "Creating virtual environment..."
	@python3 -m venv venv || python -m venv venv
	@echo "Upgrading pip, setuptools, and wheel..."
	@$(PIP) install --upgrade pip setuptools wheel
	@echo "Installing all dependencies (including test dependencies)..."
	@$(PIP) install -r requirements-dev.txt
	@echo "✔ Virtual environment created and all dependencies installed!"
	@$(MAKE) _clean

check-deps:
	@echo "Checking dependencies..."
	@$(PYTHON) -c "import fastapi, uvicorn, transformers, sentence_transformers, pytest, allure; print('✔ All dependencies installed')" || (echo "❌ Some dependencies missing. Run 'make install'"; exit 1)
	@$(MAKE) _clean

# Development commands
run-server:
	@$(MAKE) _clean
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Creating it now..."; \
		python3 -m venv venv || python -m venv venv; \
		echo "Installing dependencies..."; \
		$(PIP) install --upgrade pip setuptools wheel; \
		$(PIP) install -r requirements-dev.txt; \
		echo "✔ Virtual environment created and dependencies installed!"; \
	elif ! $(PYTHON) -c "import uvicorn" 2>/dev/null; then \
		echo "Dependencies not installed. Installing now..."; \
		$(PIP) install --upgrade pip setuptools wheel; \
		$(PIP) install -r requirements-dev.txt; \
		echo "✔ Dependencies installed!"; \
	fi
	@$(PYTHON) entrypoint/server.py

stop-server:
	@echo "Stopping server..."
	@pkill -f "uvicorn src.app.main:app" 2>/dev/null || taskkill //F //IM python.exe //T 2>/dev/null || echo "No server process found"
	@$(MAKE) _clean

# Internal cleanup function (OS-agnostic)
_clean:
	@$(PYTHON) -c "import os, shutil, glob; \
		exclude = {'venv', '.git'}; \
		paths = []; \
		paths.extend([d for d in glob.glob('**/__pycache__', recursive=True) if not any(ex in d for ex in exclude)]); \
		paths.extend([f for f in glob.glob('**/*.pyc', recursive=True) if not any(ex in f for ex in exclude)]); \
		paths.extend([f for f in glob.glob('**/*.pyo', recursive=True) if not any(ex in f for ex in exclude)]); \
		paths.extend([d for d in glob.glob('**/.pytest_cache', recursive=True) if not any(ex in d for ex in exclude)]); \
		paths.extend([d for d in glob.glob('**/.mypy_cache', recursive=True) if not any(ex in d for ex in exclude)]); \
		paths.extend([f for f in glob.glob('**/.coverage', recursive=True) if not any(ex in f for ex in exclude)]); \
		paths.extend([d for d in glob.glob('**/htmlcov', recursive=True) if not any(ex in d for ex in exclude)]); \
		paths.extend([d for d in glob.glob('**/allure-results', recursive=True) if not any(ex in d for ex in exclude)]); \
		[shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p) for p in paths if os.path.exists(p)]; \
	" 2>/dev/null || true

# Public clean command
clean:
	@echo "Cleaning cache files..."
	@$(MAKE) _clean
	@echo "✔ Cache files cleaned!"

# Testing commands
test:
	@$(MAKE) _clean
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		$(MAKE) _clean; \
		exit 1; \
	fi
	@echo "Running all tests..."
	@$(PYTHON) -m pytest tests/ -v; EXIT_CODE=$$?; \
	$(MAKE) _clean; \
	exit $$EXIT_CODE

test-api:
	@$(MAKE) _clean
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		$(MAKE) _clean; \
		exit 1; \
	fi
	@echo "Running API route tests..."
	@$(PYTHON) -m pytest tests/integration/test_api_routes.py -v; EXIT_CODE=$$?; \
	$(MAKE) _clean; \
	exit $$EXIT_CODE

test-services:
	@$(MAKE) _clean
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		$(MAKE) _clean; \
		exit 1; \
	fi
	@echo "Running core services tests..."
	@$(PYTHON) -m pytest tests/unit/services/ -v; EXIT_CODE=$$?; \
	$(MAKE) _clean; \
	exit $$EXIT_CODE

test-pipelines:
	@$(MAKE) _clean
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		$(MAKE) _clean; \
		exit 1; \
	fi
	@echo "Running data pipeline tests..."
	@$(PYTHON) -m pytest tests/unit/pipelines/ -v; EXIT_CODE=$$?; \
	$(MAKE) _clean; \
	exit $$EXIT_CODE

test-integration:
	@$(MAKE) _clean
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		$(MAKE) _clean; \
		exit 1; \
	fi
	@echo "Running integration workflow tests..."
	@$(PYTHON) -m pytest tests/integration/ -v; EXIT_CODE=$$?; \
	$(MAKE) _clean; \
	exit $$EXIT_CODE

test-coverage:
	@$(MAKE) _clean
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		$(MAKE) _clean; \
		exit 1; \
	fi
	@if ! $(PYTHON) -c "import pytest_cov" 2>/dev/null; then \
		echo "pytest-cov not found. Installing..."; \
		$(PIP) install pytest-cov; \
	fi
	@echo "Running tests with coverage analysis..."
	@$(PYTHON) -m pytest tests/ \
		--cov=src \
		--cov-report=html \
		--cov-report=term-missing \
		--cov-branch \
		-v; \
	EXIT_CODE=$$?; \
	echo ""; \
	echo "Coverage report: htmlcov/index.html"; \
	$(MAKE) _clean; \
	exit $$EXIT_CODE

test-all:
	@$(MAKE) _clean
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		$(MAKE) _clean; \
		exit 1; \
	fi
	@echo "Running all tests with verbose output..."
	@$(PYTHON) -m pytest tests/ -v -s; EXIT_CODE=$$?; \
	$(MAKE) _clean; \
	exit $$EXIT_CODE

test-report:
	@$(MAKE) _clean
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import pytest" 2>/dev/null; then \
		echo "Virtual environment or pytest not found. Run 'make install' first."; \
		$(MAKE) _clean; \
		exit 1; \
	fi
	@if ! $(PYTHON) -c "import allure" 2>/dev/null; then \
		echo "Installing allure-pytest..."; \
		$(PIP) install allure-pytest; \
	fi
	@echo "Checking for Allure CLI..."
	@if ! command -v allure >/dev/null 2>&1; then \
		echo "Allure CLI not found. Attempting to install..."; \
		if command -v brew >/dev/null 2>&1; then \
			echo "Installing Allure CLI via Homebrew..."; \
			brew install allure || echo "Failed to install via Homebrew. Please install manually: brew install allure"; \
		elif command -v npm >/dev/null 2>&1; then \
			echo "Installing Allure CLI via npm..."; \
			npm install -g allure-commandline || echo "Failed to install via npm. Please install manually: npm install -g allure-commandline"; \
		else \
			echo ""; \
			echo "⚠️  Allure CLI not found and no package manager available."; \
			echo "Please install Allure CLI manually:"; \
			echo "  macOS: brew install allure"; \
			echo "  Linux: See https://docs.qameta.io/allure/"; \
			echo "  Or use: npm install -g allure-commandline"; \
			echo ""; \
			echo "Continuing with test execution (results will be saved but HTML report won't be generated)..."; \
		fi; \
	fi
	@echo "Running tests with Allure reporting..."
	@echo "Note: Existing Allure reports will be replaced with new ones"
	@mkdir -p allure-results
	@$(PYTHON) -m pytest tests/ \
		--alluredir=allure-results \
		-v \
		--tb=short; \
	EXIT_CODE=$$?; \
	if command -v allure >/dev/null 2>&1; then \
		echo ""; \
		echo "Generating Allure HTML report (replacing old report)..."; \
		allure generate allure-results -o allure-report --clean; \
		echo ""; \
		echo "✔ Allure report generated in: allure-report/index.html"; \
		echo "Run 'make test-report-serve' to view it in browser"; \
	else \
		echo ""; \
		echo "⚠️  Allure CLI not available. Test results saved to: allure-results/"; \
		echo "Install Allure CLI to generate HTML report:"; \
		echo "  macOS: brew install allure"; \
		echo "  Linux: See https://docs.qameta.io/allure/"; \
		echo "  Or use: npm install -g allure-commandline"; \
	fi; \
	$(MAKE) _clean; \
	exit $$EXIT_CODE

test-report-serve:
	@if [ ! -d "allure-results" ] && [ ! -d "allure-report" ]; then \
		echo "Allure results not found. Run 'make test-report' first."; \
		exit 1; \
	fi
	@if ! command -v allure >/dev/null 2>&1; then \
		echo "Allure CLI not found. Attempting to install..."; \
		if command -v brew >/dev/null 2>&1; then \
			echo "Installing Allure CLI via Homebrew..."; \
			brew install allure || (echo "Failed to install via Homebrew. Please install manually: brew install allure"; exit 1); \
		elif command -v npm >/dev/null 2>&1; then \
			echo "Installing Allure CLI via npm..."; \
			npm install -g allure-commandline || (echo "Failed to install via npm. Please install manually: npm install -g allure-commandline"; exit 1); \
		else \
			echo "⚠️  Allure CLI not found and no package manager available."; \
			echo "Please install Allure CLI manually:"; \
			echo "  macOS: brew install allure"; \
			echo "  Linux: See https://docs.qameta.io/allure/"; \
			echo "  Or use: npm install -g allure-commandline"; \
			if [ -d "allure-report" ]; then \
				echo ""; \
				echo "Opening static report instead..."; \
				if command -v open >/dev/null 2>&1; then \
					open allure-report/index.html; \
				elif command -v xdg-open >/dev/null 2>&1; then \
					xdg-open allure-report/index.html; \
				else \
					echo "Please open allure-report/index.html manually"; \
				fi; \
			fi; \
			exit 1; \
		fi; \
	fi
	@if [ -d "allure-results" ]; then \
		echo "Starting Allure report server..."; \
		echo "Report will be available at: http://localhost:8080"; \
		echo "Press Ctrl+C to stop the server"; \
		allure serve allure-results || echo "Failed to start Allure server"; \
	elif [ -d "allure-report" ]; then \
		echo "Opening Allure report..."; \
		if command -v allure >/dev/null 2>&1; then \
			allure open allure-report || ( \
				echo "Failed to open with 'allure open', trying fallback..."; \
				if command -v open >/dev/null 2>&1; then \
					open allure-report/index.html; \
				elif command -v xdg-open >/dev/null 2>&1; then \
					xdg-open allure-report/index.html; \
				else \
					echo "Please open allure-report/index.html manually"; \
				fi \
			); \
		elif command -v open >/dev/null 2>&1; then \
			open allure-report/index.html; \
		elif command -v xdg-open >/dev/null 2>&1; then \
			xdg-open allure-report/index.html; \
		else \
			echo "Please open allure-report/index.html manually"; \
		fi; \
	else \
		echo "No Allure results or report found. Run 'make test-report' first."; \
		exit 1; \
	fi

# Code quality commands
lint:
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import flake8" 2>/dev/null; then \
		echo "Virtual environment or flake8 not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Running linting checks..."
	@$(PYTHON) -m flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503 --exclude=venv
	@$(MAKE) _clean

format:
	@if [ ! -d "venv" ] || ! $(PYTHON) -c "import black" 2>/dev/null; then \
		echo "Virtual environment or black not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "Formatting code with black..."
	@$(PYTHON) -m black src/ tests/ --line-length=100 --exclude=venv
	@$(MAKE) _clean

# Quick development workflow
dev: install
	@echo "Development environment ready!"
	@echo "Run 'make run-server' to start the server"
	@echo "Run 'make test' to run tests"
	@$(MAKE) _clean

# Default target
help:
	@echo "FactScreen API - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  install        Install all dependencies (including test dependencies)"
	@echo "  check-deps     Check if all dependencies are installed"
	@echo ""
	@echo "Development:"
	@echo "  run-server     Start the development server"
	@echo "  stop-server    Stop the development server"
	@echo "  run-frontend   Start Streamlit frontend only"
	@echo "  run-app        Start both backend and frontend"
	@echo "  clean          Clean cache files and temporary files"
	@echo ""
	@echo "Testing:"
	@echo "  test           Run all tests"
	@echo "  test-api       Run API route tests"
	@echo "  test-services  Run core services tests"
	@echo "  test-pipelines Run data pipeline tests"
	@echo "  test-integration Run integration workflow tests"
	@echo "  test-coverage  Run tests with coverage report"
	@echo "  test-all       Run all tests with verbose output"
	@echo "  test-report    Generate Allure test report"
	@echo "  test-report-serve Serve Allure report in browser"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code with black"
	@echo ""
	@echo "Quick Start:"
	@echo "  dev            Setup development environment"
	@echo ""
