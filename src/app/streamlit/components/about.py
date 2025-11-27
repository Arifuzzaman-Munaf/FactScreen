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

