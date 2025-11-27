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

import pandas as pd
import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_API_URL = "http://localhost:8000"
API_BASE_URL = os.getenv("FACTSCREEN_API_URL", DEFAULT_API_URL).rstrip("/")
VALIDATION_ENDPOINT = f"{API_BASE_URL}/v1/validate"

VERDICT_COLORS = {
    "true": "#22c55e",  # green
    "misleading": "#ef4444",  # red
    "unknown": "#eab308",  # yellow
    "false": "#ef4444",  # red (alias for misleading)
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
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #2d1b3d 50%, #1a1f3a 75%, #0a0e27 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: var(--text-light);
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp header {
    background: linear-gradient(90deg, #111827, #1f2937, #2d1b3d);
    color: var(--text-light);
    border-bottom: 2px solid rgba(99, 102, 241, 0.5);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.css-1d391kg, .css-12oz5g7, .css-1adrfps, .stTextInput label, .stTextArea label {
    color: var(--text-light);
}

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(148, 163, 184, 0.3);
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.2);
}

.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: rgba(15, 23, 42, 0.6);
    color: var(--text-light);
    border: 2px solid rgba(99, 102, 241, 0.4);
    border-radius: 12px;
    transition: all 0.3s ease;
}

.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: rgba(99, 102, 241, 0.8);
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
}

.stButton>button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
    background-size: 200% 200%;
    animation: buttonGradient 3s ease infinite;
    color: #ffffff;
    border: none;
    border-radius: 999px;
    padding: 0.75rem 1.6rem;
    font-weight: 700;
    font-size: 1rem;
    box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4);
    transition: all 0.3s ease;
}

@keyframes buttonGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stButton>button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.6);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899, #f59e0b);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleGradient 5s ease infinite;
    text-align: center;
    margin: 2rem 0;
    line-height: 1.2;
    text-shadow: 0 0 40px rgba(99, 102, 241, 0.5);
}

@keyframes titleGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-subtitle {
    font-size: 1.3rem;
    text-align: center;
    color: rgba(248, 250, 252, 0.8);
    margin-bottom: 3rem;
    font-weight: 300;
}

.content-card {
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
    border: 1px solid rgba(99, 102, 241, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.verdict-section {
    width: 100%;
    padding: 2.5rem 2rem;
    margin: 1.5rem 0;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    animation: verdictPulse 2s ease-in-out infinite;
}

@keyframes verdictPulse {
    0%, 100% { box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); }
    50% { box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4); }
}

.verdict-true {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: #ffffff;
}

.verdict-misleading, .verdict-false {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: #ffffff;
}

.verdict-unknown {
    background: linear-gradient(135deg, #eab308, #ca8a04);
    color: #ffffff;
}

.verdict-label {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}

.verdict-text {
    font-size: 3rem;
    font-weight: 700;
    margin: 0.5rem 0;
}

.verdict-confidence {
    font-size: 1.1rem;
    opacity: 0.95;
    margin-top: 0.5rem;
}

.stExpander {
    background: rgba(15, 23, 42, 0.5) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
}

h1, h2, h3 {
    color: var(--text-light) !important;
}

/* Light Theme adjustments */
@media (prefers-color-scheme: light) {
    .stApp {
        background: linear-gradient(135deg, #f8fafc, #e0e7ff, #fdf2f8, #e0e7ff, #f8fafc);
        background-size: 400% 400%;
        color: var(--text-dark);
    }
    section[data-testid="stSidebar"] {
        background: rgba(241, 245, 249, 0.9);
        color: var(--text-dark);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.9);
        color: var(--text-dark);
        border: 2px solid rgba(148, 163, 184, 0.4);
    }
    .stButton>button {
        color: #ffffff;
    }
    .hero-title {
        -webkit-text-fill-color: #0f172a;
    }
    .hero-subtitle {
        color: rgba(15, 23, 42, 0.7);
    }
    .content-card {
        background: rgba(255, 255, 255, 0.9);
        color: var(--text-dark);
    }
    h1, h2, h3 {
        color: var(--text-dark) !important;
    }
}
</style>
"""

# Navigation state
if "page" not in st.session_state:
    st.session_state.page = "home"


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
        st.info("No third-party sources were returned.")
        return

    # Prepare table data with deduplication
    # Deduplicate based on verdict, rating, and summary (same content = duplicate)
    seen_verdicts = {}  # key: (verdict, rating, summary_normalized) -> row_data
    
    for pr in providers:
        verdict = pr.get("verdict", "unknown").title()
        rating = pr.get("rating", "N/A")
        title = pr.get("title") or pr.get("summary") or "No title available"
        source_url = pr.get("source_url") or ""
        
        # Normalize summary for deduplication (lowercase, strip whitespace)
        summary_normalized = title.lower().strip()
        
        # Create a key for deduplication based on verdict, rating, and summary
        dedup_key = (verdict, str(rating), summary_normalized)
        
        # Truncate long titles for table display
        display_title = title[:97] + "..." if len(title) > 100 else title
        
        # Format source URL
        if source_url and source_url.startswith("http"):
            source_value = source_url
        else:
            source_value = "N/A"
        
        if dedup_key not in seen_verdicts:
            # First occurrence - store the data
            seen_verdicts[dedup_key] = {
                "Verdict": verdict,
                "Rating": str(rating),
                "Summary": display_title,
                "Source": source_value
            }
        else:
            # Duplicate found - keep first occurrence (already stored)
            # If this one has a valid URL and the stored one doesn't, update it
            existing = seen_verdicts[dedup_key]
            if source_value != "N/A" and existing["Source"] == "N/A":
                existing["Source"] = source_value
    
    # Convert to list for DataFrame
    table_data = list(seen_verdicts.values())
    
    if not table_data:
        st.info("No third-party sources were returned.")
        return
    
    # Display as table
    df = pd.DataFrame(table_data)
    
    # Check if we have any valid URLs
    has_urls = any(row["Source"] != "N/A" and row["Source"].startswith("http") for row in table_data)
    
    # Build column config (no Provider column)
    column_config = {
        "Verdict": st.column_config.TextColumn("Verdict", width="small"),
        "Rating": st.column_config.TextColumn("Rating", width="small"),
        "Summary": st.column_config.TextColumn("Summary", width="large"),
    }
    
    if has_urls:
        column_config["Source"] = st.column_config.LinkColumn(
            "Source",
            width="medium",
            display_text="🔗 View"
        )
    else:
        column_config["Source"] = st.column_config.TextColumn("Source", width="medium")
    
    # Style the table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )


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
# Page Rendering Functions
# ---------------------------------------------------------------------------
def _render_home_page():
    """Render the main home page with claim verification."""
    st.markdown(
        """
        <div class="hero-title">
            Combat Misinformation with AI-Powered Fact Verification
        </div>
        <div class="hero-subtitle">
            Instantly verify claims, detect fake news, and get evidence-backed explanations
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    with st.form("claim_form"):
        claim_text = st.text_area("Claim", placeholder="e.g., The sun rises in the west", height=120)
        claim_url = st.text_input("URL (optional)", placeholder="https://example.com/article")
        col_submit, col_reset = st.columns([2, 1])
        with col_submit:
            submitted = st.form_submit_button("🔍 Verify Claim", use_container_width=True)
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

                    # Determine verdict class for styling
                    verdict_class = "unknown"
                    if verdict == "true":
                        verdict_class = "true"
                    elif verdict in ["misleading", "false"]:
                        verdict_class = "misleading"
                    
                    verdict_text = verdict.replace("_", " ").title()
                    st.markdown(
                        f"""
                        <div class="verdict-section verdict-{verdict_class}">
                            <div class="verdict-label">Verdict</div>
                            <div class="verdict-text">{verdict_text}</div>
                            <div class="verdict-confidence">Confidence: {_format_confidence(confidence)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown("### Supporting Evidence")
                    _render_provider_results(provider_results)

                    with st.expander("📊 Explainability"):
                        main_text = explanation.split("Sources:")[0].strip()
                        st.write(main_text)
                        _render_sources_from_explanation(explanation)


def _render_about_page():
    """Render the About page with system overview and technology."""
    st.markdown(
        """
        <div class="hero-title">
            About FactScreen
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Product Information</h2>
            <p><strong>Product Name:</strong> FactScreen: AI-Powered Fake News and Misinformation Classification System</p>
            <p><strong>Version:</strong> 1.0 (API Name: FactScreen API)</p>
            <p><strong>Prepared By:</strong> Md. Arifuzzaman Munaf (Torrens University)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Our Purpose</h2>
            <p>FactScreen is a standalone, web-based application designed to combat the rapid spread of false or misleading digital information. It automates the detection, verification, and explanation of misinformation circulating online.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Primary Objectives</h2>
            <p>Our system is built to achieve the following goals:</p>
            <ul>
                <li><strong>Automate Verification:</strong> Identify and verify online claims in real-time</li>
                <li><strong>Improve Trust:</strong> Provide transparency through evidence-driven, explainable summary reports</li>
                <li><strong>Reduce Workload:</strong> Reduce manual fact-checking effort for journalists and moderators</li>
                <li><strong>Support Literacy:</strong> Provide an accessible tool to support public digital literacy</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>How It Works (Technology)</h2>
            <p>FactScreen employs a modern, multi-layered architecture that uses the following core technologies for classification and reasoning:</p>
            <ul>
                <li><strong>Source Integration (Data Layer):</strong> Aggregates data from multiple external authoritative fact-checking repositories, including the <strong>Google Fact Check Tool</strong> and the <strong>RapidAPI Fact-Checker</strong></li>
                <li><strong>Filtering & Classification (AI/ML):</strong> Uses the <strong><code>all-MiniLM-L6-v2</code></strong> model for semantic similarity filtering, and the <strong><code>facebook/bart-large-mnli</code></strong> model for final claim classification</li>
                <li><strong>Explainability (LLM):</strong> Employs the <strong>Gemini 2.5 Flash</strong> Large Language Model (LLM) to generate human-readable explanations and reasoning summaries for the final verdict</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_help_page():
    """Render the Help page with getting started and troubleshooting."""
    st.markdown(
        """
        <div class="hero-title">
            Help & Documentation
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>How to Verify a Claim</h2>
            <p>To get a classified verdict, enter the information you want to check into the input box on the Home page.</p>
            <ol>
                <li><strong>Enter Claim:</strong> Type or paste a claim or URL into the <strong>Input Section</strong></li>
                <li><strong>Start Verification:</strong> Click the <strong>"Verify Claim"</strong> button</li>
                <li><strong>Wait for Processing:</strong> A <strong>"Processing..."</strong> indicator will display while the system simultaneously retrieves external evidence, filters results by semantic similarity, and performs the AI classification</li>
                <li><strong>View Verdict:</strong> The <strong>Results Panel</strong> will update with the final verdict and classification</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Understanding the Verdict</h2>
            <p>The system provides one of three consistent, normalized classification labels:</p>
            <table style="width:100%;border-collapse:collapse;margin-top:1rem;">
                <thead>
                    <tr style="background:rgba(99,102,241,0.2);">
                        <th style="padding:0.75rem;text-align:left;border:1px solid rgba(99,102,241,0.3);">Verdict Label</th>
                        <th style="padding:0.75rem;text-align:left;border:1px solid rgba(99,102,241,0.3);">Color Code</th>
                        <th style="padding:0.75rem;text-align:left;border:1px solid rgba(99,102,241,0.3);">Meaning</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>True</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#22c55e;font-weight:bold;">Green</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">The claim is accurate, verified, or supported by evidence.</td>
                    </tr>
                    <tr style="background:rgba(15,23,42,0.3);">
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>False or Misleading</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#ef4444;font-weight:bold;">Red</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">The claim is incorrect, debunked, or contains misleading information.</td>
                    </tr>
                    <tr>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>Not enough information found</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#eab308;font-weight:bold;">Yellow</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">There is insufficient, unclear, or conflicting information to confidently determine the claim's veracity.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Accessing the Explanation and Evidence</h2>
            <p>For maximum transparency, every result includes an <strong>Explainability Panel</strong>.</p>
            <ul>
                <li><strong>How to View:</strong> Click the expandable area (e.g., "Show Explanation") on the <strong>Results Panel</strong></li>
                <li><strong>What it Contains:</strong> The panel displays a text summary and reasoning provided by the <strong>Gemini 2.5 Flash</strong> LLM, detailing the evidence and logic used to arrive at the classification verdict</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Troubleshooting and Error Recovery</h2>
            <p>The system is designed with explicit error recovery strategies to help users recover from errors.</p>
            <ul>
                <li><strong>System Error:</strong> If the backend or external services (Google/RapidAPI) fail or experience a timeout (maximum 15 seconds), the <strong>System Error UI</strong> will display. Click the <strong>"Try Again"</strong> button to re-send the request.</li>
                <li><strong>External API Fallback:</strong> If the external fact-checking APIs are unreachable, the system will attempt to use the <strong>Gemini 2.5 Flash</strong> LLM to determine a classification <strong>without external evidence</strong>. This is indicated by a confidence note or disclaimer on the verdict.</li>
                <li><strong>Invalid Input:</strong> If the input field is empty, the system will prevent the search and display an inline message like <strong>"Input cannot be empty"</strong>.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="FactScreen",
    page_icon="✅",
    layout="wide",
)
st.markdown(THEME_CSS, unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown(
        "<div style='font-size:2.5rem;font-weight:900;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>FactScreen</div>",
        unsafe_allow_html=True,
    )
    st.caption("AI-Powered Fake News and Misinformation Classification System")
    st.divider()
    
    # Navigation buttons
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.page == "home" else "secondary"):
        st.session_state.page = "home"
        st.rerun()
    if st.button("ℹ️ About", use_container_width=True, type="primary" if st.session_state.page == "about" else "secondary"):
        st.session_state.page = "about"
        st.rerun()
    if st.button("❓ Help", use_container_width=True, type="primary" if st.session_state.page == "help" else "secondary"):
        st.session_state.page = "help"
        st.rerun()
    
    st.divider()
    st.markdown(
        """
        **Quick Tips**
        - Enter a claim or paste a URL
        - Click **Verify Claim** to check
        - View detailed explanations
        """
    )

# Page routing
if st.session_state.page == "about":
    _render_about_page()
elif st.session_state.page == "help":
    _render_help_page()
else:
    _render_home_page()

