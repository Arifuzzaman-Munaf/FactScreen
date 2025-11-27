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

/* Hide Streamlit menu and settings */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
div[data-testid="stToolbar"] {visibility: hidden !important;}
.stDecoration {display: none;}
#stDecoration {display: none;}

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

.css-1d391kg, .css-12oz5g7, .css-1adrfps, .stTextInput label, .stTextArea label {
    color: var(--text-light) !important;
}

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(148, 163, 184, 0.3) !important;
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.2) !important;
}

.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: rgba(15, 23, 42, 0.7) !important;
    color: var(--text-light) !important;
    border: 2px solid rgba(99, 102, 241, 0.5) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: rgba(99, 102, 241, 0.9) !important;
    box-shadow: 0 0 25px rgba(99, 102, 241, 0.4) !important;
    background: rgba(15, 23, 42, 0.85) !important;
}

/* Enhanced button styling */
.stButton>button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%) !important;
    background-size: 200% 200% !important;
    animation: buttonGradient 3s ease infinite !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 10px 35px rgba(99, 102, 241, 0.5), 
                0 0 20px rgba(139, 92, 246, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
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
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 15px 50px rgba(99, 102, 241, 0.7),
                0 0 30px rgba(139, 92, 246, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}

.stButton>button:active {
    transform: translateY(-1px) scale(1.01) !important;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6) !important;
}

/* Secondary button style for navigation */
button[kind="secondary"] {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 2px solid rgba(99, 102, 241, 0.4) !important;
    color: var(--text-light) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
}

button[kind="secondary"]:hover {
    background: rgba(15, 23, 42, 0.95) !important;
    border-color: rgba(99, 102, 241, 0.7) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3) !important;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899, #f59e0b);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleGradient 5s ease infinite;
    text-align: center;
    margin: 0.5rem 0 1rem 0;
    line-height: 1.2;
    text-shadow: 0 0 40px rgba(99, 102, 241, 0.5);
}

@keyframes titleGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-subtitle {
    font-size: 1.3rem;
    text-align: center;
    color: rgba(248, 250, 252, 0.8);
    margin-bottom: 1.5rem;
    font-weight: 300;
}

.content-card {
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
    border: 1px solid rgba(99, 102, 241, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.verdict-section {
    width: 100%;
    padding: 2.5rem 2rem;
    margin: 1.5rem 0;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    animation: verdictPulse 2s ease-in-out infinite;
}

@keyframes verdictPulse {
    0%, 100% { box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); }
    50% { box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4); }
}

.verdict-true {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: #ffffff;
}

.verdict-misleading, .verdict-false {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: #ffffff;
}

.verdict-unknown {
    background: linear-gradient(135deg, #eab308, #ca8a04);
    color: #ffffff;
}

.verdict-label {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}

.verdict-text {
    font-size: 3rem;
    font-weight: 700;
    margin: 0.5rem 0;
}

.verdict-confidence {
    font-size: 1.1rem;
    opacity: 0.95;
    margin-top: 0.5rem;
}

.stExpander {
    background: rgba(15, 23, 42, 0.5) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
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
    padding: 1.5rem 1.5rem;
    background: rgba(15, 23, 42, 0.8);
    border-radius: 16px;
    border: 2px solid rgba(99, 102, 241, 0.4);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    margin: 1rem 0;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
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
</style>
"""


