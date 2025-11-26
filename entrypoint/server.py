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

def is_port_in_use(port, host="127.0.0.1"):
    """Check if a port is in use on the given host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(1.0)
            result = s.connect_ex((host, port))
            return result == 0
        except Exception:
            return False

def kill_process_on_port(port):
    """Find and kill process using the given port."""
    current_platform = platform.system()
    try:
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
        else:
            # Use lsof (Unix/Linux/macOS) - more aggressive approach
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

    project_root = os.path.dirname(os.path.dirname(__file__))

    if not os.path.exists(project_root):
        print("Error: Project root directory not found!")
        sys.exit(1)

    os.chdir(project_root)
    # Add project root to Python path for imports
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    port = 8000
    host = "127.0.0.1"

    # Check if port is already in use and stop the process if necessary
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

    print("Starting FactScreen API server...")
    print(f"Server will be available at: http://localhost:{port}")
    print(f"API documentation: http://localhost:{port}/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "src.app.main:app",
                "--reload",
                "--reload-dir",
                "src",
                "--reload-dir",
                "config",
                "--reload-dir",
                "entrypoint",
                "--reload-dir",
                "tests",
                "--reload-exclude",
                "venv/*",
                "--reload-exclude",
                ".venv/*",
                "--host",
                "0.0.0.0",
                "--port",
                str(port),
            ]
        )
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

