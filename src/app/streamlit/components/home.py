"""
Home page component for the Streamlit frontend.

This module contains the main home page rendering logic, including
the claim input form, processing indicator, and results display.
"""

import sys
from pathlib import Path

# Ensure project root is in path (in case this module is imported directly)
_current_file = Path(__file__).resolve()
_project_root = _current_file.parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from textwrap import dedent
import streamlit as st

from src.app.streamlit.config import VERDICT_COLORS
from src.app.streamlit.helpers import (
    build_payload,
    call_backend,
    download_pdf_report,
    format_confidence,
    render_provider_results,
    render_sources_from_explanation,
)

DEFAULT_VERDICT_CARD = dedent(
    """
<div id="verdict-result" class="verdict-card verdict-unknown placeholder">
    <div class="verdict-card-header">
        <span class="verdict-label">Verdict</span>
    </div>
    <div class="verdict-card-body">
        <div class="verdict-main-text">Submit a Claim</div>
        <p class="verdict-subtext">Insights appear here once you run a fact-check.</p>
        <div class="confidence-gauge" data-empty="true">
            <div class="confidence-center">
                <span>—</span>
                <small>Confidence</small>
            </div>
        </div>
    </div>
</div>
"""
).strip()

DEFAULT_EVIDENCE_HTML = dedent(
    """
<div class="source-table-placeholder">
    Provide a claim to see supporting evidence gathered from fact-checkers.
</div>
"""
).strip()

DEFAULT_EXPLANATION_HTML = dedent(
    """
<div class="explain-placeholder">
    Detailed explainability will be available after you verify a claim.
</div>
"""
).strip()


def render_home_page() -> None:
    """
    Render the main home page with claim verification functionality.

    This function displays the hero section, claim input form, processing
    indicator, and results (verdict, evidence, explanation).
    """
    if "verdict_card_html" not in st.session_state:
        st.session_state["verdict_card_html"] = DEFAULT_VERDICT_CARD
    if "evidence_table_html" not in st.session_state:
        st.session_state["evidence_table_html"] = DEFAULT_EVIDENCE_HTML
    if "explanation_html" not in st.session_state:
        st.session_state["explanation_html"] = DEFAULT_EXPLANATION_HTML
    if "clear_inputs" not in st.session_state:
        st.session_state["clear_inputs"] = False
    if "result_data" not in st.session_state:
        st.session_state["result_data"] = None
    if "pdf_generated" not in st.session_state:
        st.session_state["pdf_generated"] = False
    st.session_state.setdefault("claim_text_input", "")
    st.session_state.setdefault("claim_url_input", "")

    if st.session_state["clear_inputs"]:
        st.session_state["claim_text_input"] = ""
        st.session_state["claim_url_input"] = ""
        st.session_state["verdict_card_html"] = DEFAULT_VERDICT_CARD
        st.session_state["evidence_table_html"] = DEFAULT_EVIDENCE_HTML
        st.session_state["explanation_html"] = DEFAULT_EXPLANATION_HTML
        st.session_state["result_data"] = None
        st.session_state["pdf_bytes"] = None
        st.session_state["pdf_generated"] = False
        st.session_state["clear_inputs"] = False

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

    st.markdown('<div class="claim-verdict-row">', unsafe_allow_html=True)
    col_form, col_result = st.columns([1.15, 0.85], gap="large")

    with col_form:
        with st.form("claim_form", clear_on_submit=False):
            claim_text = st.text_area(
                "Claim",
                placeholder="e.g., The sun rises in the west",
                height=120,
                key="claim_text_input",
            )
            claim_url = st.text_input(
                "URL (optional)", placeholder="https://example.com/article", key="claim_url_input"
            )
            error_placeholder = st.empty()
            col_submit, col_reset = st.columns([2, 1], gap="medium")
            with col_submit:
                submitted = st.form_submit_button(
                    "Verify Claim", use_container_width=True, type="primary"
                )
            with col_reset:
                cleared = st.form_submit_button("Clear", use_container_width=True, type="secondary")

            if cleared:
                st.session_state["clear_inputs"] = True
                st.rerun()

    with col_result:
        verdict_display = st.empty()
        verdict_display.markdown(st.session_state["verdict_card_html"], unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-heading">
            <h3>Supporting Evidence</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    evidence_placeholder = st.empty()
    evidence_placeholder.markdown(st.session_state["evidence_table_html"], unsafe_allow_html=True)

    with st.expander("Explainability & Detailed Analysis", expanded=False):
        explanation_placeholder = st.empty()
        explanation_placeholder.markdown(
            st.session_state["explanation_html"], unsafe_allow_html=True
        )

    if submitted:
        if not claim_text.strip() and not claim_url.strip():
            error_placeholder.error("Input cannot be empty. Enter a claim or URL.")
        else:
            payload = build_payload(claim_text.strip(), claim_url.strip())
            # Create placeholder for custom processing indicator
            processing_placeholder = st.empty()

            # Show cool processing animation with ID for scrolling
            processing_placeholder.markdown(
                """
                <div class="processing-overlay">
                <div id="processing-indicator" class="processing-container">
                    <div class="processing-loader"></div>
                    <div class="processing-dots">
                        <div class="processing-dot"></div>
                        <div class="processing-dot"></div>
                        <div class="processing-dot"></div>
                    </div>
                        <div class="processing-text">Processing Claim</div>
                    <div class="processing-steps">Cross-referencing fact-checkers • AI classification • Generating explanation</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            try:
                # Make the API call
                response = call_backend(payload)
                processing_placeholder.empty()  # Clear the processing indicator
            except RuntimeError as exc:
                processing_placeholder.empty()  # Clear the processing indicator
                st.error(str(exc))
            else:
                result = response.get("result", {})
                verdict = (result.get("verdict") or "unknown").lower()
                confidence = result.get("confidence")
                explanation = result.get("explanation", "No explanation provided.")
                provider_results = result.get("provider_results", [])

                # Determine verdict class and supporting message
                verdict_class = "unknown"
                verdict_message = "AI review in progress. Provide more detail to begin."
                if verdict == "true":
                    verdict_class = "true"
                    verdict_message = "Evidence from fact-checkers supports this statement."
                elif verdict in ["misleading", "false"]:
                    verdict_class = "misleading"
                    verdict_message = "Cross-checked sources indicate this claim is not reliable."
                elif verdict == "unknown":
                    verdict_message = "We could not determine a verdict. Try refining the claim."

                verdict_text = verdict.replace("_", " ").title()
                # Render verdict with scroll script
                confidence_pct = confidence * 100 if confidence is not None else None
                confidence_display = format_confidence(confidence)
                confidence_html = (
                    dedent(
                        f"""
                    <div class="confidence-gauge" style="--confidence-value: {confidence_pct};">
                        <div class="confidence-center">
                            <span>{confidence_display}</span>
                            <small>Confidence</small>
                        </div>
                    </div>
                    """
                    ).strip()
                    if confidence_pct is not None
                    else dedent(
                        """
                    <div class="confidence-gauge" data-empty="true">
                        <div class="confidence-center">
                            <span>—</span>
                            <small>Confidence</small>
                        </div>
                    </div>
                    """
                    ).strip()
                )

                verdict_card_html = dedent(
                    f"""
                    <div id="verdict-result" class="verdict-card verdict-{verdict_class}">
                        <div class="verdict-card-header">
                            <span class="verdict-label">Verdict</span>
                        </div>
                        <div class="verdict-card-body">
                            <div class="verdict-main-text">{verdict_text}</div>
                            <p class="verdict-subtext">{verdict_message}</p>
                            {confidence_html}
                        </div>
                    </div>
                    """
                ).strip()
                st.session_state["verdict_card_html"] = verdict_card_html
                verdict_display.markdown(verdict_card_html, unsafe_allow_html=True)

                evidence_html = render_provider_results(provider_results)
                st.session_state["evidence_table_html"] = evidence_html
                evidence_placeholder.markdown(evidence_html, unsafe_allow_html=True)

                main_text = explanation.split("Sources:")[0].strip()
                sources_html = render_sources_from_explanation(explanation)
                explanation_html = dedent(
                    f"""
                    <div class="explain-text">
                        {main_text}
                    </div>
                    {sources_html}
                    """
                ).strip()
                st.session_state["explanation_html"] = explanation_html
                explanation_placeholder.markdown(explanation_html, unsafe_allow_html=True)

                # Store full result data for PDF generation
                st.session_state["result_data"] = result
                # Generate PDF in background (cache it for download)
                if not st.session_state.get("pdf_generated"):
                    try:
                        st.session_state["pdf_bytes"] = download_pdf_report(result)
                        st.session_state["pdf_generated"] = True
                    except RuntimeError:
                        # If PDF generation fails, don't block the UI
                        st.session_state["pdf_bytes"] = None
                        st.session_state["pdf_generated"] = True
                    
                    # Trigger rerun to show download button
                    st.rerun()

    # Download PDF button (only show if we have results) - positioned stunningly
    if st.session_state.get("result_data") and st.session_state.get("pdf_bytes"):
        st.markdown(
            """
            <div style="margin: 2rem 0;">
                <div class="section-heading" style="margin-bottom: 1rem;">
                    <h3>Export Report</h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Create a centered, prominent download button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            verdict = st.session_state["result_data"].get("verdict", "unknown")
            st.markdown(
                """
                <style>
                .stDownloadButton > button {
                    width: 100%;
                    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
                    color: white;
                    font-weight: 600;
                    font-size: 1.1rem;
                    padding: 1rem 2rem;
                    border-radius: 16px;
                    border: none;
                    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
                    transition: all 0.3s ease;
                }
                .stDownloadButton > button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.6);
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.download_button(
                label="📥 Download PDF Report",
                data=st.session_state["pdf_bytes"],
                file_name=f"factcheck-report-{verdict}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )
