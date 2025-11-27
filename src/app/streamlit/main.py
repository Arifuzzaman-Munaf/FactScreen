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

# Top Navigation Bar - Everything in one parallel horizontal line
# Use Streamlit columns to keep brand and buttons in the same row
nav_col_brand, nav_col_spacer, nav_col_buttons = st.columns([2.5, 0.5, 2], gap="medium")

with nav_col_brand:
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )

with nav_col_buttons:
    # Navigation buttons in parallel columns
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1], gap="small")
    
    with btn_col1:
        if st.button("HOME", key="nav_home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    
    with btn_col2:
        if st.button("ABOUT", key="nav_about", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
    
    with btn_col3:
        if st.button("HELP", key="nav_help", use_container_width=True):
            st.session_state.page = "help"
            st.rerun()

# Wrap everything in navbar styling and ensure parallel layout
st.markdown(
    """
    <script>
        (function() {
            const icons = {
                'HOME': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 4l9 6.5" /><path d="M5.5 9.5V20h13V9.5" /><path d="M9.5 20v-5.25h5V20" /></svg>',
                'ABOUT': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9" /><path d="M12 16v-4" /><path d="M12 8h.01" /></svg>',
                'HELP': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9" /><path d="M9.75 9a2.25 2.25 0 1 1 3.5 1.85c-.75.5-1.25 1.1-1.25 2.15v.25" /><path d="M12 17h.01" /></svg>'
            };
            
            function addIconsToButtons() {
                const buttons = Array.from(document.querySelectorAll('.top-navbar .stButton > button'));
                buttons.forEach(button => {
                    if (button.dataset.iconApplied === 'true') return;
                    const originalText = button.textContent.trim();
                    const lookupKey = originalText.toUpperCase();
                    const iconMarkup = icons[lookupKey];
                    if (!iconMarkup) return;
                    
                    const iconSpan = document.createElement('span');
                    iconSpan.className = 'nav-icon-svg';
                    iconSpan.innerHTML = iconMarkup;
                    iconSpan.setAttribute('aria-hidden', 'true');
                    
                    const labelSpan = document.createElement('span');
                    labelSpan.className = 'nav-label-text';
                    labelSpan.textContent = originalText;
                    
                    button.innerHTML = '';
                    button.appendChild(iconSpan);
                    button.appendChild(labelSpan);
                    button.dataset.iconApplied = 'true';
                });
            }
            
            // Wrap the navbar columns in styled container
            function wrapNavbar() {
                // Find all column containers
                const allColContainers = Array.from(document.querySelectorAll('[data-testid="column-container"]'));
                if (allColContainers.length < 2) return false;
                
                // Check if already wrapped
                const existingNavbar = document.querySelector('.top-navbar');
                if (existingNavbar) return true;
                
                // Get the first column container (should contain brand, spacer, buttons)
                const firstColContainer = allColContainers[0];
                if (!firstColContainer) return false;
                
                // Create navbar wrapper
                const navbar = document.createElement('div');
                navbar.className = 'top-navbar';
                
                // Get parent of column container
                const parent = firstColContainer.parentElement;
                
                // Clone and move the column container into navbar
                navbar.appendChild(firstColContainer.cloneNode(true));
                
                // Insert navbar before the first column container
                parent.insertBefore(navbar, firstColContainer);
                
                // Hide original (keep it for Streamlit functionality)
                firstColContainer.style.position = 'absolute';
                firstColContainer.style.opacity = '0';
                firstColContainer.style.pointerEvents = 'none';
                
                return true;
            }
            
            // Function to update active button styling
            function updateActiveButton() {
                const currentPage = '""" + st.session_state.page + """';
                const allButtons = Array.from(document.querySelectorAll('.top-navbar .stButton > button, button[key*="nav_"]'));
                
                allButtons.forEach(button => {
                    const buttonText = button.textContent.trim().toUpperCase();
                    button.classList.remove('nav-active');
                    
                    if (currentPage === 'home' && buttonText.includes('HOME')) {
                        button.classList.add('nav-active');
                    } else if (currentPage === 'about' && buttonText.includes('ABOUT')) {
                        button.classList.add('nav-active');
                    } else if (currentPage === 'help' && buttonText.includes('HELP')) {
                        button.classList.add('nav-active');
                    }
                });
            }
            
            // Initialize navbar
            function initNavbar() {
                wrapNavbar();
                updateActiveButton();
                addIconsToButtons();
            }
            
            // Run on page load
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', function() {
                    initNavbar();
                    setTimeout(initNavbar, 100);
                    setTimeout(initNavbar, 500);
                });
            } else {
                initNavbar();
                setTimeout(initNavbar, 100);
                setTimeout(initNavbar, 500);
                setTimeout(initNavbar, 1000);
            }
            
            // Watch for DOM changes
            const observer = new MutationObserver(function() {
                initNavbar();
            });
            observer.observe(document.body, { childList: true, subtree: true });
            setTimeout(() => observer.disconnect(), 5000);
        })();
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

