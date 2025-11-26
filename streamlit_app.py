"""
Streamlit presentation layer for FactScreen.

Implements the UI/UX described in the presentation-layer spec:
- Minimalist home screen with navigation, claim input, and clear CTA.
- Processing indicator while awaiting backend.
- Verdict + confidence + evidence display.
- Expandable explainability panel with LLM reasoning and sources.
- WCAG-friendly colour palette and error handling.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_API_URL = "http://localhost:8000"
API_BASE_URL = os.getenv("FACTSCREEN_API_URL", DEFAULT_API_URL).rstrip("/")
VALIDATION_ENDPOINT = f"{API_BASE_URL}/v1/validate"

VERDICT_COLORS = {
    "true": "#1db954",  # emerald
    "misleading": "#ff4d4f",  # coral red
    "unknown": "#ffb347",  # warm amber
}

THEME_CSS = """
<style>
:root {
    --bg-dark: #0f172a;
    --bg-card: #111827;
    --bg-light: #f8fafc;
    --accent-primary: #6366f1;
    --accent-secondary: #f472b6;
    --text-light: #f8fafc;
    --text-dark: #0f172a;
}

.stApp {
    background: linear-gradient(135deg, #131c31 0%, #1c2147 50%, #111827 100%);
    color: var(--text-light);
}

.stApp header {
    background: linear-gradient(90deg, #111827, #1f2937);
    color: var(--text-light);
    border-bottom: 1px solid rgba(99, 102, 241, 0.35);
}

.css-1d391kg, .css-12oz5g7, .css-1adrfps, .stTextInput label, .stTextArea label {
    color: var(--text-light);
}

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(8px);
    border-right: 1px solid rgba(148, 163, 184, 0.2);
}

.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: rgba(15, 23, 42, 0.4);
    color: var(--text-light);
    border: 1px solid rgba(226, 232, 240, 0.3);
    border-radius: 12px;
}

.stButton>button {
    background: linear-gradient(120deg, #facc15, #f97316);
    color: #0f172a;
    border: none;
    border-radius: 999px;
    padding: 0.65rem 1.4rem;
    font-weight: 600;
    box-shadow: 0 12px 24px rgba(249, 115, 22, 0.35);
}

.stButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 20px 35px rgba(249, 115, 22, 0.45);
}

.verdict-card {
    border-radius: 18px;
    padding: 1.5rem;
    background: rgba(15, 23, 42, 0.6);
    box-shadow: 0 20px 45px rgba(15, 23, 42, 0.35);
    border: 1px solid rgba(148, 163, 184, 0.2);
}

.stExpander {
    background: rgba(15, 23, 42, 0.4) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
}

/* Light Theme adjustments */
@media (prefers-color-scheme: light) {
    .stApp {
        background: linear-gradient(135deg, #f8fafc, #e0e7ff, #fdf2f8);
        color: var(--text-dark);
    }
    section[data-testid="stSidebar"] {
        background: rgba(241, 245, 249, 0.8);
        color: var(--text-dark);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.8);
        color: var(--text-dark);
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    .stButton>button {
        color: var(--text-light);
    }
    .verdict-card {
        background: rgba(255, 255, 255, 0.9);
    }
}
</style>
"""

NAV_LINKS = {
    "Home": "#home",
    "About": "#about",
    "Help": "#help",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _format_confidence(confidence: Optional[float]) -> str:
    if confidence is None:
        return "—"
    return f"{confidence * 100:.1f}%"


def _build_payload(claim_text: str, claim_url: str) -> Dict[str, Any]:
    if claim_url:
        return {"url": claim_url}
    return {"text": claim_text}


def _call_backend(payload: Dict[str, Any]) -> Dict[str, Any]:
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


def _render_provider_results(providers: List[Dict[str, Any]]) -> None:
    if not providers:
        st.write("No third-party sources were returned.")
        return

    for pr in providers:
        provider_name = pr.get("provider", "source").replace("_", " ").title()
        verdict = pr.get("verdict", "unknown").title()
        rating = pr.get("rating")
        title = pr.get("title") or pr.get("summary")
        source_url = pr.get("source_url")

        with st.container():
            st.markdown(f"**{provider_name}** — {verdict}")
            if rating:
                st.caption(rating)
            if title:
                st.write(title)
            if source_url:
                st.markdown(f"[Read source]({source_url})")
            st.divider()


def _render_sources_from_explanation(explanation: str) -> None:
    """
    The backend appends a Sources: block with bullet list.
    Parse it and render as list items with links when present.
    """
    if "Sources:" not in explanation:
        return
    _, sources_block = explanation.split("Sources:", maxsplit=1)
    lines = [line.strip("- ").strip() for line in sources_block.splitlines() if line.strip()]
    if not lines:
        return
    st.subheader("Sources")
    for line in lines:
        if "|" in line:
            parts = [part.strip() for part in line.split("|")]
            source_text = " | ".join(parts[:-1]) if parts[-1].startswith("http") else line
            if parts[-1].startswith("http"):
                st.markdown(f"- {source_text} | [Link]({parts[-1]})")
            else:
                st.markdown(f"- {line}")
        else:
            st.markdown(f"- {line}")


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="FactScreen",
    page_icon="✅",
    layout="wide",
)
st.markdown(THEME_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        "<div style='font-size:2rem;font-weight:700;'>FactScreen</div>",
        unsafe_allow_html=True,
    )
    st.caption("AI-assisted fact verification")
    st.divider()
    for label, href in NAV_LINKS.items():
        st.markdown(f"[{label}]({href})")
    st.divider()
    st.markdown(
        """
        **Usage Tips**
        - Enter a short claim or paste a URL.
        - Click **Verify Claim** and wait while we check multiple sources.
        - Expand **Explainability** for LLM reasoning & citations.
        """
    )

st.title("FactScreen Claim Verification")
st.markdown(
    "Enter a claim or URL below. We will cross-reference multiple fact-checkers "
    "and provide a verdict with Gemini-backed explanations."
)

with st.form("claim_form"):
    claim_text = st.text_area("Claim", placeholder="e.g., The sun rises in the west", height=120)
    claim_url = st.text_input("URL (optional)", placeholder="https://example.com/article")
    col_submit, col_reset = st.columns([2, 1])
    with col_submit:
        submitted = st.form_submit_button("Verify Claim", use_container_width=True)
    with col_reset:
        cleared = st.form_submit_button("Clear", use_container_width=True)

    if cleared:
        st.rerun()

if submitted:
    if not claim_text.strip() and not claim_url.strip():
        st.error("Input cannot be empty. Enter a claim or URL.")
    else:
        payload = _build_payload(claim_text.strip(), claim_url.strip())
        with st.spinner("Processing claim..."):
            try:
                response = _call_backend(payload)
            except RuntimeError as exc:
                st.error(str(exc))
            else:
                result = response.get("result", {})
                verdict = (result.get("verdict") or "unknown").lower()
                verdict_color = VERDICT_COLORS.get(verdict, "#607D8B")
                confidence = result.get("confidence")
                explanation = result.get("explanation", "No explanation provided.")
                provider_results = result.get("provider_results", [])

                st.markdown("### Verdict")
                verdict_text = verdict.replace("_", " ").title()
                st.markdown(
                    f"""
                    <div class="verdict-card">
                        <div style="font-size:1.1rem;color:{verdict_color};text-transform:uppercase;">
                            Verdict
                        </div>
                        <div style="font-size:2rem;font-weight:700;">{verdict_text}</div>
                        <div style="opacity:0.85;">Confidence: {_format_confidence(confidence)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("### Supporting Evidence")
                _render_provider_results(provider_results)

                with st.expander("Explainability"):
                    main_text = explanation.split("Sources:")[0].strip()
                    st.write(main_text)
                    _render_sources_from_explanation(explanation)

