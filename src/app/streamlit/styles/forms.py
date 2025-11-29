from textwrap import dedent

FORMS_CSS = dedent(
    """
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


"""
).strip()
