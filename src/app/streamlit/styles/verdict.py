from textwrap import dedent

VERDICT_CSS = dedent(
"""
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


"""
).strip()
