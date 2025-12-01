#!/usr/bin/env python3
"""
FactScreen API - Simple Python Launcher
Just run: python start.py
"""
import os
import sys
import subprocess
import time

def main():
    while True:
        print("\n" + "="*50)
        print("  FactScreen API - Launcher")
        print("="*50)
        print("\n1. Install/Setup (first time only)")
        print("2. Run Full Application (Backend + Frontend) - Recommended")
        print("3. Run Backend Only")
        print("4. Run Frontend Only")
        print("5. Run Tests")
        print("6. Run Tests with Coverage")
        print("7. Exit")
        
        choice = input("\nSelect (1-7): ").strip()
        
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
            server_script = "entrypoint\\server.py" if os.name == 'nt' else "entrypoint/server.py"
            
            # Start backend in background
            if os.name == 'nt':
                backend_process = subprocess.Popen([venv_python, server_script],
                                                  creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                backend_process = subprocess.Popen([venv_python, server_script],
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.DEVNULL)
            
            # Wait for backend to be ready
            print("Waiting for backend to be ready...", end="", flush=True)
            import urllib.request
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
                backend_process.terminate()
                input("\nPress Enter to continue...")
                continue
            
            print(f"\n✓ Backend is ready on http://localhost:{backend_port}")
            print(f"  API docs: http://localhost:{backend_port}/docs")
            
            print(f"\nStep 2: Starting frontend on http://localhost:{frontend_port}...")
            env = os.environ.copy()
            env['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
            streamlit_script = "src\\app\\streamlit\\main.py" if os.name == 'nt' else "src/app/streamlit/main.py"
            
            # Start frontend in background
            if os.name == 'nt':
                frontend_process = subprocess.Popen([venv_python, "-m", "streamlit", "run",
                                                   streamlit_script, "--server.port", str(frontend_port),
                                                   "--server.headless", "true"],
                                                  creationflags=subprocess.CREATE_NEW_CONSOLE, env=env)
            else:
                frontend_process = subprocess.Popen([venv_python, "-m", "streamlit", "run",
                                                   streamlit_script, "--server.port", str(frontend_port),
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
                server_script = "entrypoint\\server.py" if os.name == 'nt' else "entrypoint/server.py"
                subprocess.run([venv_python, server_script])
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
            env = os.environ.copy()
            env['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
            streamlit_script = "src\\app\\streamlit\\main.py" if os.name == 'nt' else "src/app/streamlit/main.py"
            try:
                subprocess.run([venv_python, "-m", "streamlit", "run", streamlit_script, "--server.port", "8501"], env=env)
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
            print("\nGoodbye!\n")
            sys.exit(0)
        else:
            print("\nInvalid choice! Please select 1-7.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)

