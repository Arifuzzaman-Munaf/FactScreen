"""
Configuration for the Streamlit frontend.

Static/frontend configuration (API base URL, verdict colors, etc.) is loaded
from config/local.yaml so that the entire project shares a single source of
truth for non-secret settings. API keys remain in the .env file only.
"""

import os
from pathlib import Path
from typing import Any, Dict

import yaml


def _load_frontend_yaml() -> Dict[str, Any]:
    """Load the frontend section from config/local.yaml, if present."""
    config_path = Path("config") / "local.yaml"
    if not config_path.exists():
        return {}

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        data = {}
    frontend_cfg = data.get("frontend", {}) if isinstance(data, dict) else {}
    return frontend_cfg if isinstance(frontend_cfg, dict) else {}


_FRONTEND_CFG = _load_frontend_yaml()


# API Configuration
_DEFAULT_API_URL = _FRONTEND_CFG.get("default_api_url", "http://localhost:8000")
DEFAULT_API_URL = _DEFAULT_API_URL
API_BASE_URL = os.getenv("FACTSCREEN_API_URL", DEFAULT_API_URL).rstrip("/")
VALIDATION_ENDPOINT = f"{API_BASE_URL}/v1/validate"
PDF_REPORT_ENDPOINT = f"{API_BASE_URL}/v1/report/pdf"

# Verdict Color Mapping
_DEFAULT_VERDICT_COLORS: Dict[str, str] = {
    "true": "#22c55e",  # Green
    "misleading": "#ef4444",  # Red
    "unknown": "#eab308",  # Yellow
    "false": "#ef4444",  # Red (alias for misleading)
}
VERDICT_COLORS: Dict[str, str] = {
    **_DEFAULT_VERDICT_COLORS,
    **(_FRONTEND_CFG.get("verdict_colors") or {}),
}
