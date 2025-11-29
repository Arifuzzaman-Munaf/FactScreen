from textwrap import dedent

PROCESSING_CSS = dedent(
    """
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


"""
).strip()
