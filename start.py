#!/usr/bin/env python3
"""
FactScreen API - Simple Python Launcher
Just run: python start.py
"""
import os
import sys
import subprocess
import time
import urllib.request
import http.server
import socketserver
import webbrowser
from threading import Timer


def serve_static_report(report_dir="allure-report", port=8080):
    """Serve static Allure report using Python HTTP server."""
    original_dir = os.getcwd()
    try:
        os.chdir(report_dir)
        handler = http.server.SimpleHTTPRequestHandler
        
        def open_browser():
            webbrowser.open(f'http://localhost:{port}')
        
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Server started at http://localhost:{port}")
            Timer(1, open_browser).start()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"\nError starting server: {e}")
    finally:
        os.chdir(original_dir)


def main():
    while True:
        print("\n" + "="*50)
        print("  FactScreen APP - Launcher")
        print("="*50)
        print("\n1. Install/Setup (first time only)")
        print("2. Run Full Application (Backend + Frontend) - Recommended")
        print("3. Run Backend Only")
        print("4. Run Frontend Only")
        print("5. Run Tests")
        print("6. Run Tests with Coverage")
        print("7. Run Tests with Allure Report")
        print("8. View Allure Report")
        print("9. Exit")
        
        choice = input("\nSelect (1-9): ").strip()
        
        venv_python = "venv\\Scripts\\python.exe" if os.name == 'nt' else "venv/bin/python"
        
        if choice == "1":
            print("\n" + "="*50)
            print("  Installing FactScreen API")
            print("="*50)
            print("\nCreating virtual environment...")
            if not os.path.exists("venv"):
                result = subprocess.run([sys.executable, "-m", "venv", "venv"])
                if result.returncode != 0:
                    print("Error: Could not create virtual environment.")
                    input("\nPress Enter to continue...")
                    continue
                print("Virtual environment created")
            else:
                print("Virtual environment already exists")
            
            print("\nUpgrading pip...")
            subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
            
            print("\nInstalling dependencies...")
            result = subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements-dev.txt"])
            if result.returncode == 0:
                print("\n" + "="*50)
                print("  Installation Complete!")
                print("="*50)
                print("\nNext steps:")
                print("  1. Create a .env file with your API keys (see README.md)")
                print("  2. Select option 2 to run the full application")
            else:
                print("\nInstallation failed. Check errors above.")
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            if not os.path.exists(venv_python):
                print("\nError: Virtual environment not found. Run option 1 first!")
                input("Press Enter to continue...")
                continue
            
            # Check dependencies
            print("\nChecking dependencies...")
            result = subprocess.run([venv_python, "-c", "import uvicorn, streamlit"],
                                   capture_output=True, text=True)
            if result.returncode != 0:
                print("Dependencies not installed. Installing now...")
                subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
                subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements-dev.txt"])
                print("Dependencies installed successfully.")
            
            print("\n" + "="*50)
            print("  Starting FactScreen Application")
            print("="*50)
            
            backend_port = 8000
            frontend_port = 8501
            
            print(f"\nStep 1: Starting backend on http://localhost:{backend_port}...")
            # Use os.path.join for proper cross-platform path handling
            server_script = os.path.join("entrypoint", "server.py")
            server_script_abs = os.path.abspath(server_script)
            
            # Start backend in background
            if os.name == 'nt':
                subprocess.Popen([venv_python, server_script_abs],
                                creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([venv_python, server_script_abs],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            
            # Wait for backend to be ready
            print("Waiting for backend to be ready...", end="", flush=True)
            max_wait = 30
            backend_ready = False
            for i in range(max_wait):
                try:
                    urllib.request.urlopen(f'http://localhost:{backend_port}/v1/health', timeout=1)
                    backend_ready = True
                    break
                except:
                    print(".", end="", flush=True)
                    time.sleep(1)
            
            if not backend_ready:
                print(f"\n\nBackend did not start within {max_wait} seconds.")
                print("Please check the backend window for errors.")
                input("\nPress Enter to continue...")
                continue
            
            print(f"\n✓ Backend is ready on http://localhost:{backend_port}")
            print(f"  API docs: http://localhost:{backend_port}/docs")
            
            print(f"\nStep 2: Starting frontend on http://localhost:{frontend_port}...")
            env = os.environ.copy()
            env['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
            # Use os.path.join for proper cross-platform path handling
            streamlit_script = os.path.join("src", "app", "streamlit", "main.py")
            streamlit_script_abs = os.path.abspath(streamlit_script)
            
            # Start frontend in background
            if os.name == 'nt':
                subprocess.Popen([venv_python, "-m", "streamlit", "run",
                                 streamlit_script_abs, "--server.port", str(frontend_port),
                                 "--server.headless", "true"],
                                creationflags=subprocess.CREATE_NEW_CONSOLE, env=env)
            else:
                subprocess.Popen([venv_python, "-m", "streamlit", "run",
                                 streamlit_script_abs, "--server.port", str(frontend_port),
                                 "--server.headless", "true"],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, env=env)
            
            time.sleep(3)
            
            print("\n" + "="*50)
            print("  FactScreen is running!")
            print("="*50)
            print(f"\n  Backend:  http://localhost:{backend_port}")
            print(f"  Frontend: http://localhost:{frontend_port}")
            print(f"  API Docs: http://localhost:{backend_port}/docs")
            print("\n" + "="*50)
            print("\nServers are running in separate windows.")
            print("Close those windows or press Ctrl+C in them to stop.")
            input("\nPress Enter to return to menu (servers will keep running)...")
            
        elif choice == "3":
            if not os.path.exists(venv_python):
                print("\nError: Virtual environment not found. Run option 1 first!")
                input("Press Enter to continue...")
                continue
            print("\nStarting backend on http://localhost:8000...")
            print("API docs will be available at http://localhost:8000/docs")
            print("Press Ctrl+C to stop the server\n")
            try:
                # Use os.path.join for proper cross-platform path handling
                server_script = os.path.join("entrypoint", "server.py")
                # Use absolute path to avoid any path interpretation issues
                server_script_abs = os.path.abspath(server_script)
                subprocess.run([venv_python, server_script_abs])
            except KeyboardInterrupt:
                print("\nServer stopped.")
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            if not os.path.exists(venv_python):
                print("\nError: Virtual environment not found. Run option 1 first!")
                input("Press Enter to continue...")
                continue
            print("\nStarting frontend on http://localhost:8501...")
            print("Note: Make sure backend is running on http://localhost:8000")
            print("Press Ctrl+C to stop the frontend\n")
            print("Press Enter if Streamlit asks for Email or server not started\n")
            env = os.environ.copy()
            env['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
            # Use os.path.join for proper cross-platform path handling
            streamlit_script = os.path.join("src", "app", "streamlit", "main.py")
            streamlit_script_abs = os.path.abspath(streamlit_script)
            try:
                subprocess.run([venv_python, "-m", "streamlit", "run", streamlit_script_abs, "--server.port", "8501"], env=env)
            except KeyboardInterrupt:
                print("\nFrontend stopped.")
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            if not os.path.exists(venv_python):
                print("\nError: Virtual environment not found. Run option 1 first!")
                input("Press Enter to continue...")
                continue
            print("\nRunning tests...\n")
            tests_dir = "tests\\" if os.name == 'nt' else "tests/"
            result = subprocess.run([venv_python, "-m", "pytest", tests_dir, "-v"])
            if result.returncode == 0:
                print("\nAll tests passed!")
            else:
                print("\nSome tests failed.")
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            if not os.path.exists(venv_python):
                print("\nError: Virtual environment not found. Run option 1 first!")
                input("Press Enter to continue...")
                continue
            print("\nRunning tests with coverage...\n")
            tests_dir = "tests\\" if os.name == 'nt' else "tests/"
            result = subprocess.run([venv_python, "-m", "pytest", tests_dir,
                                   "--cov=src", "--cov-report=html", "--cov-report=term-missing",
                                   "--cov-branch", "-v"])
            if result.returncode == 0:
                print("\nAll tests passed!")
            else:
                print("\nSome tests failed.")
            
            if os.path.exists("htmlcov/index.html"):
                print("\nCoverage report: htmlcov/index.html")
                if os.name == 'nt':
                    os.startfile("htmlcov/index.html")
                elif sys.platform == 'darwin':
                    subprocess.run(['open', 'htmlcov/index.html'])
                else:
                    subprocess.run(['xdg-open', 'htmlcov/index.html'])
            input("\nPress Enter to continue...")
            
        elif choice == "7":
            if not os.path.exists(venv_python):
                print("\nError: Virtual environment not found. Run option 1 first!")
                input("Press Enter to continue...")
                continue
            
            # Check if allure-pytest is installed
            print("\nChecking dependencies...")
            result = subprocess.run([venv_python, "-c", "import pytest, allure"],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("Installing allure-pytest...")
                subprocess.run([venv_python, "-m", "pip", "install", "allure-pytest"])
            
            print("\n" + "="*50)
            print("  Running Tests with Allure Report")
            print("="*50)
            print("\nRunning tests...\n")
            
            # Create allure-results directory
            os.makedirs("allure-results", exist_ok=True)
            
            tests_dir = "tests\\" if os.name == 'nt' else "tests/"
            result = subprocess.run([venv_python, "-m", "pytest", tests_dir,
                                   "--alluredir=allure-results", "-v", "--tb=short"])
            
            if result.returncode == 0:
                print("\nAll tests passed!")
            else:
                print("\nSome tests failed. Check the output above.")
            
            print("\nGenerating Allure report...")
            
            # Check if Allure CLI is available
            allure_available = False
            try:
                subprocess.run(["allure", "--version"], capture_output=True, check=True)
                allure_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                allure_available = False
            
            if allure_available:
                # Generate HTML report
                print("Generating HTML report...")
                subprocess.run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean"])
                
                if os.path.exists("allure-report/index.html"):
                    print("\n✓ Allure report generated: allure-report/index.html")
                    print("\nStarting Allure report server...")
                    print("Report will open in your browser at http://localhost:8080")
                    print("Press Ctrl+C in the server window to stop the server")
                    print("\nNote: Keep this window open while viewing the report.")
                    try:
                        # Use allure serve which starts a web server (recommended)
                        subprocess.run(["allure", "serve", "allure-results"])
                    except KeyboardInterrupt:
                        print("\nReport server stopped.")
                else:
                    print("\nWarning: Report file not found after generation.")
            else:
                print("\n⚠ Allure CLI not found. Test results saved to: allure-results/")
                print("\nTo generate HTML report, install Allure CLI:")
                if os.name == 'nt':
                    print("  Option 1: Download from https://github.com/allure-framework/allure2/releases")
                    print("  Option 2: Install via npm: npm install -g allure-commandline")
                    print("  Option 3: Install via Chocolatey: choco install allure")
                elif sys.platform == 'darwin':
                    print("  brew install allure")
                else:
                    print("  See: https://docs.qameta.io/allure/")
                print("\nOr use: npm install -g allure-commandline")
            
            input("\nPress Enter to continue...")
            
        elif choice == "8":
            print("\n" + "="*50)
            print("  View Allure Report")
            print("="*50)
            print()
            
            # Check if allure-results exists
            if not os.path.exists("allure-results") and not os.path.exists("allure-report"):
                print("No Allure results found.")
                print("Please run option 7 (Run Tests with Allure Report) first.")
                input("\nPress Enter to continue...")
                continue
            
            # Check if Allure CLI is available
            allure_available = False
            try:
                subprocess.run(["allure", "--version"], capture_output=True, check=True)
                allure_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                allure_available = False
            
            if allure_available:
                # Use allure serve which is the recommended way (starts web server)
                if os.path.exists("allure-results"):
                    print("\nStarting Allure report server...")
                    print("Report will open in your browser at http://localhost:8080")
                    print("Press Ctrl+C to stop the server")
                    print("\nNote: Keep this window open while viewing the report.")
                    try:
                        subprocess.run(["allure", "serve", "allure-results"])
                    except KeyboardInterrupt:
                        print("\nReport server stopped.")
                elif os.path.exists("allure-report/index.html"):
                    # If only static report exists, try to serve it
                    print("\nFound static report. Starting server...")
                    print("Report will be available at http://localhost:8080")
                    print("Press Ctrl+C to stop the server")
                    try:
                        # Generate fresh from results if available, otherwise serve static
                        if os.path.exists("allure-results"):
                            subprocess.run(["allure", "serve", "allure-results"])
                        else:
                            # For static reports, use Python HTTP server
                            print("\nServing static report...")
                            serve_static_report()
                    except KeyboardInterrupt:
                        print("\nServer stopped.")
                else:
                    print("\nNo Allure results or report found. Run option 7 first.")
            else:
                # Allure CLI not available - try to serve static report with Python HTTP server
                if os.path.exists("allure-report/index.html"):
                    print("\n⚠ Allure CLI not found. Using Python HTTP server to view report...")
                    print("Report will be available at http://localhost:8080")
                    print("Press Ctrl+C to stop the server")
                    serve_static_report()
                else:
                    print("\n⚠ Allure CLI not found and no report available.")
                    print("\nTo view reports properly, install Allure CLI:")
                    if os.name == 'nt':
                        print("  Option 1: Download from https://github.com/allure-framework/allure2/releases")
                        print("  Option 2: npm install -g allure-commandline")
                        print("  Option 3: choco install allure")
                    elif sys.platform == 'darwin':
                        print("  brew install allure")
                    else:
                        print("  See: https://docs.qameta.io/allure/")
                    print("\nOr use: npm install -g allure-commandline")
                    print("\nTest results are saved in: allure-results/")
            
            input("\nPress Enter to continue...")
            
        elif choice == "9":
            print("\nGoodbye!\n")
            sys.exit(0)
        else:
            print("\nInvalid choice! Please select 1-9.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)