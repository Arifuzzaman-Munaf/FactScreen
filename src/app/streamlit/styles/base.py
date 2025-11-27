from textwrap import dedent

BASE_CSS = dedent(
"""
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


"""
).strip()
