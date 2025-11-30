@echo off
REM FactScreen API - Windows Launcher
setlocal enabledelayedexpansion
setlocal ENABLEEXTENSIONS

:menu
cls
echo.
echo ========================================
echo   FactScreen API - Windows Launcher
echo ========================================
echo.
echo   1. Install/Setup (first time only)
echo   2. Run Full Application (Backend + Frontend)
echo   3. Run Backend Only
echo   4. Run Frontend Only
echo   5. Run Tests
echo   6. Run Tests with Coverage
echo   7. Exit
echo.
set /p choice="Select an option (1-7): "

if "%choice%"=="" goto menu
if "%choice%"=="1" goto install
if "%choice%"=="2" goto run_app
if "%choice%"=="3" goto run_server
if "%choice%"=="4" goto run_frontend
if "%choice%"=="5" goto run_tests
if "%choice%"=="6" goto run_tests_coverage
if "%choice%"=="7" goto end
echo.
echo Invalid choice. Please try again.
timeout /t 2 /nobreak >nul
goto menu

:install
cls
echo.
echo ========================================
echo   Installing FactScreen API
echo ========================================
echo.
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo Error: Could not create virtual environment. Please install Python 3.8+ first.
        pause
        goto menu
    )
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo.
echo Upgrading pip, setuptools, and wheel...
call venv\Scripts\pip.exe install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo Error: Could not upgrade pip
    pause
    goto menu
)

echo.
echo Installing all dependencies...
call venv\Scripts\pip.exe install -r requirements-dev.txt
if errorlevel 1 (
    echo Error: Could not install dependencies
    pause
    goto menu
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Create a .env file with your API keys (see README.md)
echo   2. Select option 2 to run the application
echo.
pause
goto menu

:run_app
cls
echo.
echo ========================================
echo   Starting FactScreen Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo ERROR: Virtual environment not found.
    echo Please run option 1 (Install/Setup) first.
    echo.
    pause
    goto menu
)

REM Check if venv\Scripts exists
if not exist "venv\Scripts" (
    echo.
    echo ERROR: Virtual environment Scripts directory not found.
    echo The virtual environment may be corrupted. Please run option 1 (Install/Setup) again.
    echo.
    pause
    goto menu
)

REM Check if Python executable exists
if not exist "venv\Scripts\python.exe" (
    echo.
    echo ERROR: Python executable not found in virtual environment.
    echo The virtual environment may be corrupted. Please run option 1 (Install/Setup) again.
    echo.
    pause
    goto menu
)

REM Check if dependencies are installed
echo Checking dependencies...
venv\Scripts\python.exe -c "import uvicorn, streamlit" 2>nul
if errorlevel 1 (
    echo Dependencies not installed. Installing now...
    call venv\Scripts\pip.exe install --upgrade pip setuptools wheel
    if errorlevel 1 (
        echo Failed to upgrade pip
        pause
        goto menu
    )
    call venv\Scripts\pip.exe install -r requirements-dev.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        goto menu
    )
    echo Dependencies installed successfully.
)

REM Set ports
set BACKEND_PORT=8000
set FRONTEND_PORT=8501

REM Check and free ports
echo Step 1: Checking ports...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%BACKEND_PORT%"') do (
    echo Port %BACKEND_PORT% is in use. Stopping process...
    taskkill /PID %%a /F >nul 2>&1
    timeout /t 1 /nobreak >nul
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%FRONTEND_PORT%"') do (
    echo Port %FRONTEND_PORT% is in use. Stopping process...
    taskkill /PID %%a /F >nul 2>&1
    timeout /t 1 /nobreak >nul
)

echo.
echo Step 2: Starting backend server on http://localhost:%BACKEND_PORT%...
start "FactScreen Backend" /MIN cmd /c "venv\Scripts\python.exe entrypoint\server.py"

REM Wait for backend to be ready
echo Waiting for backend to be ready...
set WAIT_COUNT=0
set MAX_WAIT=30
:wait_backend
timeout /t 1 /nobreak >nul
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:%BACKEND_PORT%/v1/health' -TimeoutSec 1 -UseBasicParsing; exit 0 } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 (
    echo.
    echo Backend server is ready on http://localhost:%BACKEND_PORT%
    echo API docs: http://localhost:%BACKEND_PORT%/docs
    goto start_frontend
)
set /a WAIT_COUNT+=1
if !WAIT_COUNT! geq %MAX_WAIT% (
    echo.
    echo Backend did not start within %MAX_WAIT% seconds. Please check the backend window.
    pause
    goto menu
)
echo|set /p="."
goto wait_backend

:start_frontend
echo.
echo Step 3: Starting frontend on http://localhost:%FRONTEND_PORT%...
set STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
start "FactScreen Frontend" cmd /k "venv\Scripts\python.exe -m streamlit run src\app\streamlit\main.py --server.port %FRONTEND_PORT% --server.headless true"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   FactScreen is running!
echo   Backend:  http://localhost:%BACKEND_PORT%
echo   Frontend: http://localhost:%FRONTEND_PORT%
echo   API Docs: http://localhost:%BACKEND_PORT%/docs
echo ========================================
echo.
echo Press any key to return to menu (servers will keep running)...
pause >nul
goto menu

:run_server
cls
echo.
echo ========================================
echo   Starting Backend Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo ERROR: Virtual environment not found.
    echo Please run option 1 (Install/Setup) first.
    echo.
    pause
    goto menu
)

REM Check if venv\Scripts exists
if not exist "venv\Scripts" (
    echo.
    echo ERROR: Virtual environment Scripts directory not found.
    echo The virtual environment may be corrupted. Please run option 1 (Install/Setup) again.
    echo.
    pause
    goto menu
)

REM Check if dependencies are installed
echo Checking dependencies...
venv\Scripts\python.exe -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo Dependencies not installed. Installing now...
    call venv\Scripts\pip.exe install --upgrade pip setuptools wheel
    if errorlevel 1 (
        echo Failed to upgrade pip
        pause
        goto menu
    )
    call venv\Scripts\pip.exe install -r requirements-dev.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        goto menu
    )
    echo Dependencies installed successfully.
)

echo Starting FactScreen API server...
echo.
call venv\Scripts\python.exe entrypoint\server.py
if errorlevel 1 (
    echo.
    echo Server encountered an error. Press any key to return to menu...
    pause >nul
    goto menu
)
echo.
echo Server stopped. Press any key to return to menu...
pause >nul
goto menu

:run_frontend
cls
echo.
echo ========================================
echo   Starting Frontend
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo ERROR: Virtual environment not found.
    echo Please run option 1 (Install/Setup) first.
    echo.
    pause
    goto menu
)

REM Check if venv\Scripts exists
if not exist "venv\Scripts" (
    echo.
    echo ERROR: Virtual environment Scripts directory not found.
    echo The virtual environment may be corrupted. Please run option 1 (Install/Setup) again.
    echo.
    pause
    goto menu
)

REM Check if dependencies are installed
echo Checking dependencies...
venv\Scripts\python.exe -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Dependencies not installed. Installing now...
    call venv\Scripts\pip.exe install --upgrade pip setuptools wheel
    if errorlevel 1 (
        echo Failed to upgrade pip
        pause
        goto menu
    )
    call venv\Scripts\pip.exe install -r requirements-dev.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        goto menu
    )
    echo Dependencies installed successfully.
)

echo Starting Streamlit frontend...
echo Note: Make sure the backend server is running on http://localhost:8000
echo.
set STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
call venv\Scripts\python.exe -m streamlit run src\app\streamlit\main.py --server.port 8501
if errorlevel 1 (
    echo.
    echo Frontend encountered an error. Press any key to return to menu...
    pause >nul
    goto menu
)
echo.
echo Frontend stopped. Press any key to return to menu...
pause >nul
goto menu

:run_tests
cls
echo.
echo ========================================
echo   Running Tests
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo ERROR: Virtual environment not found.
    echo Please run option 1 (Install/Setup) first.
    echo.
    pause
    goto menu
)

REM Check if venv\Scripts exists
if not exist "venv\Scripts" (
    echo.
    echo ERROR: Virtual environment Scripts directory not found.
    echo The virtual environment may be corrupted. Please run option 1 (Install/Setup) again.
    echo.
    pause
    goto menu
)

REM Check if dependencies are installed
echo Checking dependencies...
venv\Scripts\python.exe -c "import pytest" 2>nul
if errorlevel 1 (
    echo Dependencies not installed. Installing now...
    call venv\Scripts\pip.exe install --upgrade pip setuptools wheel
    if errorlevel 1 (
        echo Failed to upgrade pip
        pause
        goto menu
    )
    call venv\Scripts\pip.exe install -r requirements-dev.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        goto menu
    )
    echo Dependencies installed successfully.
)

echo Running all tests...
echo.
call venv\Scripts\python.exe -m pytest tests\ -v
if errorlevel 1 (
    echo.
    echo Some tests failed. Check the output above for details.
) else (
    echo.
    echo All tests passed!
)
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:run_tests_coverage
cls
echo.
echo ========================================
echo   Running Tests with Coverage
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo ERROR: Virtual environment not found.
    echo Please run option 1 (Install/Setup) first.
    echo.
    pause
    goto menu
)

REM Check if venv\Scripts exists
if not exist "venv\Scripts" (
    echo.
    echo ERROR: Virtual environment Scripts directory not found.
    echo The virtual environment may be corrupted. Please run option 1 (Install/Setup) again.
    echo.
    pause
    goto menu
)

REM Check if dependencies are installed
echo Checking dependencies...
venv\Scripts\python.exe -c "import pytest, pytest_cov" 2>nul
if errorlevel 1 (
    echo Dependencies not installed. Installing now...
    call venv\Scripts\pip.exe install --upgrade pip setuptools wheel
    if errorlevel 1 (
        echo Failed to upgrade pip
        pause
        goto menu
    )
    call venv\Scripts\pip.exe install -r requirements-dev.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        goto menu
    )
    echo Dependencies installed successfully.
)

echo Running tests with coverage analysis...
echo.
call venv\Scripts\python.exe -m pytest tests\ --cov=src --cov-report=html --cov-report=term-missing --cov-branch -v
if errorlevel 1 (
    echo.
    echo Some tests failed. Check the output above for details.
) else (
    echo.
    echo All tests passed!
)
echo.
if exist "htmlcov\index.html" (
    echo Coverage report generated: htmlcov\index.html
    echo Opening coverage report in browser...
    start htmlcov\index.html
) else (
    echo Warning: Coverage report not found.
)
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:end
cls
echo.
echo Stopping any running servers...
taskkill /FI "WINDOWTITLE eq FactScreen Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq FactScreen Frontend*" /F >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *streamlit*" >nul 2>&1
echo.
echo Goodbye!
timeout /t 2 /nobreak >nul
exit

