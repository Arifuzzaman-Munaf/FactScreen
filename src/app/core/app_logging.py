"""
Centralized logging configuration for the FactScreen application.

This module configures Python's logging system with both console and file
handlers so every part of the app shares a consistent log format. Static
settings (level, log directory/file) are managed via config/local.yaml and
surfaced through src.app.core.config.Settings.
"""

from __future__ import annotations

import logging
from logging.config import dictConfig
from pathlib import Path
from typing import Any, Dict

from src.app.core.config import settings

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _build_logging_config() -> Dict[str, Any]:
    """
    Build a logging configuration dictionary compatible with dictConfig.

    Returns:
        Dictionary describing formatters, handlers, and loggers.
    """
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / settings.log_file

    level = (settings.log_level or "INFO").upper()

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": LOG_FORMAT,
                "datefmt": DATE_FORMAT,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": level,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "level": level,
                "filename": str(log_file),
                "maxBytes": 5 * 1024 * 1024,  # 5 MB
                "backupCount": 3,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": level,
            "handlers": ["console", "file"],
        },
    }


def setup_logging() -> None:
    """
    Configure global logging for the application.

    Call this once at startup (e.g., before instantiating FastAPI) to ensure
    all modules share the same logging handlers.
    """
    config = _build_logging_config()
    dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger configured by setup_logging()."""
    return logging.getLogger(name)