"""
Main entry point for the Streamlit frontend application.

This module initializes the Streamlit application, sets up navigation,
and routes to the appropriate page components based on user selection.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path for cross-device compatibility
# This file is at: src/app/streamlit/main.py
# Project root is 3 levels up
_current_file = Path(__file__).resolve()
_project_root = _current_file.parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st

from src.app.streamlit.components import about, help, home
from src.app.streamlit.styles import THEME_CSS

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Configure page settings
st.set_page_config(
    page_title="FactScreen",
    page_icon="✅",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Apply custom styles
st.markdown(THEME_CSS, unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown(
        "<div style='font-size:2.5rem;font-weight:900;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>FactScreen</div>",
        unsafe_allow_html=True,
    )
    st.caption("AI-Powered Fake News and Misinformation Classification System")
    st.divider()
    
    # Navigation buttons
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.page == "home" else "secondary"):
        st.session_state.page = "home"
        st.rerun()
    if st.button("ℹ️ About", use_container_width=True, type="primary" if st.session_state.page == "about" else "secondary"):
        st.session_state.page = "about"
        st.rerun()
    if st.button("❓ Help", use_container_width=True, type="primary" if st.session_state.page == "help" else "secondary"):
        st.session_state.page = "help"
        st.rerun()
    
    st.divider()
    st.markdown(
        """
        **Quick Tips**
        - Enter a claim or paste a URL
        - Click **Verify Claim** to check
        - View detailed explanations
        """
    )

# Page routing
if st.session_state.page == "about":
    about.render_about_page()
elif st.session_state.page == "help":
    help.render_help_page()
else:
    home.render_home_page()

