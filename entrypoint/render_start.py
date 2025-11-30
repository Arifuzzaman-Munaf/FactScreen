#!/usr/bin/env python3
"""
Production startup script for Render deployment.
This script ensures proper port binding for Render.
"""
import os
import sys

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Change to project root
os.chdir(PROJECT_ROOT)

# Get port from environment (Render sets this, default is 10000)
port = int(os.getenv("PORT", 10000))
host = "0.0.0.0"  # Render requires binding to 0.0.0.0

print(f"Starting FactScreen API server on Render...")
print(f"PORT environment variable: {os.getenv('PORT', 'not set')}")
print(f"Binding to {host}:{port}")

# Start uvicorn directly
import uvicorn

if __name__ == "__main__":
    try:
        uvicorn.run(
            "src.app.main:app",
            host=host,
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

