from textwrap import dedent

RESPONSIVE_CSS = dedent(
    """
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
"""
).strip()
