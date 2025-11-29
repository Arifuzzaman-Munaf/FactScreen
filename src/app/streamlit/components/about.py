"""
About Page Component for the Streamlit Frontend

This module defines the rendering logic for the About page in the FactScreen Streamlit
application. It presents a formal overview of the FactScreen system, including its
purpose, objectives, and core technology stack.

Component Responsibilities:
    - Display product mission and value proposition.
    - Summarize primary objectives and outcomes.
    - Outline the technical architecture and integrated AI models and services.
"""

import streamlit as st


def render_about_page() -> None:
    """
    Renders the About page with formal documentation of system overview, product objectives,
    and technology stack.

    The function orchestrates the layout and content of the About page by utilizing Streamlit's
    markdown rendering capability, providing a structured description of FactScreen's mission,
    functionality, and core technologies.

    Content Sections:
        1. Page Title
        2. Product Introduction
        3. Purpose Rationale
        4. Feature Highlights (two-column)
        5. Primary Objectives
        6. Technology Stack
    """

    # Section 1: Page Title (Styled as hero)
    st.markdown(
        """
        <div class="hero-title">
            About FactScreen
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section 2: Product Introduction (Formal summary)
    st.markdown(
        """
        <div class="hero-subtitle" style="max-width:900px;margin:0 auto 2rem auto;">
            FactScreen is an advanced artificial intelligence (AI) companion designed to proactively
            address misinformation through rapid fact verification, transparent evidence citation,
            and concise narrative explanations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section 3: Purpose Rationale (Overview of system purpose)
    st.markdown(
        """
        <div class="content-card">
            <h2>Purpose and System Overview</h2>
            <p>
                <strong>FactScreen</strong> integrates authoritative third-party fact-checker feeds
                evidence retrieval, verdict computation, and explanatory
                Users may submit a statement or URL, after which the platform coordinates automated
                manual fact-checking workflows.
                the need for manual research.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section 4: Feature Highlights - Split into two columns
    col1, col2 = st.columns(2, gap="large")

    with col1:
        # Real-time fact-checking feature highlights
        st.markdown(
            """
            <div class="content-card">
                <h2>Real-Time Fact-Checking</h2>
                <ul>
                    <li>Multi-source fact-checking pipelines augmented
                    with semantic relevance filtering.</li>
                    <li>Immediate verdict presentation, including
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        # Explainable AI features
        st.markdown(
            """
            <div class="content-card">
                <h2>Transparent and Explainable AI</h2>
                <ul>
                    <li>Employs Gemini 2.5 Flash to concisely
                    articulate the reasoning behind each verdict.</li>
                    <li>Displays comprehensive source tables,
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Section 5: Primary Objectives (Formal enumeration of goals)
    st.markdown(
        """
        <div class="content-card">
            <h2>Primary Objectives</h2>
            <p>FactScreen is engineered to achieve the following outcomes:</p>
            <ul>
                <li>
                    <strong>Automated Verification:</strong>
                    Enable instant identification and classification of factual claims.
                </li>
                <li>
                    <strong>Trust Enhancement:</strong>
                    Facilitate evidence-backed, narrative explanations
                </li>
                <li>
                    <strong>Accessibility:</strong>
                    Deliver a seamless, intuitive single-page
                </li>
                <li>
                    <strong>Accuracy:</strong>
                    Leverage multi-source data validation and
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section 6: Technology Stack (Formal, detailed technical components)
    st.markdown(
        """
        <div class="content-card">
            <h2>Core Technology Stack</h2>
            <p>
                FactScreen operates atop a modular, asynchronous
                cutting-edge machine learning and LLMs. The key components are:
            </p>
            <ul>
                <li>
                    <strong>Data Sourcing & Integration:</strong>
                    Aggregates and standardizes fact-check records
                    collected from multiple authoritative external APIs,
                </li>
                <li>
                    <strong>Semantic Filtering:</strong>
                    Utilizes the <strong><code>all-MiniLM-L6-v2</code>
                    scores, filtering records for high relevance to the user's query.
                </li>
                <li>
                    <strong>AI Classification:</strong>
                    Applies the <strong><code>facebook/bart-large-mnli
                    final verdict labels for each claim.
                </li>
                <li>
                    <strong>Explainability Service:</strong>
                    Implements <strong>Gemini 2.5 Flash</strong> LLM
                    explanations and evidence-based summaries supporting each verdict.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
