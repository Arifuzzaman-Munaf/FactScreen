"""
Help Page Component for the Streamlit Frontend.

This module provides the rendering logic for the FactScreen "Help & Documentation" page.
It includes user usage instructions, troubleshooting and safety information, and explanations
for verdict classification—allowing users to fully understand and navigate the app.

Component Responsibilities:
    - Deliver quickstart instructions for claim verification.
    - Explain when to use FactScreen and provide user support contacts.
    - Define verdict meaning and indicators in an accessible documentation table.
    - Document fail-safe design features and error handling instructions.
"""

import streamlit as st

def render_help_page() -> None:
    """
    Renders the Help & Documentation page with detailed instructions and explanations.

    This function guides users through the verification process,
    provides a legend for interpreting verdicts, and details troubleshooting and
    fail-safe measures for robust and reliable experience.
    """
    # Hero Title: Page Heading
    st.markdown(
        """
        <div class="hero-title">
            Help & Documentation
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero Subtitle: Concise summary line describing support scope
    st.markdown(
        """
        <div class="hero-subtitle" style="max-width:900px;margin:0 auto 2rem auto;">
            Quick walkthroughs, verdict definitions, and safety nets—everything you need to feel confident while using FactScreen.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # How-to Card: Step-by-step verification workflow
    st.markdown(
        """
        <div class="content-card">
            <h2>How to Verify a Claim</h2>
            <ol>
                <li><strong>Paste or type a claim:</strong> Enter anything from a viral headline to a rumor you heard.</li>
                <li><strong>Select “Verify Claim”:</strong> FactScreen will check trusted APIs and apply AI analysis for you.</li>
                <li><strong>Watch the processing overlay:</strong> The animation confirms each pipeline stage is running.</li>
                <li><strong>Read the verdict card:</strong> Results include confidence, explanations, and supporting sources.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Two column layout for contextual help
    col1, col2 = st.columns(2, gap="large")

    # Column 1: Appropriate usage scenarios for FactScreen
    with col1:
        st.markdown(
            """
            <div class="content-card">
                <h2>When to Use FactScreen</h2>
                <ul>
                    <li>Before sharing a breaking-news claim.</li>
                    <li>When preparing editorial content or reports.</li>
                    <li>During classroom or newsroom fact-checking drills.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    # Column 2: User support contact and assistance notes
    with col2:
        st.markdown(
            """
            <div class="content-card">
                <h2>Need Assistance?</h2>
                <ul>
                    <li>Use the “Clear” button to start a new verification.</li>
                    <li>Contact <strong><i>arifuzzamanmunaf@gmail.com</i></strong> for workflow support questions.</li>
                    <li>Report suspicious verdicts or errors through the GitHub issues template.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Verdict explanation table: How to interpret output colors and labels
    st.markdown(
        """
        <div class="content-card">
            <h2>Understanding the Verdict</h2>
            <p>The AI classifier provides one of three normalized verdicts for your claim:</p>
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
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">Claim is accurate: verified or supported by authoritative evidence.</td>
                    </tr>
                    <tr style="background:rgba(15,23,42,0.3);">
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>False or Misleading</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#ef4444;font-weight:bold;">Red</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">Claim is incorrect, debunked, or contains misleading information.</td>
                    </tr>
                    <tr>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>Not enough information found</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#eab308;font-weight:bold;">Yellow</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">Evidence from external sources is insufficient, unclear, or conflicting.</td>
                    </tr>
                    <tr style="background:rgba(15,23,42,0.3);">
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><strong>Explainability Panel</strong></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);"><span style="color:#8b5cf6;font-weight:bold;">Expandable</span></td>
                        <td style="padding:0.75rem;border:1px solid rgba(99,102,241,0.3);">Click to reveal a summary and reasoning generated by <strong>Gemini 2.5 Flash LLM</strong>.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Troubleshooting and fail-safe documentation
    st.markdown(
        """
        <div class="content-card">
            <h2>Troubleshooting and Fail-Safe Mechanisms</h2>
            <p>The system employs a <strong>Fail-Safe Design</strong> to ensure continuous operation and data integrity.</p>
            <ul>
                <li>
                    <strong>API Timeouts:</strong>
                    All external fact-checking APIs have a <strong>15-second timeout</strong>.
                    If a request exceeds this duration, a <strong>System Error</strong> screen is immediately displayed.
                </li>
                <li>
                    <strong>System Error Recovery:</strong>
                    In case of unhandled server errors or network outages,
                    the <strong>System Error UI</strong> displays a plain-language diagnosis and provides a
                    <strong>“Try Again”</strong> button to recover.
                </li>
                <li>
                    <strong>External API Fallback:</strong>
                    If both fact-checker APIs are unavailable, the backend executes
                    <strong>Gemini 2.5 Flash LLM</strong> to determine a verdict and explanation
                    <b>without external evidence</b>.
                </li>
                <li>
                    <strong>AI Disclaimer:</strong>
                    Every AI-generated result includes a warning that outputs are probabilistic and
                    <b>not legally binding</b>.
                </li>
                <li>
                    <strong>Input Validation:</strong>
                    The UI prevents submission if the input field is empty, showing an error such as
                    <strong>“Input cannot be empty”</strong> to prevent user-side crashes.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )