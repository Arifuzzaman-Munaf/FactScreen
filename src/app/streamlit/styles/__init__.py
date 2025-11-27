"""
Modular CSS assembly utilities for the Streamlit frontend.

This package breaks the previous monolithic styles module into smaller,
focused sections so the theme is easier to reason about and maintain.
"""

from __future__ import annotations

from textwrap import dedent

from .base import BASE_CSS
from .components import COMPONENTS_CSS
from .forms import FORMS_CSS
from .navbar import NAVBAR_CSS
from .processing import PROCESSING_CSS
from .responsive import RESPONSIVE_CSS
from .verdict import VERDICT_CSS

_CSS_SECTIONS = [
    BASE_CSS,
    NAVBAR_CSS,
    FORMS_CSS,
    COMPONENTS_CSS,
    VERDICT_CSS,
    PROCESSING_CSS,
    RESPONSIVE_CSS,
]


def build_theme_css() -> str:
    """Compose the ordered CSS sections into a single <style> block."""
    body = "\n\n".join(section.strip() for section in _CSS_SECTIONS if section.strip())
    return dedent(
        f"""
        <style>
        {body}
        </style>
        """
    ).strip()


THEME_CSS = build_theme_css()

__all__ = ["THEME_CSS", "build_theme_css"]

