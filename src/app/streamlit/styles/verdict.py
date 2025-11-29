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
        rgba(30, 41, 59, 0.9) 0%, 
        rgba(15, 23, 42, 0.95) 50%, 
        rgba(30, 41, 59, 0.9) 100%) !important;
    backdrop-filter: blur(22px) saturate(180%) !important;
    border-radius: 24px !important;
    border: 1px solid rgba(99, 102, 241, 0.45) !important;
    padding: 1rem !important;
    margin: 1.75rem auto !important;
    max-width: 1080px !important;
    box-shadow: 
        0 18px 50px rgba(0, 0, 0, 0.45),
        0 10px 30px rgba(76, 81, 191, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
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
    padding: 0.9rem 1.25rem !important;
    border-radius: 16px !important;
    background: rgba(79, 70, 229, 0.08) !important;
    border: 1px solid rgba(148, 163, 184, 0.25) !important;
    transition: all 0.3s ease !important;
}

.stExpander summary:hover {
    background: rgba(99, 102, 241, 0.1) !important;
    color: rgba(248, 250, 252, 1) !important;
}

.section-heading {
    margin: 2.5rem auto 1rem auto;
    max-width: 1080px;
    padding: 0 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
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
    padding: 1.5px;
    border-radius: 24px;
    border: 1px solid rgba(148, 163, 184, 0.6);
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(15, 23, 42, 0.94));
    box-shadow:
        0 20px 45px rgba(15, 23, 42, 0.7),
        inset 0 1px 0 rgba(255, 255, 255, 0.06);
}

.source-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 10px;
}

.source-table thead th {
    padding: 0.9rem 1.4rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 0.8rem;
    background: rgba(15, 23, 42, 0.85);
    border-right: 1px solid rgba(30, 64, 175, 0.6);
}

.source-table thead th:first-child {
    border-top-left-radius: 18px;
    border-bottom-left-radius: 18px;
}

.source-table thead th:last-child {
    border-right: none;
    border-top-right-radius: 18px;
    border-bottom-right-radius: 18px;
}

.source-table tbody tr {
    background: linear-gradient(120deg, rgba(30, 64, 175, 0.14), rgba(15, 23, 42, 0.98));
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(30, 64, 175, 0.65);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.source-table tbody tr:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 36px rgba(15, 23, 42, 0.8);
    border-color: rgba(96, 165, 250, 0.9);
}

.source-table tbody td {
    padding: 0.95rem 1.4rem;
    border: none;
    font-size: 0.95rem;
}

.source-table tbody tr td:first-child {
    border-top-left-radius: 24px;
    border-bottom-left-radius: 24px;
}

.source-table tbody tr td:last-child {
    border-top-right-radius: 24px;
    border-bottom-right-radius: 24px;
}

.source-table a {
    color: #c4b5fd;
    text-decoration: none;
    font-weight: 600;
}

.source-table a:hover {
    text-decoration: underline;
}

.rating-pill {
    font-weight: 700;
    border-radius: 999px;
    padding: 0.4rem 1.1rem;
    display: inline-block;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.85rem;
    box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.25);
}

.rating-pill[data-rating="true"] {
    background: linear-gradient(120deg, rgba(16, 185, 129, 0.2), rgba(5, 46, 22, 0.55));
    color: #bbf7d0;
}

.rating-pill[data-rating="false"],
.rating-pill[data-rating="false or misleading"],
.rating-pill[data-rating="misleading"] {
    background: linear-gradient(120deg, rgba(239, 68, 68, 0.25), rgba(67, 12, 23, 0.6));
    color: #fecaca;
}

.rating-pill[data-rating="unclear"],
.rating-pill[data-rating="unknown"] {
    background: linear-gradient(120deg, rgba(234, 179, 8, 0.2), rgba(70, 41, 3, 0.45));
    color: #fde68a;
}

.summary-cell {
    color: rgba(248, 250, 252, 0.96);
    line-height: 1.6;
    font-size: 0.98rem;
}

.source-cell {
    text-align: right;
    width: 170px;
}

.source-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.45rem 1rem;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.35), rgba(79, 70, 229, 0.45));
    color: #ede9fe !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    transition: all 0.2s ease;
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.25);
}

.source-link::after {
    content: '↗';
    font-size: 0.85rem;
}

.source-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 30px rgba(79, 70, 229, 0.35);
    text-decoration: none;
}

.source-table-placeholder {
    max-width: 1080px;
    margin: 0 auto 2rem auto;
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.92), rgba(17, 24, 39, 0.9));
    border: 1px solid rgba(99, 102, 241, 0.35);
    box-shadow: 
        0 20px 55px rgba(12, 17, 40, 0.65),
        inset 0 1px 0 rgba(255, 255, 255, 0.08);
    color: rgba(248, 250, 252, 0.85);
    font-size: 1rem;
    letter-spacing: 0.05em;
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

.sources-list {
    max-width: 1080px;
    margin: 0 auto 2rem auto;
    padding: 1.75rem 2rem;
    border-radius: 24px;
    border: 1px solid rgba(99, 102, 241, 0.4);
    background: radial-gradient(circle at 0% 0%, rgba(99, 102, 241, 0.25), transparent 55%),
                radial-gradient(circle at 100% 100%, rgba(56, 189, 248, 0.25), transparent 55%),
                linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.92));
    box-shadow:
        0 22px 55px rgba(15, 23, 42, 0.75),
        inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.sources-list h4 {
    margin-bottom: 0.75rem;
    font-size: 0.95rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(226, 232, 240, 0.9);
}

.sources-list ol {
    list-style: none;
    padding-left: 0;
    margin: 0;
}

.sources-list li {
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(148, 163, 184, 0.25);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

.sources-list li:last-child {
    border-bottom: none;
}

.sources-list .source-title {
    font-weight: 600;
    color: rgba(248, 250, 252, 0.94);
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