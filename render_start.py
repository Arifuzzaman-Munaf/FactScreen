#!/usr/bin/env python3
"""
Render-specific startup script for FactScreen API
This script is optimized for Render's deployment environment
"""
import os
import sys

# Add project root to path FIRST, before any imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Get PORT from environment (Render sets this automatically)
# Default to 10000 if not set (Render's default)
port = int(os.environ.get("PORT", 10000))
host = "0.0.0.0"  # Render requires binding to 0.0.0.0

print(f"Starting FactScreen API on Render...")
print(f"Host: {host}")
print(f"Port: {port}")
print(f"PORT env var: {os.environ.get('PORT', 'NOT SET')}")
print(f"Python path: {sys.path[:3]}")  # Show first 3 paths for debugging

# Test import before starting server
try:
    print("Testing imports...")
    import uvicorn
    print("✓ uvicorn imported successfully")
    
    # Try importing the app to catch any import errors early
    print("Testing app import...")
    from src.app.main import app
    print("✓ App imported successfully")
    print(f"✓ App name: {app.title}")
    
except Exception as e:
    print(f"✗ ERROR during import: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Start uvicorn server
# This must stay in foreground for Render to detect the port
print(f"\nStarting uvicorn server on {host}:{port}...")
print("=" * 50)

try:
    # Use string format for app (standard uvicorn approach)
    uvicorn.run(
        "src.app.main:app",
        host=host,
        port=port,
        log_level="info"
    )
except Exception as e:
    print(f"✗ ERROR starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

