"""Gemini 2.5 Flash service for classification and explanation generation."""

from typing import List, Dict, Optional, Tuple
import json
import logging
from pathlib import Path

try:
    from google import genai

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

from src.app.core.config import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "gemini.log"

logger = logging.getLogger("gemini")
if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def _log_event(level: int, message: str, **fields: Dict[str, object]) -> None:
    """Log with optional structured context."""
    if fields:
        context = ", ".join(f"{k}={v}" for k, v in fields.items())
        message = f"{message} | {context}"
    logger.log(level, message)


def _log_usage_metadata(usage: object, context: str) -> None:
    """Persist token usage data to the log file."""
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
    """Return user-facing error message and log detailed diagnostics."""
    message = str(exc)
    lower_msg = message.lower()

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

    _log_event(logging.ERROR, f"{context} failed", error=message)
    return f"Error in Gemini {context.lower()}: {message}"


_gemini_client: Optional["genai.Client"] = None


def _get_gemini_client() -> "genai.Client":
    """Create or retrieve the cached Gemini client."""
    global _gemini_client
    if _gemini_client is not None:
        return _gemini_client

    if not GEMINI_AVAILABLE:
        raise RuntimeError("google-genai package not installed")
    if not settings.gemini_api_key:
        raise RuntimeError("Gemini API key not configured")

    _gemini_client = genai.Client(api_key=settings.gemini_api_key)
    return _gemini_client


def _invoke_gemini(prompt: str, context: str) -> Tuple[str, Optional[Dict[str, object]]]:
    """Send a request via google-genai client and return text plus usage metadata."""
    client = _get_gemini_client()

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
        )
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc

    text = getattr(response, "text", None)
    if not text:
        candidates = getattr(response, "candidates", None) or []
        if candidates:
            first = candidates[0]
            content = getattr(first, "content", None) or {}
            parts = content.get("parts", []) if isinstance(content, dict) else []
            text_chunks = [p.get("text", "") for p in parts if isinstance(p, dict)]
            text = "\n".join(text_chunks).strip()
    if not text:
        raise RuntimeError("Gemini returned no text")

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
    Check if the verdicts from third-party fact-checkers align with the claim query.

    Args:
        claim: The original claim query
        verdicts: List of verdict dictionaries with 'snippet', 'verdict', 'rating', etc.

    Returns:
        Tuple of (is_aligned: bool, explanation: str)
    """
    if not GEMINI_AVAILABLE:
        _log_event(logging.WARNING, "google-genai package not installed", remaining_limit="unknown")
        return True, ""
    if not settings.gemini_api_key:
        _log_event(logging.WARNING, "Gemini API key missing", remaining_limit="unknown")
        return True, ""  # If no API key, assume aligned

    # Build context from verdicts - include more details
    verdict_context = []
    for v in verdicts[:5]:  # Use top 5 verdicts
        snippet = v.get("snippet", "") or ""
        title = v.get("title", "") or ""
        verdict = v.get("verdict", "") or v.get("rating", "") or ""
        source = v.get("source", "") or ""
        # The title often contains the actual claim being fact-checked
        # Use title first, then snippet as fallback
        claim_being_checked = title.strip() if title else (snippet[:200] if snippet else "")

        if snippet or verdict or title:
            verdict_context.append(
                f"Source: {source}\n"
                f"Title/Claim Being Fact-Checked: {claim_being_checked}\n"
                f"Verdict/Rating: {verdict}\n"
                f"Full Context: {snippet[:300] if snippet else 'No additional context'}"
            )

    if not verdict_context:
        return True, ""

    context_text = "\n\n".join(verdict_context)

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
        response_text, usage = _invoke_gemini(prompt, context="alignment-check")
        _log_usage_metadata(usage, "alignment-check")

        # Extract JSON from response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        result = json.loads(response_text)
        is_aligned = result.get("aligned", True)
        reason = result.get("reason", "")

        return is_aligned, reason
    except Exception as exc:
        _log_event(
            logging.WARNING,
            "Alignment check failed; assuming aligned",
            error=str(exc),
        )
        # On error, assume aligned to avoid false positives
        return True, ""


async def classify_with_gemini(
    claim: str, sources: Optional[List[Dict[str, Optional[str]]]] = None
) -> Tuple[str, float, str]:
    """
    Classify a claim using Gemini 2.5 Flash and generate explanation.

    Args:
        claim: The claim to classify
        sources: Optional list of fact-checking sources/evidence

    Returns:
        Tuple of (label: "True"|"False"|"Unclear", confidence: float, explanation: str)
    """
    if not settings.gemini_api_key:
        _log_event(logging.WARNING, "Gemini API key missing", remaining_limit="unknown")
        return "Unclear", 0.5, "Gemini API key not configured"
    if not GEMINI_AVAILABLE:
        _log_event(logging.WARNING, "google-genai package not installed", remaining_limit="unknown")
        return "Unclear", 0.5, "Gemini package not installed"

    # Build sources context if provided
    sources_text = ""
    if sources:
        sources_list = []
        for s in sources[:10]:  # Use top 10 sources
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
        response_text, usage = _invoke_gemini(prompt, context="classification")
        _log_usage_metadata(usage, "classification")

        # Extract JSON from response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        result = json.loads(response_text)
        label = result.get("label", "Unclear")
        confidence = float(result.get("confidence", 0.5))
        explanation = result.get("explanation", "No explanation provided")

        # Normalize label
        label_upper = label.upper()
        if "TRUE" in label_upper or "ACCURATE" in label_upper:
            label = "True"
        elif "FALSE" in label_upper or "MISLEADING" in label_upper or "INACCURATE" in label_upper:
            label = "False"
        else:
            label = "Unclear"

        # Clamp confidence
        confidence = max(0.0, min(1.0, confidence))

        return label, confidence, explanation
    except Exception as exc:
        friendly = _handle_gemini_exception(exc, "classification")
        return "Unclear", 0.5, friendly


async def generate_explanation_from_sources(
    claim: str, sources: List[Dict[str, Optional[str]]]
) -> str:
    """
    Generate an explanation based on fact-checking sources without changing classification.

    Args:
        claim: The claim being verified
        sources: List of fact-checking sources with verdicts

    Returns:
        Explanation string based on sources
    """
    if not settings.gemini_api_key:
        _log_event(logging.WARNING, "Gemini API key missing", remaining_limit="unknown")
        return "Explanation generation not available (API key not configured)"
    if not GEMINI_AVAILABLE:
        _log_event(logging.WARNING, "google-genai package not installed", remaining_limit="unknown")
        return "Explanation generation not available (Gemini package not installed)"

    # Build sources context
    sources_list = []
    for s in sources[:10]:  # Use top 10 sources
        snippet = s.get("snippet", "") or ""
        verdict = s.get("verdict", "") or s.get("rating", "") or ""
        source_name = s.get("source", "") or ""
        url = s.get("url", "") or ""
        if snippet or verdict:
            sources_list.append(
                f"- Source: {source_name}\n  Verdict: {verdict}\n  "
                f"Context: {snippet[:300]}\n  URL: {url}"
            )

    if not sources_list:
        return "No fact-checking sources available for explanation."

    sources_text = "\n\n".join(sources_list)

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
        response_text, usage = _invoke_gemini(prompt, context="explanation")
        _log_usage_metadata(usage, "explanation")
        explanation = response_text.strip()
        return explanation
    except Exception as exc:
        friendly = _handle_gemini_exception(exc, "explanation")
        return friendly
