"""Gemini 2.5 Flash service for claim classification and explanation generation."""

from typing import List, Dict, Optional, Tuple
import json
import logging
from pathlib import Path

# Try to import the Gemini client from google-genai, and set a flag indicating availability
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

from src.app.core.config import settings

# --- Logging Setup ---
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "gemini.log"

logger = logging.getLogger("gemini")
# Set up logging to a file
if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def _log_event(level: int, message: str, **fields: Dict[str, object]) -> None:
    """
    Log an event to the Gemini log file, optionally with structured key-value fields.
    Args:
        level: The logging level.
        message: The message to log.
        fields: Optional key-value fields to log.
    """
    if fields:
        context = ", ".join(f"{k}={v}" for k, v in fields.items())
        message = f"{message} | {context}"
    logger.log(level, message)


def _log_usage_metadata(usage: object, context: str) -> None:
    """
    Log Gemini usage/tokens metadata if available .
    Args:
        usage: The usage metadata to log.
        context: The context of the usage.
    """
    if not usage:
        return

    prompt_tokens = getattr(usage, "prompt_token_count", "n/a")
    candidate_tokens = getattr(usage, "candidates_token_count", "n/a")
    total_tokens = getattr(usage, "total_token_count", "n/a")
    _log_event(
        logging.INFO,
        f"{context} usage",
        prompt_tokens=prompt_tokens,
        candidates_tokens=candidate_tokens,
        total_tokens=total_tokens,
    )


def _handle_gemini_exception(exc: Exception, context: str) -> str:
    """
    Log Gemini exceptions and return a user-facing error message.
    Handles invalid key, quota exhaust, and generic failures.
    Args:
        exc: The exception to log.
        context: The context of the exception.
    """
    # Get the exception message
    message = str(exc)
    lower_msg = message.lower()
    # Log the exception if the API key is invalid
    if "api key" in lower_msg and "invalid" in lower_msg:
        _log_event(
            logging.ERROR,
            f"{context} failed due to invalid Gemini API key",
            remaining_limit="unknown",
        )
        return (
            "Gemini API key is invalid. Update the GEMINI_API_KEY environment variable "
            "or .env file and restart the server."
        )

    # Log the exception if the quota is exhausted
    if "quota" in lower_msg or "exhausted" in lower_msg or "429" in lower_msg:
        _log_event(
            logging.WARNING,
            f"{context} failed due to quota exhaustion",
            remaining_limit=0,
        )
        return (
            "Gemini quota has been exhausted for the current billing window. "
            "Wait for the quota to reset or upgrade your plan."
        )

    # Log the exception if the context is not found
    _log_event(logging.ERROR, f"{context} failed", error=message)
    return f"Error in Gemini {context.lower()}: {message}"


# Caches a singleton Gemini client
_gemini_client: Optional["genai.Client"] = None


def _get_gemini_client() -> "genai.Client":
    """
    Initialize and cache the Gemini client instance.
    Raises informative errors if requirements are missing.
    """
    global _gemini_client
    # Return the cached client if it exists
    if _gemini_client is not None:
        return _gemini_client

    # Raise an error if the Gemini package is not installed
    if not GEMINI_AVAILABLE:
        raise RuntimeError("google-genai package not installed")
    # Raise an error if the Gemini API key is not configured
    if not settings.gemini_api_key:
        raise RuntimeError("Gemini API key not configured")

    # Create a new Gemini client
    _gemini_client = genai.Client(api_key=settings.gemini_api_key)
    # Return the new Gemini client
    return _gemini_client


def _invoke_gemini(prompt: str, context: str) -> Tuple[str, Optional[Dict[str, object]]]:
    """
    Invoke Gemini with a prompt and return the text response and usage metadata.
    Args:
        prompt: The prompt to send to Gemini.
        context: The context of the prompt.
    Returns:
        A tuple containing the text response and usage metadata.
    """
    # Get the Gemini client
    client = _get_gemini_client()

    try:
        # Send the prompt to Gemini
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
        )
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc

    # Try to extract the output text (either directly or from candidates)
    text = getattr(response, "text", None)
    # If no text, try to extract it from the candidates
    if not text:
        candidates = getattr(response, "candidates", None) or []
        if candidates:
            # Get the first candidate
            first = candidates[0]
            content = getattr(first, "content", None) or {}
            # Get the parts of the content
            parts = content.get("parts", []) if isinstance(content, dict) else []
            text_chunks = [p.get("text", "") for p in parts if isinstance(p, dict)]
            text = "\n".join(text_chunks).strip()
    # If no text, raise an error
    if not text:
        raise RuntimeError("Gemini returned no text")

    # Extract usage metadata if present
    usage = getattr(response, "usage_metadata", None)
    if isinstance(usage, dict):
        usage_metadata = usage
    else:
        usage_metadata = {
            "prompt_token_count": getattr(usage, "prompt_token_count", "n/a"),
            "candidates_token_count": getattr(usage, "candidates_token_count", "n/a"),
            "total_token_count": getattr(usage, "total_token_count", "n/a"),
        }
    return text, usage_metadata


async def check_claim_verdict_alignment(
    claim: str, verdicts: List[Dict[str, Optional[str]]]
) -> Tuple[bool, str]:
    """
    Check if verdicts from third-party fact-checkers are truly about the user's claim.

    Args:
        claim: User's claim string.
        verdicts: List of verdict dictionaries from sources.
    Returns:
        A tuple containing the alignment and explanation.
    """
    # Log a warning if the Gemini package is not installed
    if not GEMINI_AVAILABLE:
        _log_event(logging.WARNING, "google-genai package not installed", remaining_limit="unknown")
        return True, ""
    if not settings.gemini_api_key:
        _log_event(logging.WARNING, "Gemini API key missing", remaining_limit="unknown")
        # If no API key, assume aligned to avoid blocking
        return True, ""

    # Prepare verdict context text from up to 5 top verdicts
    verdict_context = []
    for v in verdicts[:5]:
        snippet = v.get("snippet", "") or ""
        title = v.get("title", "") or ""
        verdict = v.get("verdict", "") or v.get("rating", "") or ""
        source = v.get("source", "") or ""
        claim_being_checked = title.strip() if title else (snippet[:200] if snippet else "")
        if snippet or verdict or title:
            verdict_context.append(
                f"Source: {source}\n"
                f"Title/Claim Being Fact-Checked: {claim_being_checked}\n"
                f"Verdict/Rating: {verdict}\n"
                f"Full Context: {snippet[:300] if snippet else 'No additional context'}"
            )
    # If no verdict context, return True and an empty explanation
    if not verdict_context:
        return True, ""

    context_text = "\n\n".join(verdict_context)

    # Build the prompt with detailed instructions to force strict claim alignment checking
    prompt = f"""You are a fact-checking assistant. Analyze if the verdicts from fact-checking sources are actually about the SAME claim as the user's query.

CRITICAL: Pay special attention to:
1. OPPOSITE claims (e.g., user says "X causes Y" but verdict is about "X doesn't cause Y")
2. NEGATED claims (e.g., user says "A is true" but verdict is about "A is false")
3. DIFFERENT claims (e.g., user asks about "smoking causes cancer" but verdict is about "smoking doesn't cause cancer")

User's Claim Query: "{claim}"

Fact-Checking Results:
{context_text}

Task: Determine if these fact-checking results are about the EXACT SAME claim as the user's query.

Return aligned: false if:
- The verdicts are about the OPPOSITE of the user's claim (e.g., user says "X causes Y" but verdict says "X doesn't cause Y")
- The verdicts are about a NEGATED version of the claim
- The verdicts are about a significantly different claim (different topic, different person, different event, different time period)
- The verdicts contain negations that contradict the user's claim

Return aligned: true ONLY if:
- The verdicts are clearly about the SAME claim as the user's query
- The verdicts address the exact same statement, even if they disagree on the verdict

Respond ONLY with a JSON object in this exact format:
{{
    "aligned": true or false,
    "reason": "brief explanation of why aligned or not aligned. If not aligned, explain what the mismatch is (e.g., 'verdict is about opposite claim', 'verdict is about different topic', etc.)"
}}

Be VERY strict: When in doubt, return aligned: false."""

    try:
        # Invoke Gemini with the prompt and context
        response_text, usage = _invoke_gemini(prompt, context="alignment-check")
        _log_usage_metadata(usage, "alignment-check")

        # Extract the JSON reply from possible codeblock formatting
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        result = json.loads(response_text)
        # Get the aligned value from the result
        is_aligned = result.get("aligned", True)
        # Get the reason from the result
        reason = result.get("reason", "")

        return is_aligned, reason
    except Exception as exc:
        # Log a warning if the alignment check failed
        _log_event(
            logging.WARNING,
            "Alignment check failed; assuming aligned",
            error=str(exc),
        )
        # On error, assume aligned so we don't block legitimate users
        return True, ""


async def classify_with_gemini(
    claim: str, sources: Optional[List[Dict[str, Optional[str]]]] = None
) -> Tuple[str, float, str]:
    """
    Classify a claim using Gemini 2.5 Flash and generate an explanation.

    Args:
        claim: The claim statement to classify.
        sources: Optional list of fact-checking sources/evidence.

    Returns:
        Tuple: (label: "True"/"False"/"Unclear", confidence: float, explanation: str)
    """
    # Log a warning if the Gemini API key is not configured
    if not settings.gemini_api_key:
        _log_event(logging.WARNING, "Gemini API key missing", remaining_limit="unknown")
        return "Unclear", 0.5, "Gemini API key not configured"
    # Log a warning if the Gemini package is not installed
    if not GEMINI_AVAILABLE:
        _log_event(logging.WARNING, "google-genai package not installed", remaining_limit="unknown")
        return "Unclear", 0.5, "Gemini package not installed"

    # Construct source summaries if provided
    sources_text = ""
    if sources:
        sources_list = []
        for s in sources[:10]:
            snippet = s.get("snippet", "") or ""
            verdict = s.get("verdict", "") or s.get("rating", "") or ""
            source_name = s.get("source", "") or ""
            url = s.get("url", "") or ""
            if snippet or verdict:
                sources_list.append(
                    f"- Source: {source_name}\n  Verdict: {verdict}\n  "
                    f"Context: {snippet[:300]}\n  URL: {url}"
                )
        if sources_list:
            sources_text = "\n\n".join(sources_list)

    # Choose prompt format depending on whether sources are supplied
    if sources_text:
        prompt = f"""You are a fact-checking assistant. Classify the following claim based on the provided fact-checking sources.

Claim to verify: "{claim}"

Fact-Checking Sources:
{sources_text}

Task:
1. Analyze the claim against the provided fact-checking sources
2. Classify the claim as "True", "False", or "Unclear"
3. Provide a confidence score between 0.0 and 1.0
4. Generate a clear, concise explanation based on the sources

Respond ONLY with a JSON object in this exact format:
{{
    "label": "True" or "False" or "Unclear",
    "confidence": 0.0 to 1.0,
    "explanation": "detailed explanation based on the sources provided, cite specific sources when possible"
}}

Guidelines:
- "True": Claim is accurate and supported by sources
- "False": Claim is inaccurate or misleading, contradicted by sources
- "Unclear": Insufficient information or conflicting evidence
- Confidence should reflect how certain you are based on source quality and agreement
- Explanation should reference specific sources and their verdicts"""
    else:
        prompt = f"""You are a fact-checking assistant. Classify the following claim.

Claim to verify: "{claim}"

Task:
1. Analyze the claim using your knowledge
2. Classify the claim as "True", "False", or "Unclear"
3. Provide a confidence score between 0.0 and 1.0
4. Generate a clear, concise explanation

Respond ONLY with a JSON object in this exact format:
{{
    "label": "True" or "False" or "Unclear",
    "confidence": 0.0 to 1.0,
    "explanation": "detailed explanation of your reasoning"
}}

Guidelines:
- "True": Claim appears to be accurate
- "False": Claim appears to be inaccurate or misleading
- "Unclear": Insufficient information to determine
- Confidence should reflect your certainty level
- Explanation should be clear and informative"""

    try:
        # Invoke Gemini with the prompt and context
        response_text, usage = _invoke_gemini(prompt, context="classification")
        _log_usage_metadata(usage, "classification")

        # Extract the JSON reply from possible codeblock formatting
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        result = json.loads(response_text)
        # Get the label from the result
        label = result.get("label", "Unclear")
        # Get the confidence from the result
        confidence = float(result.get("confidence", 0.5))
        # Get the explanation from the result
        explanation = result.get("explanation", "No explanation provided")

        # Normalize label (case-insensitive, handle synonyms)
        label_upper = label.upper()
        if "TRUE" in label_upper or "ACCURATE" in label_upper:
            label = "True"
        elif "FALSE" in label_upper or "MISLEADING" in label_upper or "INACCURATE" in label_upper:
            label = "False"
        else:
            label = "Unclear"

        # Clamp confidence to [0.0, 1.0]
        # Return the label, confidence, and explanation
        confidence = max(0.0, min(1.0, confidence))

        return label, confidence, explanation
    except Exception as exc:
        # Log a warning if the classification failed
        friendly = _handle_gemini_exception(exc, "classification")
        return "Unclear", 0.5, friendly


async def generate_explanation_from_sources(
    claim: str, sources: List[Dict[str, Optional[str]]]
) -> str:
    """
    Generate a clear, informative explanation based on fact-checking sources
    for a verified claim, without re-generating a classification label.

    Args:
        claim: The claim being verified.
        sources: List of fact-checking sources with verdicts.

    Returns:
        A string with the detailed explanation.
    """
    if not settings.gemini_api_key:
        _log_event(logging.WARNING, "Gemini API key missing", remaining_limit="unknown")
        return "Explanation generation not available (API key not configured)"
    if not GEMINI_AVAILABLE:
        _log_event(logging.WARNING, "google-genai package not installed", remaining_limit="unknown")
        return "Explanation generation not available (Gemini package not installed)"

    # Build context from the top 10 provided sources
    sources_list = []
    for s in sources[:10]:
        snippet = s.get("snippet", "") or ""
        verdict = s.get("verdict", "") or s.get("rating", "") or ""
        source_name = s.get("source", "") or ""
        url = s.get("url", "") or ""
        if snippet or verdict:
            sources_list.append(
                f"- Source: {source_name}\n  Verdict: {verdict}\n  "
                f"Context: {snippet[:300]}\n  URL: {url}"
            )

    # If no sources list, return an error message
    if not sources_list:
        return "No fact-checking sources available for explanation."

    sources_text = "\n\n".join(sources_list)

    # Build the prompt with detailed instructions to generate an explanation
    prompt = f"""You are a fact-checking assistant. Generate a clear, informative explanation based on the provided fact-checking sources.

Claim being verified: "{claim}"

Fact-Checking Sources:
{sources_text}

Task: Generate a comprehensive explanation that:
1. Summarizes what the fact-checking sources found
2. References specific sources and their verdicts
3. Explains the reasoning behind the verdicts
4. Is clear and easy to understand

Respond with ONLY the explanation text (no JSON, no markdown formatting, just plain text)."""

    try:
        # Invoke Gemini with the prompt and context
        response_text, usage = _invoke_gemini(prompt, context="explanation")
        _log_usage_metadata(usage, "explanation")
        # Get the explanation from the result
        explanation = response_text.strip()
    
        return explanation
    except Exception as exc:
        # Log a warning if the explanation generation failed
        friendly = _handle_gemini_exception(exc, "explanation")
        return friendly