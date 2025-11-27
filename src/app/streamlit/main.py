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
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Apply custom styles
st.markdown(THEME_CSS, unsafe_allow_html=True)

# Top Navigation Bar - Stunning Design with Logo
st.markdown(
    """
    <div class="top-navbar">
        <div class="nav-brand">
            <div class="logo-container">
                <svg class="logo-icon" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
                            <stop offset="50%" style="stop-color:#8b5cf6;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#ec4899;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                    <circle cx="32" cy="32" r="28" fill="url(#logoGradient)" opacity="0.2"/>
                    <path d="M32 12 L42 22 L32 32 L22 22 Z" fill="url(#logoGradient)"/>
                    <circle cx="32" cy="32" r="4" fill="#ffffff"/>
                    <path d="M32 40 L28 48 L36 48 Z" fill="url(#logoGradient)"/>
                    <rect x="26" y="50" width="12" height="2" fill="url(#logoGradient)"/>
                </svg>
            </div>
            <div class="nav-text-container">
                <span class="nav-logo">FactScreen</span>
                <span class="nav-tagline">AI-Powered Fact Verification</span>
            </div>
        </div>
        <div class="nav-buttons-container">
            <button class="nav-btn-html" id="nav-btn-home" onclick="window.location.href='?nav=home'">
                <svg class="nav-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>HOME</span>
            </button>
            <button class="nav-btn-html" id="nav-btn-about" onclick="window.location.href='?nav=about'">
                <svg class="nav-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                    <path d="M12 16V12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <circle cx="12" cy="8" r="1" fill="currentColor"/>
                </svg>
                <span>ABOUT</span>
            </button>
            <button class="nav-btn-html" id="nav-btn-help" onclick="window.location.href='?nav=help'">
                <svg class="nav-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                    <path d="M9.09 9C9.3251 8.33167 9.78915 7.76811 10.4 7.40913C11.0108 7.05016 11.7289 6.91894 12.4272 7.03871C13.1255 7.15849 13.7588 7.52152 14.2151 8.06353C14.6713 8.60553 14.9211 9.29152 14.92 10C14.92 12 11.92 13 11.92 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="12" cy="17" r="1" fill="currentColor"/>
                </svg>
                <span>HELP</span>
            </button>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Handle navigation via query params
if "nav" in st.query_params:
    nav_page = st.query_params.get("nav")
    if nav_page in ["home", "about", "help"]:
        st.session_state.page = nav_page
        for key in list(st.query_params.keys()):
            del st.query_params[key]
        st.rerun()

# Update active button state
st.markdown(
    f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const currentPage = '{st.session_state.page}';
            const buttons = {{
                'home': document.getElementById('nav-btn-home'),
                'about': document.getElementById('nav-btn-about'),
                'help': document.getElementById('nav-btn-help')
            }};
            
            Object.keys(buttons).forEach(page => {{
                if (buttons[page]) {{
                    if (page === currentPage) {{
                        buttons[page].classList.add('active');
                    }} else {{
                        buttons[page].classList.remove('active');
                    }}
                }}
            }});
        }});
    </script>
    """,
    unsafe_allow_html=True,
)

# Hide sidebar completely
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page routing
if st.session_state.page == "about":
    about.render_about_page()
elif st.session_state.page == "help":
    help.render_help_page()
else:
    home.render_home_page()

