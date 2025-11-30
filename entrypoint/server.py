#!/usr/bin/env python3
"""
Startup script for FactScreen API server
"""
import subprocess
import sys
import os
import socket
import platform
import signal
import time

# get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.app.core.config import settings

def is_port_in_use(port, host="127.0.0.1"):
    """Check if a port is in use on the given host.
    Args:
        port: The port to check.
        host: The host to check.
    Returns:
        True if the port is in use, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(1.0)
            result = s.connect_ex((host, port))
            return result == 0
        except Exception:
            return False

def kill_process_on_port(port):
    """Find and kill process using the given port.
    Args:
        port: The port to kill the process on.
    """
    current_platform = platform.system()
    try:
        # if the current platform is Windows, use the netstat command to find and kill the process
        if current_platform == "Windows":
            # Find PID(s) listening on the port
            result = subprocess.check_output(["netstat", "-ano"], encoding="utf-8")
            lines = result.strip().splitlines()
            for line in lines:
                if f":{port} " in line:
                    parts = line.split()
                    pid = parts[-1]
                    if pid != "0":
                        print(f"Stopping process with PID {pid} using port {port}...")
                        subprocess.call(["taskkill", "/PID", pid, "/F"])
        # if the current platform is not Windows, use the lsof command to find and kill the process
        else:
            # Use lsof (Unix/Linux/macOS)
            try:
                # First try to get PIDs using lsof
                result = subprocess.check_output(["lsof", "-ti", f":{port}"], encoding='utf-8')
                pids = result.strip().split('\n')

                for pid in pids:
                    if pid.strip():
                        print(f"Stopping process with PID {pid} using port {port}...")
                        try:
                            os.kill(int(pid), signal.SIGTERM)
                            time.sleep(0.5)
                            # If SIGTERM doesn't work, try SIGKILL
                            if is_port_in_use(port):
                                os.kill(int(pid), signal.SIGKILL)
                        except ProcessLookupError:
                            # Process already dead
                            pass
                        except Exception as e:
                            print(f"Warning: Could not kill process {pid}: {e}")
            except subprocess.CalledProcessError:
                # lsof returns non-zero exit code if nothing found
                pass
    except Exception as e:
        print(f"Warning: Could not stop process on port {port}: {e}")

def main():
    """Start the FactScreen API server"""

    # get the project root directory
    project_root = os.path.dirname(os.path.dirname(__file__))

    # if the project root directory does not exist, print an error and exit
    if not os.path.exists(project_root):
        print("Error: Project root directory not found!")
        sys.exit(1)

    # change the current working directory to the project root directory
    os.chdir(project_root)

    # add the project root to the Python path for imports
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # get the server port and host from the settings
    # For Render: PORT env var is used (default 10000), host must be 0.0.0.0
    # Explicitly check PORT env var first (Render requirement)
    port = int(os.getenv("PORT", settings.server_port))
    host = settings.server_host
    
    # Check if running in production (Render sets PORT env var)
    is_production = os.getenv("PORT") is not None
    
    # In production, always use 0.0.0.0 and skip port checking
    if is_production:
        host = "0.0.0.0"
        print(f"Starting FactScreen API server in production mode...")
        print(f"PORT environment variable: {os.getenv('PORT')}")
        print(f"Binding to {host}:{port}")
    else:
        # Development mode: Check if port is already in use
        if is_port_in_use(port, host):
            print(f"Port {port} is already in use. Attempting to stop server on port {port}...")
            kill_process_on_port(port)
            time.sleep(2)  # Give more time for processes to terminate
            
            # Double check before proceeding
            if is_port_in_use(port, host):
                print(f"Failed to free port {port}. Trying alternative port...")
                # Try alternative ports
                for alt_port in [8001, 8002, 8003, 8004, 8005]:
                    if not is_port_in_use(alt_port, host):
                        port = alt_port
                        print(f"Using alternative port {port}")
                        break
                else:
                    print("No available ports found. Please manually stop processes using ports 8000-8005.")
                    sys.exit(1)
            else:
                print(f"Port {port} is now free.")
        
        print("Starting FactScreen API server in development mode...")
        print(f"Server will be available at: http://{host}:{port}")
        print(f"API documentation: http://{host}:{port}/docs")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)

    try:
        # Build uvicorn command
        uvicorn_cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "src.app.main:app",
            "--host",
            host,
            "--port",
            str(port),
        ]
        
        # Add reload options only in development
        if not is_production:
            uvicorn_cmd.extend([
                "--reload",
                "--reload-dir",
                "src",
                "--reload-dir",
                "entrypoint",
                "--reload-dir",
                "tests",
                "--reload-exclude",
                "venv/*",
                "--reload-exclude",
                ".venv/*",
            ])
        
        # run the server using uvicorn
        subprocess.run(uvicorn_cmd)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()