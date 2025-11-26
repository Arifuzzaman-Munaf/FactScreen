"""
Utility functions for FactScreen
"""


def extract_key_claim(text: str) -> str:
    """Extract key claim from text (simple implementation)"""
    if not text:
        return ""
    # Simple extraction - take first sentence or first 200 chars
    sentences = text.split(".")
    if sentences:
        return sentences[0].strip()[:200]
    return text[:200].strip()


def extract_claim(text: str) -> str:
    """Extract claim from text"""
    return extract_key_claim(text)
