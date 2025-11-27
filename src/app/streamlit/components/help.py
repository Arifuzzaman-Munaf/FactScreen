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

