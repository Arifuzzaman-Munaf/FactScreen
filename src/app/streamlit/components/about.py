"""
About page component for the Streamlit frontend.

This module contains the About page rendering logic, displaying
system overview, technology stack, and product information.
"""

import streamlit as st


def render_about_page() -> None:
    """
    Render the About page with system overview and technology information.
    
    This function displays product information, purpose, objectives,
    and technical architecture details.
    """
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
        <div class="hero-subtitle" style="max-width:900px;margin:0 auto 2rem auto;">
            FactScreen is a human-friendly AI companion that keeps misinformation in check with
            rapid verification, transparent evidence, and beautiful storytelling.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="content-card">
            <h2>Why FactScreen Exists</h2>
            <p><strong>FactScreen</strong> combines trusted fact-checker feeds with modern AI classification to help anyone validate a claim in seconds. Paste a statement or URL, and the platform orchestrates evidence gathering, verdict generation, and narrative explanations—no research rabbit holes required.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            """
            <div class="content-card">
                <h2>Real-time Defense</h2>
                <ul>
                    <li>Multisource fact-checking pipelines with relevance filtering.</li>
                    <li>Instant verdict card with animated confidence dial.</li>
                    <li>Session memory so teams can compare multiple claims quickly.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="content-card">
                <h2>Explainable AI</h2>
                <ul>
                    <li>Gemini 2.5 Flash summarizes why the verdict landed where it did.</li>
                    <li>Source tables highlight the third-party citations powering each label.</li>
                    <li>Design language mirrors the verdict colors to reinforce trust.</li>
                </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Primary Objectives</h2>
            <p>Everything inside FactScreen is optimized for four outcomes:</p>
            <ul>
                <li><strong>Automate Verification:</strong> Identify and classify claims in real time.</li>
                <li><strong>Improve Trust:</strong> Share evidence-backed stories instead of raw predictions.</li>
                <li><strong>Accessibility:</strong> A single-page interface that works on desktop or tablet.</li>
                <li><strong>Accuracy:</strong> Multi-source validation plus semantic filtering for relevance.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Core Technology Stack</h2>
            <p>FactScreen utilizes a multi-layered, asynchronous architecture built on FastAPI:</p>
            <ul>
                <li><strong>Data Sourcing & Integration:</strong> Aggregates and standardizes data retrieved from multiple authoritative external APIs, including the <strong>Google Fact Check Tool</strong> and the <strong>RapidAPI Fact-Checker</strong>.</li>
                <li><strong>Semantic Filtering:</strong> The <strong><code>all-MiniLM-L6-v2</code></strong> model calculates the semantic similarity score to retain only the most relevant records against the user query.</li>
                <li><strong>AI Classification:</strong> The <strong><code>facebook/bart-large-mnli</code></strong> transformer model is applied to predict the final verdict label.</li>
                <li><strong>Explainability Service:</strong> The <strong>Gemini 2.5 Flash</strong> Large Language Model (LLM) is used exclusively to generate the human-readable reasoning and evidence summaries for the verdict.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Project details card intentionally removed per latest design request.

