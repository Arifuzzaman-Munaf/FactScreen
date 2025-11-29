"""
Helper functions for the Streamlit frontend.

This module contains utility functions used throughout the Streamlit application,
including API communication, data formatting, and UI rendering helpers.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import html
from textwrap import dedent

# Ensure project root is in path (in case this module is imported directly)
_current_file = Path(__file__).resolve()
_project_root = _current_file.parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import requests
import streamlit as st

from src.app.streamlit.config import VALIDATION_ENDPOINT


def format_confidence(confidence: Optional[float]) -> str:
    """
    Format confidence score as a percentage string.

    Args:
        confidence: Confidence score between 0.0 and 1.0, or None

    Returns:
        Formatted percentage string (e.g., "85.5%") or "—" if None
    """
    if confidence is None:
        return "—"
    return f"{confidence * 100:.1f}%"


def build_payload(claim_text: str, claim_url: str) -> Dict[str, Any]:
    """
    Build API request payload from user input.

    Args:
        claim_text: Text claim entered by user
        claim_url: Optional URL entered by user

    Returns:
        Dictionary containing either 'url' or 'text' key for API request
    """
    if claim_url:
        return {"url": claim_url}
    return {"text": claim_text}


def call_backend(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make API request to the FactScreen backend.

    Args:
        payload: Request payload dictionary

    Returns:
        JSON response from the backend API

    Raises:
        RuntimeError: If the API request fails or returns an error status
    """
    try:
        response = requests.post(
            VALIDATION_ENDPOINT,
            json=payload,
            timeout=120,
        )
    except requests.RequestException as exc:
        raise RuntimeError(
            "Unable to reach FactScreen backend. Please ensure the API server is running."
        ) from exc

    if response.status_code >= 400:
        try:
            detail = response.json().get("detail")
        except Exception:  # pragma: no cover - defensive
            detail = response.text
        raise RuntimeError(detail or "Backend returned an error.")

    return response.json()


def render_provider_results(providers: List[Dict[str, Any]]) -> str:
    """
    Build an HTML table summarizing supporting evidence.

    Args:
        providers: List of provider result dictionaries

    Returns:
        HTML string representing the evidence table/placeholder.
    """
    if not providers:
        return dedent(
            """
            <div class="source-table-placeholder">
                No third-party sources were returned for this claim.
            </div>
            """
        ).strip()

    # Prepare table data with deduplication
    # Deduplicate based on rating and summary (same content = duplicate)
    seen_entries = {}  # key: (rating, summary_normalized) -> row_data

    for pr in providers:
        verdict = pr.get("verdict", "unknown").title()
        rating = pr.get("rating", "N/A")
        title = pr.get("title") or pr.get("summary") or "No title available"
        source_url = pr.get("source_url") or ""

        # Normalize summary for deduplication (lowercase, strip whitespace)
        summary_normalized = title.lower().strip()

        # Create a key for deduplication based on rating and summary
        dedup_key = (str(rating), summary_normalized)

        # Truncate long titles for table display
        display_title = title[:97] + "..." if len(title) > 100 else title

        # Format source URL
        if source_url and source_url.startswith("http"):
            source_value = source_url
        else:
            source_value = "N/A"

        if dedup_key not in seen_entries:
            # First occurrence - store the data
            seen_entries[dedup_key] = {
                "Rating": str(rating),
                "Summary": display_title,
                "Source": source_value,
            }
        else:
            # Duplicate found - keep first occurrence (already stored)
            # If this one has a valid URL and the stored one doesn't, update it
            existing = seen_entries[dedup_key]
            if source_value != "N/A" and existing["Source"] == "N/A":
                existing["Source"] = source_value

    # Convert to list for DataFrame
    table_data = list(seen_entries.values())

    if not table_data:
        return dedent(
            """
            <div class="source-table-placeholder">
                No third-party sources were returned for this claim.
            </div>
            """
        ).strip()

    rows_html = []
    for row in table_data:
        rating = html.escape(row["Rating"])
        summary = html.escape(row["Summary"])
        source = row["Source"]
        if source != "N/A" and source.startswith("http"):
            source_cell = (
                f'<a class="source-link" href="{html.escape(source)}" '
                f'target="_blank" rel="noopener">Visit Source</a>'
            )
        else:
            source_cell = "N/A"
        rows_html.append(
            dedent(
                f"""
                <tr>
                    <td class="rating-pill" data-rating="{rating.lower()}">{rating}</td>
                    <td class="summary-cell">{summary}</td>
                    <td class="source-cell">{source_cell}</td>
                </tr>
                """
            ).strip()
        )

    table_html = dedent(
        f"""
    <div class="source-table-wrapper">
        <table class="source-table">
            <thead>
                <tr>
                    <th>Rating</th>
                    <th>Summary</th>
                    <th>Source</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
    </div>
    """
    ).strip()

    return table_html


def render_sources_from_explanation(explanation: str) -> str:
    """
    Parse and render sources from explanation text as HTML.

    The backend appends a "Sources:" block with bullet list to the explanation.
    This function parses that section and returns formatted list items
    with clickable links when URLs are present.

    Args:
        explanation: Full explanation text including sources section

    Returns:
        HTML string containing formatted sources.
    """
    if "Sources:" not in explanation:
        return ""

    # Extract the sources block after the "Sources:" marker
    _, sources_block = explanation.split("Sources:", maxsplit=1)
    lines = [line.strip("- ").strip() for line in sources_block.splitlines() if line.strip()]
    if not lines:
        return ""

    items: List[str] = []
    seen: set[tuple[str, str]] = set()

    for idx, line in enumerate(lines, start=1):
        raw_line = line
        url = ""
        label = raw_line

        if "|" in raw_line:
            parts = [part.strip() for part in raw_line.split("|")]
            possible_url = parts[-1]
            if possible_url.startswith("http"):
                url = possible_url
                label = " | ".join(parts[:-1]).strip() or raw_line

        label_escaped = html.escape(label)
        key = (label_escaped.lower(), url.lower())
        if key in seen:
            continue
        seen.add(key)

        if url:
            items.append(
                f'<li><span class="source-title">{idx}. {label_escaped}</span>'
                f' — <a href="{html.escape(url)}" target="_blank" rel="noopener">Visit Link</a></li>'
            )
        else:
            items.append(f"<li>{idx}. {html.escape(raw_line)}</li>")

    if not items:
        return ""

    sources_html = dedent(
        f"""
        <div class="sources-list">
            <h4>Sources</h4>
            <ol>
                {''.join(items)}
            </ol>
        </div>
        """
    ).strip()

    return sources_html


def scroll_to_element(element_id: str, delay: int = 100) -> None:
    """
    Inject JavaScript to scroll to a specific element on the page.

    Args:
        element_id: HTML ID of the element to scroll to
        delay: Delay in milliseconds before attempting scroll
    """
    st.markdown(
        f"""
        <script>
            (function() {{
                function scrollToElement() {{
                    const element = document.getElementById('{element_id}');
                    if (element) {{
                        // Calculate scroll position to center the element
                        const elementRect = element.getBoundingClientRect();
                        const elementTop = elementRect.top + window.pageYOffset;
                        const elementHeight = elementRect.height;
                        const windowHeight = window.innerHeight;
                        const scrollPosition = elementTop - (windowHeight / 2) + (elementHeight / 2);
                        window.scrollTo({{
                            top: scrollPosition,
                            behavior: 'smooth'
                        }});
                        return true;
                    }}
                    return false;
                }}
                
                // Try immediately
                if (!scrollToElement()) {{
                    // If element not found, try after a short delay
                    setTimeout(scrollToElement, {delay});
                }}
            }})();
        </script>
        """,
        unsafe_allow_html=True,
    )
