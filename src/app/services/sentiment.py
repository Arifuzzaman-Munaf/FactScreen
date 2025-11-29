from __future__ import annotations

from typing import Iterable, List, Tuple
import asyncio
import os

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

from src.app.core.config import settings


_sentiment_pipeline = None


def _get_model_dir() -> str:
    """Get the model directory path, with environment variable override support."""
    # Allow environment variable to override config (useful for deployment)
    env_dir = os.environ.get("SENTIMENT_MODEL_DIR")
    if env_dir:
        return env_dir
    # Use configured path from local.yaml, resolve relative to project root
    config_dir = settings.sentiment_model_dir
    if os.path.isabs(config_dir):
        return config_dir
    # Resolve relative path from project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    return os.path.join(project_root, config_dir)


def _get_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        # Ensure local model directory exists; try local load first, else download then save locally
        model_dir = _get_model_dir()
        os.makedirs(model_dir, exist_ok=True)
        model_id = settings.sentiment_model_id
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
            model = AutoModelForSequenceClassification.from_pretrained(
                model_dir, local_files_only=True
            )
        except Exception:
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModelForSequenceClassification.from_pretrained(model_id)
            # Save for future local use
            tokenizer.save_pretrained(model_dir)
            model.save_pretrained(model_dir)

        # Create the sentiment analysis pipeline
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
        )
    return _sentiment_pipeline


async def analyze_texts_sentiment(texts: Iterable[str]) -> List[Tuple[str, float]]:
    """Run DistilBERT sentiment on texts.

    Returns list of tuples ("POSITIVE"|"NEGATIVE", score in [0,1])
    Args:
        texts: The texts to analyze.
    Returns:
        A list of tuples ("POSITIVE"|"NEGATIVE", score in [0,1]).
    """
    # Clean the texts by removing whitespace and filtering out non-string values
    cleaned = [t.strip() for t in texts if isinstance(t, str) and t.strip()]
    if not cleaned:
        return []

    # Run the sentiment analysis pipeline in a batch
    def _run_batch(batch: List[str]):
        pipe = _get_pipeline()
        results = pipe(batch, truncation=True, max_length=settings.sentiment_max_length)
        out: List[Tuple[str, float]] = []
        for r in results:
            label = str(r.get("label", "")).upper()
            score = float(r.get("score", 0.0))
            out.append((label, score))
        return out

    # Run synchronously in a worker thread to avoid blocking event loop
    return await asyncio.to_thread(_run_batch, cleaned)


def sentiment_to_label(results: List[Tuple[str, float]]) -> Tuple[str, float]:
    """Aggregate multiple sentiment outputs into a single label and confidence.

    Map POSITIVE→"True" and NEGATIVE→"False". If close, return "Unclear".
    Confidence is the dominant side's normalized score, clamped.
    """
    if not results:
        return "Unclear", settings.sentiment_default_unclear_confidence
    # Sum the scores for positive and negative labels
    pos = sum(score for label, score in results if label.startswith("POS"))
    neg = sum(score for label, score in results if label.startswith("NEG"))
    total = max(1e-6, pos + neg)
    # Calculate the threshold for unclear sentiment
    unclear_threshold = settings.sentiment_unclear_threshold
    # If the difference between positive and negative scores is less than
    # the threshold, return unclear
    if abs(pos - neg) < unclear_threshold * total:
        return "Unclear", settings.sentiment_unclear_confidence
    # Calculate the minimum and maximum confidence
    min_conf = settings.sentiment_min_confidence
    # Calculate the maximum confidence
    max_conf = settings.sentiment_max_confidence
    # If the positive score is greater than the negative score, return true
    if pos > neg:
        # Calculate the confidence
        conf = min(max_conf, max(min_conf, pos / total))
        return "True", float(conf)
    conf = min(max_conf, max(min_conf, neg / total))
    return "False", float(conf)
