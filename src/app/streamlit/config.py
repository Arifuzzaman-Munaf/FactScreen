"""
Configuration constants for the Streamlit frontend.

This module contains all configuration constants used throughout the Streamlit
application, including API endpoints, verdict colors, and default values.
"""

import os
from typing import Dict

# API Configuration
DEFAULT_API_URL = "http://localhost:8000"
API_BASE_URL = os.getenv("FACTSCREEN_API_URL", DEFAULT_API_URL).rstrip("/")
VALIDATION_ENDPOINT = f"{API_BASE_URL}/v1/validate"

# Verdict Color Mapping
VERDICT_COLORS: Dict[str, str] = {
    "true": "#22c55e",  # Green
    "misleading": "#ef4444",  # Red
    "unknown": "#eab308",  # Yellow
    "false": "#ef4444",  # Red (alias for misleading)
}


