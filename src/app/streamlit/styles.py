"""
CSS styles and theme configuration for the Streamlit frontend.

This module contains all CSS styles, animations, and theme configurations
used throughout the Streamlit application to ensure a consistent, modern,
and accessible user interface.
"""

THEME_CSS = """
<style>
:root {
    --bg-dark: #0f172a;
    --bg-card: #111827;
    --accent-primary: #6366f1;
    --accent-secondary: #f472b6;
    --text-light: #f8fafc;
}

/* Hide Streamlit menu and settings but keep header space */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
div[data-testid="stToolbar"] {visibility: hidden !important;}
.stDecoration {display: none;}
#stDecoration {display: none;}

/* Make header area available for custom navbar */
header[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Remove default Streamlit padding */
.stApp > header {
    display: none !important;
}

/* Ensure body and html start at top */
html, body {
    margin: 0 !important;
    padding: 0 !important;
}

/* Remove any default Streamlit spacing */
#root {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Top Navigation Bar - Stunning Glassmorphic Design */
.top-navbar {
    background: linear-gradient(135deg, 
        rgba(15, 23, 42, 0.95) 0%, 
        rgba(30, 41, 59, 0.95) 50%,
        rgba(15, 23, 42, 0.95) 100%);
    backdrop-filter: blur(30px) saturate(180%);
    -webkit-backdrop-filter: blur(30px) saturate(180%);
    border-bottom: 2px solid transparent;
    background-image: 
        linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)),
        linear-gradient(90deg, 
            rgba(99, 102, 241, 0.6), 
            rgba(139, 92, 246, 0.6), 
            rgba(236, 72, 153, 0.6),
            rgba(99, 102, 241, 0.6));
    background-origin: border-box;
    background-clip: padding-box, border-box;
    padding: 1.5rem 4rem;
    margin: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 
        0 10px 40px rgba(0, 0, 0, 0.6),
        0 0 0 1px rgba(99, 102, 241, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.15),
        inset 0 -1px 0 rgba(99, 102, 241, 0.2);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 1000;
    box-sizing: border-box;
    animation: navbarGlow 4s ease-in-out infinite;
}

/* Ensure navbar content is properly structured - everything in parallel */
.top-navbar {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
}

.top-navbar [data-testid="column-container"] {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    gap: 1rem !important;
}

.top-navbar [data-testid="column"] {
    display: flex !important;
    align-items: center !important;
    flex: 0 0 auto !important;
}

.top-navbar .nav-brand {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
}

.top-navbar .nav-buttons-wrapper {
    flex: 0 0 auto;
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: flex-end;
}

@keyframes navbarGlow {
    0%, 100% { 
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    50% { 
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.5),
            0 0 20px rgba(99, 102, 241, 0.4),
            0 0 0 1px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
}

/* Add padding to main content to account for fixed navbar */
.main .block-container {
    padding-top: 6.5rem !important;
    margin-top: 0 !important;
    max-width: 1400px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

/* JavaScript injection to restructure navbar */
.stApp::before {
    content: '';
    display: block;
    height: 0;
}

/* Ensure app container starts at top */
.stApp {
    margin-top: 0 !important;
    padding-top: 0 !important;
    overflow-x: hidden !important;
}

/* Remove any spacing before navbar */
.stApp > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Ensure navbar is at absolute top */
.top-navbar {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

.nav-brand {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    align-items: center;
    justify-content: flex-start;
}

.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    flex-shrink: 0;
}

.logo-icon {
    width: 48px;
    height: 48px;
    filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.6));
    animation: logoFloat 3s ease-in-out infinite;
}

@keyframes logoFloat {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-5px);
    }
}

.nav-text-container {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.nav-logo {
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: navLogoGradient 4s ease infinite;
    letter-spacing: -0.03em;
    filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.5));
    transition: filter 0.3s ease;
}

.nav-logo:hover {
    filter: drop-shadow(0 0 30px rgba(99, 102, 241, 0.7));
}

@keyframes navLogoGradient {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.nav-tagline {
    font-size: 0.9rem;
    color: rgba(248, 250, 252, 0.8);
    font-weight: 400;
    letter-spacing: 0.3px;
}

.nav-buttons-wrapper {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: flex-end;
    flex-wrap: nowrap;
}

.nav-buttons-container {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: flex-end;
}

/* Ensure Streamlit columns in navbar are properly styled */
.nav-buttons-wrapper [data-testid="column"],
.nav-buttons-container [data-testid="column"] {
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: 130px !important;
    max-width: 150px !important;
    padding: 0 !important;
    margin: 0 !important;
}

.nav-buttons-wrapper [data-testid="column"] > div,
.nav-buttons-container [data-testid="column"] > div {
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Ensure the column container itself is a flex container */
.nav-buttons-wrapper > div[data-testid="column-container"],
.nav-buttons-container > div[data-testid="column-container"] {
    display: flex !important;
    gap: 1rem !important;
    align-items: center !important;
    justify-content: flex-end !important;
    width: 100% !important;
}

/* Fix for columns that appear after nav-buttons-wrapper */
.top-navbar + * [data-testid="column-container"] {
    display: flex !important;
    gap: 1rem !important;
    align-items: center !important;
    justify-content: flex-end !important;
}

/* Style Streamlit buttons in navbar - formal & classic */
.nav-buttons-wrapper .stButton > button,
.nav-buttons-container .stButton > button,
.top-navbar .stButton > button {
    background: rgba(13, 18, 32, 0.85) !important;
    border: 1px solid rgba(226, 232, 240, 0.35) !important;
    color: #e2e8f0 !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.2rem !important;
    font-family: "Segoe UI", "Helvetica Neue", sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    min-width: 120px !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: none !important;
    transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease !important;
    width: 100% !important;
    height: auto !important;
}

.nav-buttons-wrapper .stButton > button::before,
.nav-buttons-container .stButton > button::before,
.top-navbar .stButton > button::before {
    display: none !important;
}

.nav-buttons-wrapper .stButton > button:hover,
.nav-buttons-container .stButton > button:hover,
.top-navbar .stButton > button:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    border-color: rgba(248, 250, 252, 0.65) !important;
    color: #ffffff !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Active / Focus state */
.nav-buttons-wrapper .stButton > button.nav-active,
.nav-buttons-container .stButton > button.nav-active,
.nav-buttons-wrapper .stButton > button:focus,
.nav-buttons-container .stButton > button:focus,
.top-navbar .stButton > button:focus {
    background: #ffffff !important;
    border-color: #ffffff !important;
    color: #0f172a !important;
    box-shadow: none !important;
    transform: none !important;
    animation: none !important;
    font-weight: 600 !important;
}

/* Custom HTML buttons (if used) */
.nav-btn-html {
    background: rgba(13, 18, 32, 0.85) !important;
    border: 1px solid rgba(226, 232, 240, 0.35) !important;
    color: #e2e8f0 !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.2rem !important;
    font-family: "Segoe UI", "Helvetica Neue", sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    min-width: 120px !important;
    cursor: pointer !important;
    transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.6rem !important;
}

.nav-btn-html:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    border-color: rgba(248, 250, 252, 0.65) !important;
    color: #ffffff !important;
    transform: none !important;
    box-shadow: none !important;
}

.nav-btn-html.active {
    background: #ffffff !important;
    border-color: #ffffff !important;
    color: #0f172a !important;
    box-shadow: none !important;
    transform: none !important;
    animation: none !important;
    font-weight: 600 !important;
}

.nav-btn-html::before {
    display: none !important;
}

.nav-icon-svg {
    width: 18px;
    height: 18px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-right: 0.6rem;
}

.nav-icon-svg svg {
    width: 100%;
    height: 100%;
    display: block;
    stroke: currentColor;
    fill: none;
}

.nav-label-text {
    letter-spacing: 0.08em;
}

@keyframes buttonPulse {
    0%, 100% {
        box-shadow: 
            0 8px 30px rgba(99, 102, 241, 0.6),
            0 0 20px rgba(139, 92, 246, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    50% {
        box-shadow: 
            0 8px 35px rgba(99, 102, 241, 0.8),
            0 0 30px rgba(139, 92, 246, 0.7),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
}

/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* Force dark mode - override any light mode */
.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #2d1b3d 50%, #1a1f3a 75%, #0a0e27 100%) !important;
    background-size: 400% 400% !important;
    animation: gradientShift 15s ease infinite !important;
    color: var(--text-light) !important;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp header {
    background: linear-gradient(90deg, #111827, #1f2937, #2d1b3d) !important;
    color: var(--text-light) !important;
    border-bottom: 2px solid rgba(99, 102, 241, 0.5) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
}

/* Input Card Container - Glassmorphic Design with Better Contrast */
div[data-testid="stForm"] {
    background: linear-gradient(135deg, 
        rgba(30, 41, 59, 0.95) 0%, 
        rgba(15, 23, 42, 0.9) 50%, 
        rgba(30, 41, 59, 0.95) 100%) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    border-radius: 24px !important;
    padding: 2.5rem !important;
    margin: 2rem auto !important;
    max-width: 900px !important;
    border: 2px solid rgba(99, 102, 241, 0.5) !important;
    box-shadow: 
        0 12px 48px rgba(0, 0, 0, 0.5),
        0 4px 16px rgba(99, 102, 241, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.15),
        inset 0 -1px 0 rgba(0, 0, 0, 0.2),
        0 0 0 1px rgba(99, 102, 241, 0.2) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

div[data-testid="stForm"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(99, 102, 241, 0.1), 
        transparent);
    transition: left 0.6s ease;
}

div[data-testid="stForm"]:hover::before {
    left: 100%;
}

div[data-testid="stForm"]:hover {
    border-color: rgba(99, 102, 241, 0.7) !important;
    box-shadow: 
        0 16px 64px rgba(0, 0, 0, 0.6),
        0 8px 24px rgba(99, 102, 241, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.2),
        inset 0 -1px 0 rgba(0, 0, 0, 0.3),
        0 0 60px rgba(99, 102, 241, 0.4) !important;
    transform: translateY(-3px);
    background: linear-gradient(135deg, 
        rgba(30, 41, 59, 1) 0%, 
        rgba(15, 23, 42, 0.95) 50%, 
        rgba(30, 41, 59, 1) 100%) !important;
}

/* Input Labels */
.css-1d391kg, .css-12oz5g7, .css-1adrfps, .stTextInput label, .stTextArea label {
    color: var(--text-light) !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.75rem !important;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(148, 163, 184, 0.3) !important;
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.2) !important;
}

/* Input Fields - Enhanced Styling with Better Contrast */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: rgba(30, 41, 59, 0.8) !important;
    backdrop-filter: blur(10px) !important;
    border: 2px solid rgba(99, 102, 241, 0.4) !important;
    border-radius: 16px !important;
    color: var(--text-light) !important;
    padding: 1rem 1.25rem !important;
    font-size: 1.05rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        inset 0 2px 4px rgba(0, 0, 0, 0.3),
        0 1px 0 rgba(255, 255, 255, 0.08),
        0 0 0 1px rgba(99, 102, 241, 0.1) !important;
}

.stTextInput>div>div>input::placeholder, .stTextArea>div>div>textarea::placeholder {
    color: rgba(248, 250, 252, 0.4) !important;
    font-style: italic;
}

.stTextInput>div>div>input:hover, .stTextArea>div>div>textarea:hover {
    border-color: rgba(99, 102, 241, 0.6) !important;
    background: rgba(30, 41, 59, 0.9) !important;
    box-shadow: 
        inset 0 2px 4px rgba(0, 0, 0, 0.3),
        0 1px 0 rgba(255, 255, 255, 0.1),
        0 0 25px rgba(99, 102, 241, 0.3) !important;
}

.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: rgba(99, 102, 241, 1) !important;
    box-shadow: 
        0 0 0 4px rgba(99, 102, 241, 0.3),
        0 0 40px rgba(99, 102, 241, 0.6),
        inset 0 2px 4px rgba(0, 0, 0, 0.3),
        0 4px 12px rgba(99, 102, 241, 0.4) !important;
    outline: none !important;
    transform: scale(1.01);
    background: rgba(30, 41, 59, 1) !important;
}

/* Enhanced button styling - Primary Button */
.stButton>button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%) !important;
    background-size: 200% 200% !important;
    animation: buttonGradient 4s ease infinite !important;
    color: #ffffff !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 16px !important;
    padding: 1rem 2.5rem !important;
    font-weight: 800 !important;
    font-size: 1.15rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    box-shadow: 
        0 10px 30px rgba(99, 102, 241, 0.6),
        0 4px 15px rgba(139, 92, 246, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.3),
        inset 0 -1px 0 rgba(0, 0, 0, 0.2) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.stButton>button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.stButton>button:hover::before {
    left: 100%;
}

@keyframes buttonGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stButton>button:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 
        0 20px 60px rgba(99, 102, 241, 0.8),
        0 8px 25px rgba(139, 92, 246, 0.6),
        0 0 40px rgba(236, 72, 153, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.4),
        inset 0 -1px 0 rgba(0, 0, 0, 0.2) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
}

.stButton>button:active {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 
        0 8px 25px rgba(99, 102, 241, 0.7),
        0 4px 15px rgba(139, 92, 246, 0.5),
        inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
}

/* Secondary button style (Clear button) */
button[kind="secondary"] {
    background: rgba(15, 23, 42, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    border: 2px solid rgba(99, 102, 241, 0.4) !important;
    color: var(--text-light) !important;
    border-radius: 16px !important;
    padding: 1rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    box-shadow: 
        0 6px 20px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
}

button[kind="secondary"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.5s;
}

button[kind="secondary"]:hover::before {
    left: 100%;
}

button[kind="secondary"]:hover {
    background: rgba(15, 23, 42, 1) !important;
    border-color: rgba(99, 102, 241, 0.7) !important;
    box-shadow: 
        0 10px 30px rgba(99, 102, 241, 0.4),
        0 4px 15px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    transform: translateY(-2px) scale(1.02);
}

button[kind="secondary"]:active {
    transform: translateY(0) scale(0.98);
}

.hero-title {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 900;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 25%, #ec4899 50%, #f59e0b 75%, #6366f1 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleGradient 6s ease infinite;
    text-align: center;
    margin: 2rem 0 1.5rem 0;
    line-height: 1.15;
    letter-spacing: -0.02em;
    filter: drop-shadow(0 0 30px rgba(99, 102, 241, 0.4));
    position: relative;
    padding: 0 1rem;
}

@keyframes titleGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-subtitle {
    font-size: clamp(1.1rem, 2vw, 1.4rem);
    text-align: center;
    color: rgba(248, 250, 252, 0.85);
    margin-bottom: 3rem;
    font-weight: 400;
    letter-spacing: 0.02em;
    line-height: 1.6;
    padding: 0 2rem;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

.content-card {
    background: linear-gradient(135deg, 
        rgba(30, 41, 59, 0.85) 0%, 
        rgba(15, 23, 42, 0.9) 50%, 
        rgba(30, 41, 59, 0.85) 100%);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-radius: 24px;
    padding: 2.5rem;
    margin: 2rem 0;
    border: 2px solid rgba(99, 102, 241, 0.4);
    box-shadow: 
        0 12px 48px rgba(0, 0, 0, 0.4),
        0 4px 16px rgba(99, 102, 241, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.content-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
    transition: left 0.5s;
}

.content-card:hover::before {
    left: 100%;
}

.content-card:hover {
    transform: translateY(-4px);
    box-shadow: 
        0 16px 56px rgba(0, 0, 0, 0.5),
        0 6px 20px rgba(99, 102, 241, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    border-color: rgba(99, 102, 241, 0.6);
}

.content-card h2 {
    color: rgba(248, 250, 252, 0.95);
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 1.25rem;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}

.content-card p {
    color: rgba(248, 250, 252, 0.85);
    line-height: 1.8;
    margin-bottom: 1rem;
    font-size: 1.05rem;
}

.content-card ul, .content-card ol {
    color: rgba(248, 250, 252, 0.85);
    line-height: 1.8;
    margin-left: 1.5rem;
    margin-bottom: 1rem;
}

.content-card li {
    margin-bottom: 0.75rem;
    padding-left: 0.5rem;
}

.content-card strong {
    color: rgba(248, 250, 252, 0.95);
    font-weight: 600;
}

.content-card code {
    background: rgba(99, 102, 241, 0.2);
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
    color: #a78bfa;
    border: 1px solid rgba(99, 102, 241, 0.3);
}

.content-card table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    background: rgba(15, 23, 42, 0.5);
    border-radius: 12px;
    overflow: hidden;
}

.content-card th {
    background: rgba(99, 102, 241, 0.3);
    color: rgba(248, 250, 252, 0.95);
    font-weight: 600;
    padding: 1rem;
    text-align: left;
    border-bottom: 2px solid rgba(99, 102, 241, 0.4);
}

.content-card td {
    padding: 0.875rem 1rem;
    border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    color: rgba(248, 250, 252, 0.85);
}

.content-card tr:hover {
    background: rgba(99, 102, 241, 0.1);
}

.claim-verdict-row {
    display: flex;
    gap: 2.5rem;
    max-width: 1200px;
    margin: 0 auto 1.5rem auto;
    align-items: flex-start;
}

.claim-verdict-row > div[data-testid="column"] {
    flex: 1;
    display: flex;
    padding-top: 0 !important;
}

.claim-verdict-row > div[data-testid="column"] > div {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.claim-verdict-row div[data-testid="stForm"][aria-label="claim_form"] {
    width: 100%;
    padding: 2.5rem;
    border-radius: 28px;
    border: 1px solid rgba(94, 96, 206, 0.5);
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(37, 46, 76, 0.9));
    box-shadow: 0 25px 55px rgba(15, 23, 42, 0.6);
    min-height: 350px;
    display: flex;
    flex-direction: column;
}

.claim-verdict-row #verdict-result {
    width: 100%;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.verdict-card {
    width: 100%;
    margin: 0;
    padding: 2.5rem;
    border-radius: 28px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    background: linear-gradient(145deg, rgba(32, 59, 94, 0.35), rgba(18, 24, 38, 0.15)),
                linear-gradient(135deg, rgba(32, 235, 140, 0.95), rgba(23, 173, 64, 0.9));
    box-shadow: 0 35px 65px rgba(25, 135, 84, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 350px;
}

.verdict-card::before {
    content: "";
    position: absolute;
    inset: 18px;
    border-radius: 22px;
    border: 1px solid rgba(255, 255, 255, 0.25);
    background: radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.25), transparent 55%);
    pointer-events: none;
}

.verdict-card::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 28px;
    background: linear-gradient(120deg, rgba(255, 255, 255, 0.25), transparent 40%);
    opacity: 0.35;
    pointer-events: none;
}

.verdict-card > * {
    position: relative;
    z-index: 1;
}

.verdict-card.verdict-true {
    background: linear-gradient(145deg, rgba(32, 59, 94, 0.35), rgba(18, 24, 38, 0.15)),
                linear-gradient(135deg, rgba(34, 197, 94, 0.97), rgba(19, 142, 73, 0.9));
    box-shadow: 0 35px 65px rgba(16, 185, 129, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.verdict-card.verdict-misleading {
    background: linear-gradient(145deg, rgba(94, 32, 59, 0.4), rgba(38, 18, 24, 0.2)),
                linear-gradient(135deg, rgba(239, 68, 68, 0.97), rgba(190, 24, 93, 0.9));
    box-shadow: 0 35px 65px rgba(239, 68, 68, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.verdict-card.verdict-unknown {
    background: linear-gradient(145deg, rgba(94, 84, 32, 0.35), rgba(38, 33, 18, 0.15)),
                linear-gradient(135deg, rgba(234, 179, 8, 0.9), rgba(217, 119, 6, 0.85));
    box-shadow: 0 30px 55px rgba(217, 119, 6, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.verdict-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.verdict-label {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.4rem;
    opacity: 0.85;
}

.verdict-pill {
    background: rgba(255, 255, 255, 0.2);
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.85rem;
    letter-spacing: 0.3rem;
    text-transform: uppercase;
}

.verdict-card-body {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 1.6rem;
    text-align: center;
}

.verdict-main-text {
    font-size: clamp(2.4rem, 4vw, 3.6rem);
    font-weight: 800;
    letter-spacing: -0.02em;
}

.verdict-subtext {
    font-size: 0.95rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.85);
    margin: 0;
}

.confidence-gauge {
    --confidence-value: 0;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: conic-gradient(#fef3c7 calc(var(--confidence-value) * 1%), rgba(255, 255, 255, 0.15) 0);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 0.35rem;
    margin: 0 auto;
}

.verdict-card.verdict-true .confidence-gauge {
    background: conic-gradient(#dcfce7 calc(var(--confidence-value) * 1%), rgba(255, 255, 255, 0.15) 0);
}

.verdict-card.verdict-unknown .confidence-gauge {
    background: conic-gradient(#fef9c3 calc(var(--confidence-value) * 1%), rgba(255, 255, 255, 0.15) 0);
}

.confidence-gauge[data-empty="true"] {
    background: rgba(255, 255, 255, 0.2);
}

.confidence-center {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: rgba(15, 23, 42, 0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.15rem;
    text-align: center;
}

.confidence-center span {
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
}

.confidence-center small {
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.7);
}


.stExpander {
    background: linear-gradient(135deg, 
        rgba(30, 41, 59, 0.85) 0%, 
        rgba(15, 23, 42, 0.9) 50%, 
        rgba(30, 41, 59, 0.85) 100%) !important;
    backdrop-filter: blur(15px) saturate(180%) !important;
    border-radius: 16px !important;
    border: 2px solid rgba(99, 102, 241, 0.4) !important;
    padding: 1rem !important;
    margin: 1.5rem 0 !important;
    max-width: 900px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        0 2px 8px rgba(99, 102, 241, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stExpander:hover {
    border-color: rgba(99, 102, 241, 0.6) !important;
    box-shadow: 
        0 12px 40px rgba(0, 0, 0, 0.4),
        0 4px 12px rgba(99, 102, 241, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    transform: translateY(-2px);
}

.stExpander summary {
    color: rgba(248, 250, 252, 0.95) !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    padding: 0.75rem 1rem !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

.stExpander summary:hover {
    background: rgba(99, 102, 241, 0.1) !important;
    color: rgba(248, 250, 252, 1) !important;
}

.section-heading {
    margin: 2.5rem auto 1rem auto;
    max-width: 1080px;
}

.section-heading h3 {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
    color: rgba(248, 250, 252, 0.95);
}

.source-table-wrapper {
    max-width: 1080px;
    margin: 0 auto 2rem auto;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.35);
}

.source-table {
    width: 100%;
    border-collapse: collapse;
}

.source-table th,
.source-table td {
    padding: 1rem 1.2rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    text-align: left;
    font-size: 0.95rem;
}

.source-table th {
    background: rgba(255, 255, 255, 0.05);
    text-transform: uppercase;
    letter-spacing: 0.2em;
    font-size: 0.8rem;
}

.source-table tbody tr:last-child td {
    border-bottom: none;
}

.source-table a {
    color: #c4b5fd;
    text-decoration: none;
    font-weight: 600;
}

.source-table a:hover {
    text-decoration: underline;
}

.source-table-placeholder {
    max-width: 1080px;
    margin: 0 auto 2rem auto;
    border: 1px dashed rgba(148, 163, 184, 0.5);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    color: rgba(248, 250, 252, 0.8);
    font-size: 0.95rem;
}

.explain-placeholder {
    padding: 1rem 0;
    color: rgba(248, 250, 252, 0.75);
    font-style: italic;
}

.explain-text {
    color: rgba(248, 250, 252, 0.92);
    line-height: 1.85;
    font-size: 1.05rem;
    margin-bottom: 1rem;
}

.sources-list h4 {
    margin-bottom: 0.5rem;
    font-size: 1rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

.sources-list ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
}

.sources-list li {
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.sources-list li:last-child {
    border-bottom: none;
}

h1, h2, h3 {
    color: var(--text-light) !important;
}

/* Force all text to be light colored */
p, span, div, li, td, th {
    color: var(--text-light) !important;
}

/* Ensure dataframes are dark themed */
.stDataFrame {
    background: rgba(15, 23, 42, 0.6) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    margin: 1rem 0 !important;
    max-width: 900px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Style for data table */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Dark mode for all Streamlit components */
.stSelectbox label, .stMultiSelect label, .stCheckbox label {
    color: var(--text-light) !important;
}

/* Custom Processing Animation - Smaller size */
.processing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 2rem;
    background: linear-gradient(135deg, 
        rgba(30, 41, 59, 0.9) 0%, 
        rgba(15, 23, 42, 0.95) 50%, 
        rgba(30, 41, 59, 0.9) 100%);
    backdrop-filter: blur(20px) saturate(180%);
    border-radius: 20px;
    border: 2px solid rgba(99, 102, 241, 0.5);
    box-shadow: 
        0 12px 40px rgba(0, 0, 0, 0.4),
        0 4px 16px rgba(99, 102, 241, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    margin: 2rem auto;
    max-width: 500px;
    animation: processingGlow 3s ease-in-out infinite;
}

.processing-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(4, 7, 23, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100000;
    padding: 1rem;
}

@keyframes processingGlow {
    0%, 100% {
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.4),
            0 4px 16px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    50% {
        box-shadow: 
            0 16px 50px rgba(0, 0, 0, 0.5),
            0 8px 24px rgba(99, 102, 241, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
}

.processing-loader {
    position: relative;
    width: 80px;
    height: 80px;
    margin-bottom: 1rem;
}

.processing-loader::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    border: 3px solid transparent;
    border-top: 3px solid #6366f1;
    border-right: 3px solid #8b5cf6;
    border-bottom: 3px solid #ec4899;
    border-left: 3px solid #f59e0b;
    border-radius: 50%;
    animation: spin 1.5s linear infinite;
}

.processing-loader::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 55px;
    height: 55px;
    border: 2px solid transparent;
    border-top: 2px solid #8b5cf6;
    border-right: 2px solid #ec4899;
    border-radius: 50%;
    animation: spinReverse 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes spinReverse {
    0% { transform: translate(-50%, -50%) rotate(360deg); }
    100% { transform: translate(-50%, -50%) rotate(0deg); }
}

.processing-dots {
    display: flex;
    gap: 0.4rem;
    margin-top: 0.5rem;
}

.processing-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    animation: pulse 1.4s ease-in-out infinite;
    box-shadow: 0 0 8px rgba(99, 102, 241, 0.6);
}

.processing-dot:nth-child(1) {
    animation-delay: 0s;
}

.processing-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.processing-dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        opacity: 1;
    }
    50% {
        transform: scale(1.5);
        opacity: 0.7;
    }
}

.processing-text {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-light);
    margin-top: 1rem;
    text-align: center;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: textShimmer 2s ease-in-out infinite;
}

@keyframes textShimmer {
    0%, 100% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
}

.processing-steps {
    margin-top: 0.8rem;
    font-size: 0.85rem;
    color: rgba(248, 250, 252, 0.7);
    text-align: center;
    font-style: italic;
}

/* Responsive Design - Stunning on All Screens */
@media (max-width: 1200px) {
    .main .block-container {
        max-width: 95% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    .top-navbar {
        padding: 1.25rem 2.5rem !important;
    }
    
    .nav-btn-html {
        min-width: 110px !important;
        padding: 0.65rem 1.5rem !important;
        font-size: 0.9rem !important;
    }
    
    .nav-buttons-wrapper .stButton > button,
    .nav-buttons-container .stButton > button {
        min-width: 110px !important;
        padding: 0.65rem 1.5rem !important;
        font-size: 0.9rem !important;
    }
}

@media (max-width: 768px) {
    .top-navbar {
        padding: 1rem 1.5rem !important;
        flex-direction: column !important;
        gap: 1rem !important;
        align-items: flex-start !important;
    }
    
    .nav-brand {
        width: 100% !important;
        gap: 0.75rem !important;
    }
    
    .logo-container {
        width: 40px !important;
        height: 40px !important;
    }
    
    .logo-icon {
        width: 40px !important;
        height: 40px !important;
    }
    
    .nav-buttons-wrapper,
    .nav-buttons-container {
        width: 100% !important;
        justify-content: flex-start !important;
        flex-wrap: wrap !important;
        gap: 0.75rem !important;
    }
    
    .nav-btn-html {
        min-width: 100px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.85rem !important;
        gap: 0.4rem !important;
    }
    
    .nav-buttons-wrapper .stButton > button,
    .nav-buttons-container .stButton > button {
        min-width: 100px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.85rem !important;
    }
    
    .nav-icon {
        width: 18px !important;
        height: 18px !important;
    }
    
    .nav-logo {
        font-size: 1.8rem !important;
    }
    
    .nav-tagline {
        font-size: 0.8rem !important;
    }
    
    .hero-title {
        font-size: 2rem !important;
        margin: 0.75rem 0 1rem 0 !important;
        padding: 0 0.5rem !important;
    }
    
    .hero-subtitle {
        font-size: 1rem !important;
        padding: 0 1rem !important;
        margin-bottom: 2rem !important;
    }
    
    .main .block-container {
        padding-top: 8rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    
    div[data-testid="stForm"] {
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
    }
}

@media (max-width: 480px) {
    .top-navbar {
        padding: 0.875rem 1rem !important;
    }
    
    .logo-container {
        width: 36px !important;
        height: 36px !important;
    }
    
    .logo-icon {
        width: 36px !important;
        height: 36px !important;
    }
    
    .nav-btn-html {
        min-width: 90px !important;
        padding: 0.5rem 0.875rem !important;
        font-size: 0.8rem !important;
        gap: 0.35rem !important;
    }
    
    .nav-buttons-wrapper .stButton > button,
    .nav-buttons-container .stButton > button {
        min-width: 90px !important;
        padding: 0.5rem 0.875rem !important;
        font-size: 0.8rem !important;
    }
    
    .nav-icon {
        width: 16px !important;
        height: 16px !important;
    }
    
    .nav-logo {
        font-size: 1.5rem !important;
    }
    
    .content-card {
        padding: 1.5rem !important;
        margin: 1.5rem 0 !important;
    }
    
    .content-card h2 {
        font-size: 1.5rem !important;
    }
    
    .content-card p, .content-card li {
        font-size: 1rem !important;
    }
    
    .hero-title {
        font-size: 1.75rem !important;
    }
    
    .main .block-container {
        padding-top: 9rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

/* Smooth transitions for all interactive elements */
* {
    transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

/* Ensure proper text rendering */
body, .stApp {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}
</style>
"""


