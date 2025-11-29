"""
Help page component for the Streamlit frontend.

This module contains the Help page rendering logic, providing
user documentation, troubleshooting guides, and usage instructions.
"""

import streamlit as st


def render_help_page() -> None:
    """
    Render the Help page with getting started and troubleshooting information.

    This function displays usage instructions, verdict explanations,
    and error recovery guidance.
    """
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
        <div class="hero-subtitle" style="max-width:900px;margin:0 auto 2rem auto;">
            Quick walkthroughs, verdict definitions, and safety nets—everything you need to feel confident while using FactScreen.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="content-card">
            <h2>How to Verify a Claim</h2>
            <ol>
                <li><strong>Paste or type a claim:</strong> Anything from a viral headline to a rumor you heard.</li>
                <li><strong>Select “Verify Claim”:</strong> FactScreen queues up fact-checker APIs and AI analysis.</li>
                <li><strong>Watch the processing overlay:</strong> The animation confirms every stage is running.</li>
                <li><strong>Read the verdict card:</strong> Confidence, reasoning, and supporting evidence appear simultaneously.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            """
            <div class="content-card">
                <h2>When to Use FactScreen</h2>
                <ul>
                    <li>Before sharing a breaking-news claim.</li>
                    <li>While preparing editorial content or reports.</li>
                    <li>During classroom or newsroom fact-checking drills.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="content-card">
                <h2>Need Assistance?</h2>
                <ul>
                    <li>Use the “Clear” button to start a fresh verification.</li>
                    <li>Contact <strong><i>arifuzzamanmunaf@gmail.com</i></strong> for workflow guidance.</li>
                    <li>Report suspicious results via the GitHub issues template.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="content-card">
            <h2>Understanding the Verdict</h2>
            <p>The AI classifier provides one of three clear, normalized labels for all processed claims:</p>
            <table style="width:100%;border-collapse:collapse;margin-top:1rem;">
                <thead>
                    <tr style="background:rgba(99,102,241,0.2);">
                        <th style="padding:0.75rem;text-align:left;border:1px solid rgba(99,102,241,0.3);">Verdict Label</th>
                        <th style="padding:0.75rem;text-align:left;border:1px solid rgba(99,102,241,0.3);">Visual Indicator</th>
                        <th style="padding:0.75rem;text-align:left;border:1px solid rgba(99,102,241,0.3);">Meaning (Classification)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>True</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#22c55e;font-weight:bold;">Green</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">The claim is accurate, verified, or supported by authoritative evidence.</td>
                    </tr>
                    <tr style="background:rgba(15,23,42,0.3);">
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>False or Misleading</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#ef4444;font-weight:bold;">Red</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">The claim is incorrect, debunked, or contains inaccurate information.</td>
                    </tr>
                    <tr>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>Not enough information found</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#eab308;font-weight:bold;">Yellow</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">There is insufficient, unclear, or conflicting evidence from external sources to confirm or refute the claim.</td>
                    </tr>
                    <tr style="background:rgba(15,23,42,0.3);">
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>Explainability Panel</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#8b5cf6;font-weight:bold;">Expandable</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">Click to view the generated summary and reasoning provided by the <strong>Gemini 2.5 Flash LLM</strong>.</td>
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
            <h2>Troubleshooting and Fail-Safe Mechanisms</h2>
            <p>The system employs a <strong>Fail-Safe Design</strong> to ensure continuous operation and reliability.</p>
            <ul>
                <li><strong>API Timeouts:</strong> All external fact-checking API requests are subject to a maximum <strong>15-second timeout</strong>. If exceeded, the system immediately displays a <strong>System Error</strong> screen.</li>
                <li><strong>System Error Recovery:</strong> If the server encounters an unhandled exception or network failure, the <strong>System Error UI</strong> provides a plain-language diagnosis and a constructive solution (the <strong>"Try Again"</strong> button).</li>
                <li><strong>External API Fallback:</strong> If both external fact-checking APIs are unavailable, the backend automatically executes the <strong>Gemini 2.5 Flash LLM</strong> to determine a classification and explanation <strong>without external evidence</strong> .</li>
                <li><strong>AI Disclaimer:</strong> All AI-generated outputs include a disclaimer clarifying that the results are probabilistic and are <strong>not legally binding</strong> .</li>
                <li><strong>Input Validation:</strong> The UI actively prevents form submission if the input field is empty, displaying an error message like <strong>"Input cannot be empty"</strong> to prevent a client-side crash.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
