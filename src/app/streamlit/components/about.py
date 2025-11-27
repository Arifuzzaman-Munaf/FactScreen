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
            ℹ️ About FactScreen
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Product Name & Purpose</h2>
            <p><strong>FactScreen: AI-Powered Fake News and Misinformation Classification System.</strong></p>
            <p>FactScreen is a standalone, web-based application designed to combat the rapid spread of false or misleading digital information. It functions as a core verification engine for classifying and explaining the authenticity of claims extracted from text and URLs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Primary Objectives</h2>
            <p>The system's architecture is structured to deliver four core goals:</p>
            <ul>
                <li><strong>Automate Verification:</strong> Identify and verify online claims in real-time.</li>
                <li><strong>Improve Trust:</strong> Provide transparency through evidence-driven, explainable summary reports.</li>
                <li><strong>Accessibility:</strong> Support public digital literacy by providing an accessible, web-based verification tool.</li>
                <li><strong>Accuracy:</strong> Maintain high precision through multi-source verification and advanced Natural Language Processing (NLP).</li>
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
    
    st.markdown(
        """
        <div class="content-card">
            <h2>Project Details</h2>
            <p><strong>Version:</strong> 1.0</p>
            <p><strong>Prepared by:</strong> Md. Arifuzzaman Munaf</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

