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

import streamlit as st

from src.app.streamlit.config import VERDICT_COLORS
from src.app.streamlit.helpers import (
    build_payload,
    call_backend,
    format_confidence,
    render_provider_results,
    render_sources_from_explanation,
    scroll_to_element,
)


def render_home_page() -> None:
    """
    Render the main home page with claim verification functionality.
    
    This function displays the hero section, claim input form, processing
    indicator, and results (verdict, evidence, explanation).
    """
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
    
    with st.form("claim_form", clear_on_submit=False):
        claim_text = st.text_area(
            "Claim", 
            placeholder="e.g., The sun rises in the west", 
            height=120,
            value=st.session_state.get("claim_text", ""),
            key="claim_text_input"
        )
        claim_url = st.text_input(
            "URL (optional)", 
            placeholder="https://example.com/article",
            value=st.session_state.get("claim_url", ""),
            key="claim_url_input"
        )
        col_submit, col_reset = st.columns([2, 1], gap="medium")
        with col_submit:
            submitted = st.form_submit_button("🔍 Verify Claim", use_container_width=True, type="primary")
        with col_reset:
            cleared = st.form_submit_button("🗑️ Clear", use_container_width=True, type="secondary")

        if cleared:
            st.session_state.claim_text = ""
            st.session_state.claim_url = ""
            st.rerun()

    if submitted:
        if not claim_text.strip() and not claim_url.strip():
            st.error("Input cannot be empty. Enter a claim or URL.")
        else:
            payload = build_payload(claim_text.strip(), claim_url.strip())
            # Create placeholder for custom processing indicator
            processing_placeholder = st.empty()
            
            # Show cool processing animation with ID for scrolling
            processing_placeholder.markdown(
                """
                <div id="processing-indicator" class="processing-container">
                    <div class="processing-loader"></div>
                    <div class="processing-dots">
                        <div class="processing-dot"></div>
                        <div class="processing-dot"></div>
                        <div class="processing-dot"></div>
                    </div>
                    <div class="processing-text">Analyzing Claim</div>
                    <div class="processing-steps">Cross-referencing fact-checkers • AI classification • Generating explanation</div>
                </div>
                <script>
                    // Scroll to processing card when it becomes visible
                    function scrollToProcessingCard() {
                        const card = document.getElementById('processing-indicator');
                        if (card) {
                            card.scrollIntoView({
                                behavior: 'smooth',
                                block: 'center',
                                inline: 'nearest'
                            });
                            return true;
                        }
                        return false;
                    }
                    
                    // Try immediately
                    if (!scrollToProcessingCard()) {
                        // Retry when element appears
                        const observer = new MutationObserver(() => {
                            if (scrollToProcessingCard()) {
                                observer.disconnect();
                            }
                        });
                        observer.observe(document.body, { childList: true, subtree: true });
                        
                        // Also try with timeouts
                        setTimeout(scrollToProcessingCard, 100);
                        setTimeout(scrollToProcessingCard, 300);
                        setTimeout(() => observer.disconnect(), 2000);
                    }
                </script>
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

                # Determine verdict class for styling
                verdict_class = "unknown"
                if verdict == "true":
                    verdict_class = "true"
                elif verdict in ["misleading", "false"]:
                    verdict_class = "misleading"
                
                verdict_text = verdict.replace("_", " ").title()
                # Render verdict with scroll script
                st.markdown(
                    f"""
                    <div id="verdict-result" class="verdict-section verdict-{verdict_class}">
                        <div class="verdict-label">Verdict</div>
                        <div class="verdict-text">{verdict_text}</div>
                        <div class="verdict-confidence">Confidence: {format_confidence(confidence)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                # Scroll to verdict after rendering
                scroll_to_element("verdict-result", delay=200)

                st.markdown(
                    """
                    <div style="margin-top: 2rem;">
                        <h3 style="color: rgba(248, 250, 252, 0.95); font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">
                            📚 Supporting Evidence
                        </h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                render_provider_results(provider_results)

                with st.expander("📊 Explainability & Detailed Analysis", expanded=False):
                    main_text = explanation.split("Sources:")[0].strip()
                    st.markdown(
                        f"""
                        <div style="color: rgba(248, 250, 252, 0.9); line-height: 1.8; font-size: 1.05rem;">
                            {main_text}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    render_sources_from_explanation(explanation)

