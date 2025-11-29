"""
Utility functions for FactScreen
"""


def extract_key_claim(text: str) -> str:
    """Extract key claim from text (simple implementation)
    Args:
        text: The text to extract the key claim from

    Returns:
        The key claim
    """
    if not text:
        return ""
    # Split the text into sentences
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