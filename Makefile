# FactScreen API Makefile
# OS-agnostic Makefile for cross-platform compatibility

.PHONY: help install clean _clean test test-api test-services test-pipelines test-integration test-coverage test-all test-report test-report-allure run-server stop-server lint format check-deps dev run-frontend run-app

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
	@BACKEND_PORT=8000; \
	FRONTEND_PORT=8501; \
	echo "Step 1: Checking and freeing ports..."; \
	for port in $$BACKEND_PORT $$FRONTEND_PORT; do \
		if lsof -ti:$$port > /dev/null 2>&1; then \
			echo "⚠️  Port $$port is in use. Stopping existing process..."; \
			lsof -ti:$$port | xargs kill -9 2>/dev/null || true; \
			sleep 1; \
			if lsof -ti:$$port > /dev/null 2>&1; then \
				if [ $$port -eq 8000 ]; then \
					for alt_port in 8001 8002 8003 8004 8005; do \
						if ! lsof -ti:$$alt_port > /dev/null 2>&1; then \
							BACKEND_PORT=$$alt_port; \
							echo "✔ Using alternative backend port $$BACKEND_PORT"; \
							break; \
						fi; \
					done; \
				elif [ $$port -eq 8501 ]; then \
					for alt_port in 8502 8503 8504 8505 8506; do \
						if ! lsof -ti:$$alt_port > /dev/null 2>&1; then \
							FRONTEND_PORT=$$alt_port; \
							echo "✔ Using alternative frontend port $$FRONTEND_PORT"; \
							break; \
						fi; \
					done; \
				fi; \
			fi; \
		fi; \
	done; \
	echo ""; \
	echo "Step 2: Starting backend server on http://localhost:$$BACKEND_PORT..."; \
	$(PYTHON) entrypoint/server.py > /tmp/factscreen-backend.log 2>&1 & \
	BACKEND_PID=$$!; \
	echo "Backend starting (PID: $$BACKEND_PID)..."; \
	echo "Waiting for backend to be ready..."; \
	MAX_WAIT=30; \
	WAIT_COUNT=0; \
	HEALTH_CHECK_CMD=""; \
	if command -v curl > /dev/null 2>&1; then \
		HEALTH_CHECK_CMD="curl -s -f http://localhost:$$BACKEND_PORT/v1/health > /dev/null 2>&1"; \
	elif command -v wget > /dev/null 2>&1; then \
		HEALTH_CHECK_CMD="wget -q --spider http://localhost:$$BACKEND_PORT/v1/health > /dev/null 2>&1"; \
	else \
		HEALTH_CHECK_CMD="$(PYTHON) -c \"import urllib.request; urllib.request.urlopen('http://localhost:$$BACKEND_PORT/v1/health').read()\" > /dev/null 2>&1"; \
	fi; \
	while [ $$WAIT_COUNT -lt $$MAX_WAIT ]; do \
		if eval $$HEALTH_CHECK_CMD; then \
			echo ""; \
			echo "✔ Backend server is ready on http://localhost:$$BACKEND_PORT"; \
			echo "  API docs: http://localhost:$$BACKEND_PORT/docs"; \
			break; \
		fi; \
		sleep 1; \
		WAIT_COUNT=$$((WAIT_COUNT + 1)); \
		if [ $$((WAIT_COUNT % 5)) -eq 0 ]; then \
			echo  " ($$WAIT_COUNT/$$MAX_WAIT)"; \
		else \
			echo  "."; \
		fi; \
	done; \
	if [ $$WAIT_COUNT -eq $$MAX_WAIT ]; then \
		echo ""; \
		echo "⚠️  Backend did not start within $$MAX_WAIT seconds. Check /tmp/factscreen-backend.log"; \
		kill $$BACKEND_PID 2>/dev/null || true; \
		$(MAKE) _clean; \
		exit 1; \
	fi; \
	echo ""; \
	echo "Step 3: Starting frontend on http://localhost:$$FRONTEND_PORT..."; \
	STREAMLIT_SERVER_FILE_WATCHER_TYPE=none $(PYTHON) -m streamlit run src/app/streamlit/main.py --server.port $$FRONTEND_PORT --server.headless true & \
	FRONTEND_PID=$$!; \
	sleep 3; \
	if ps -p $$FRONTEND_PID > /dev/null 2>&1; then \
		echo "✔ Frontend is ready on http://localhost:$$FRONTEND_PORT"; \
	else \
		echo "❌ Frontend failed to start. Check logs above."; \
		kill $$BACKEND_PID 2>/dev/null || true; \
		$(MAKE) _clean; \
		exit 1; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  FactScreen is running!"; \
	echo "  Backend:  http://localhost:$$BACKEND_PORT"; \
	echo "  Frontend: http://localhost:$$FRONTEND_PORT"; \
	echo "  API Docs: http://localhost:$$BACKEND_PORT/docs"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "Press Ctrl+C to stop both servers"; \
	echo ""; \
	wait $$FRONTEND_PID; \
	EXIT_CODE=$$?; \
	echo ""; \
	echo "Stopping servers..."; \
	kill $$BACKEND_PID 2>/dev/null || true; \
	pkill -f "uvicorn.*src.app.main:app" 2>/dev/null || true; \
	pkill -f "streamlit.*main.py" 2>/dev/null || true; \
	$(MAKE) _clean; \
	exit $$EXIT_CODE

# Setup commands
install:
	@echo "Creating virtual environment..."
	@if [ ! -d "venv" ]; then \
		python3 -m venv venv 2>/dev/null || python -m venv venv 2>/dev/null || (echo "Error: Could not create virtual environment. Please install Python 3.8+ first."; exit 1); \
		echo "✔ Virtual environment created"; \
	else \
		echo "Virtual environment already exists"; \
	fi
	@echo "Upgrading pip, setuptools, and wheel..."
	@if [ -f "venv/bin/pip" ]; then \
		venv/bin/pip install --upgrade pip setuptools wheel; \
	elif [ -f "venv/Scripts/pip.exe" ]; then \
		venv/Scripts/pip.exe install --upgrade pip setuptools wheel; \
	else \
		echo "Error: Could not find pip in virtual environment"; \
		exit 1; \
	fi
	@echo "Installing all dependencies (including test dependencies)..."
	@if [ -f "venv/bin/pip" ]; then \
		venv/bin/pip install -r requirements-dev.txt; \
	elif [ -f "venv/Scripts/pip.exe" ]; then \
		venv/Scripts/pip.exe install -r requirements-dev.txt; \
	else \
		echo "Error: Could not find pip in virtual environment"; \
		exit 1; \
	fi
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
	if [ -d "htmlcov" ]; then \
		echo "✓ Coverage report generated: htmlcov/index.html"; \
		if command -v open >/dev/null 2>&1; then \
			echo "  Opening coverage report in browser..."; \
			open htmlcov/index.html; \
		elif command -v xdg-open >/dev/null 2>&1; then \
			echo "  Opening coverage report in browser..."; \
			xdg-open htmlcov/index.html; \
		else \
			echo "  Open it manually: htmlcov/index.html"; \
		fi; \
	else \
		echo "⚠ Warning: Coverage report directory not found"; \
	fi; \
	$(PYTHON) -c "import os, shutil, glob; \
		exclude = {'venv', '.git', 'htmlcov'}; \
		paths = []; \
		paths.extend([d for d in glob.glob('**/__pycache__', recursive=True) if not any(ex in d for ex in exclude)]); \
		paths.extend([f for f in glob.glob('**/*.pyc', recursive=True) if not any(ex in f for ex in exclude)]); \
		paths.extend([f for f in glob.glob('**/*.pyo', recursive=True) if not any(ex in f for ex in exclude)]); \
		paths.extend([d for d in glob.glob('**/.pytest_cache', recursive=True) if not any(ex in d for ex in exclude)]); \
		paths.extend([d for d in glob.glob('**/.mypy_cache', recursive=True) if not any(ex in d for ex in exclude)]); \
		paths.extend([f for f in glob.glob('**/.coverage', recursive=True) if not any(ex in f for ex in exclude)]); \
		paths.extend([d for d in glob.glob('**/allure-results', recursive=True) if not any(ex in d for ex in exclude)]); \
		[shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p) for p in paths if os.path.exists(p)]; \
	" 2>/dev/null || true; \
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
		echo "Run 'make test-report-allure' to view it in browser"; \
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

test-report-allure:
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
	@echo "  test-report-allure Serve Allure report in browser"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code with black"
	@echo ""
	@echo "Quick Start:"
	@echo "  dev            Setup development environment"
	@echo ""