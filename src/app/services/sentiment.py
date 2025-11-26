from __future__ import annotations

from typing import Iterable, List, Tuple
import asyncio
import os

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


_sentiment_pipeline = None
_MODEL_ID = "distilbert-base-uncased-finetuned-sst-2-english"
_MODEL_DIR = os.environ.get(
    "SENTIMENT_MODEL_DIR",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "distilbert-sst2"),
)


def _get_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        # Ensure local model directory exists; try local load first, else download then save locally
        os.makedirs(_MODEL_DIR, exist_ok=True)
        try:
            tokenizer = AutoTokenizer.from_pretrained(_MODEL_DIR, local_files_only=True)
            model = AutoModelForSequenceClassification.from_pretrained(
                _MODEL_DIR, local_files_only=True
            )
        except Exception:
            tokenizer = AutoTokenizer.from_pretrained(_MODEL_ID)
            model = AutoModelForSequenceClassification.from_pretrained(_MODEL_ID)
            # Save for future local use
            tokenizer.save_pretrained(_MODEL_DIR)
            model.save_pretrained(_MODEL_DIR)

        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
        )
    return _sentiment_pipeline


async def analyze_texts_sentiment(texts: Iterable[str]) -> List[Tuple[str, float]]:
    """Run DistilBERT sentiment on texts.

    Returns list of tuples ("POSITIVE"|"NEGATIVE", score in [0,1]).
    """
    cleaned = [t.strip() for t in texts if isinstance(t, str) and t.strip()]
    if not cleaned:
        return []

    def _run_batch(batch: List[str]):
        pipe = _get_pipeline()
        results = pipe(batch, truncation=True, max_length=256)
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
        return "Unclear", 0.5
    pos = sum(score for label, score in results if label.startswith("POS"))
    neg = sum(score for label, score in results if label.startswith("NEG"))
    total = max(1e-6, pos + neg)
    if abs(pos - neg) < 0.1 * total:
        return "Unclear", 0.55
    if pos > neg:
        conf = min(0.95, max(0.6, pos / total))
        return "True", float(conf)
    conf = min(0.95, max(0.6, neg / total))
    return "False", float(conf)
