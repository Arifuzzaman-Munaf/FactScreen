import base64
import io


def extract_text_from_base64_image(image_base64: str) -> str:
    """Extract text from a base64-encoded image.

    This uses pytesseract if available; otherwise returns an empty string.
    We avoid a hard dependency to keep the project lightweight by default.
    """
    try:
        from PIL import Image  # type: ignore
        import pytesseract  # type: ignore
    except Exception:
        return ""

    try:
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))
        text: str = pytesseract.image_to_string(image)  # type: ignore
        return text.strip()
    except Exception:
        return ""
