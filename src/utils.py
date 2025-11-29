"""
Utility functions for FactScreen
"""
from urllib.parse import urlparse


def extract_key_claim(text: str) -> str:
    """Extract key claim from text (simple implementation)
    Args:
        text: The text to extract the key claim from

    Returns:
        The key claim
    """
    if not text:
        return ""
    
    # Check if the text is a URL - if so, return it as-is (up to reasonable length)
    text_stripped = text.strip()
    try:
        parsed = urlparse(text_stripped)
        # If it has a scheme and netloc, it's a valid URL
        if parsed.scheme and parsed.netloc:
            # Return the full URL, but limit to 500 chars to avoid extremely long URLs
            return text_stripped[:500]
    except Exception:
        # Not a URL, continue with normal processing
        pass
    
    # For non-URL text, split into sentences and take the first one
    sentences = text.split(".")
    if sentences:
        return sentences[0].strip()[:200]
    return text[:200].strip()


def extract_claim(text: str) -> str:
    """Extract claim from text
    Args:
        text: The text to extract the claim from

    Returns:
        The claim
    """
    # Extract the key claim
    return extract_key_claim(text)
