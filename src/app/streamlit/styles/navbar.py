from textwrap import dedent

NAVBAR_CSS = dedent(
    """
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


"""
).strip()
