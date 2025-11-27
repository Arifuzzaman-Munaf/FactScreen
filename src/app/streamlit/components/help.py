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
            ❓ Help & Documentation
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>How to Verify a Claim</h2>
            <ol>
                <li><strong>Enter Claim:</strong> Type or paste the claim text or URL you wish to verify into the input field on the Home page.</li>
                <li><strong>Start Verification:</strong> Click the <strong>"Verify Claim"</strong> button.</li>
                <li><strong>Wait for Processing:</strong> The <strong>"Processing..."</strong> indicator will display. The FastAPI backend is designed to return a classified verdict within <strong>5 seconds</strong> under normal conditions.</li>
                <li><strong>View Results:</strong> The <strong>Results Panel</strong> will update with the final verdict, confidence score, and supporting evidence.</li>
            </ol>
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
                <li><strong>External API Fallback:</strong> If both external fact-checking APIs are unavailable, the backend automatically executes the <strong>Gemini 2.5 Flash LLM</strong> to determine a classification and explanation <strong>without external evidence</strong> (Alternate Flow 1 in UC-04).</li>
                <li><strong>AI Disclaimer:</strong> All AI-generated outputs include a disclaimer clarifying that the results are probabilistic and are <strong>not legally binding</strong> (Business Rule BR-3).</li>
                <li><strong>Input Validation:</strong> The UI actively prevents form submission if the input field is empty, displaying an error message like <strong>"Input cannot be empty"</strong> to prevent a client-side crash.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

