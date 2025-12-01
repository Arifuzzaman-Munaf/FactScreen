#!/usr/bin/env python3
"""
Render-specific startup script for FactScreen API
This script is optimized for Render's deployment environment
"""
import os
import sys
import uvicorn

# Add project root to path
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

# Start uvicorn server
# This must stay in foreground for Render to detect the port
uvicorn.run(
    "src.app.main:app",
    host=host,
    port=port,
    log_level="info"
)

