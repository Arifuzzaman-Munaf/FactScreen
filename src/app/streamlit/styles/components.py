from textwrap import dedent

COMPONENTS_CSS = dedent(
"""
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


"""
).strip()
