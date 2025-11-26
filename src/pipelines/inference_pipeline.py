from transformers import pipeline
from typing import List, Dict, Any
from src.app.core.config import settings


class ClaimClassificationService:
    """Service for classifying claims using transformers pipeline"""

    def __init__(self):
        self.model_name = settings.classification_model
        self.classifier = None
        self.candidate_labels = ["True", "False or Misleading", "Not enough information found"]
        self._load_model()
        self._setup_keywords()

    def _load_model(self):
        """Load the classification model"""
        try:
            self.classifier = pipeline("zero-shot-classification", model=self.model_name)
        except Exception as e:
            print(f"Error loading classification model: {e}")
            raise

    def _setup_keywords(self):
        """Setup keyword lists for fast classification"""
        self.true_keywords = [
            "true",
            "correct",
            "accurate",
            "valid",
            "factual",
            "verified",
            "confirmed",
            "legitimate",
            "proven",
        ]
        self.false_misleading_keywords = [
            "false",
            "misleading",
            "lie",
            "incorrect",
            "debunked",
            "refuted",
            "inaccurate",
            "fabricated",
            "untrue",
            "wrong",
            "fake",
            "hoax",
            "myth",
            "busted",
            "disproven",
        ]
        self.no_info_keywords = [
            "not enough",
            "no evidence",
            "unproven",
            "no proof",
            "inconclusive",
            "unclear",
            "insufficient",
            "unknown",
            "partly true",
            "partially true",
            "mixed",
            "unverified",
        ]

    def fast_keyword_classification(self, text: str) -> str:
        """Fast classification based on keywords"""
        if not isinstance(text, str) or not text.strip():
            return "Not enough information found"

        text_lower = text.lower().strip()

        # Check for false/misleading keywords first (higher priority)
        for keyword in self.false_misleading_keywords:
            if keyword in text_lower:
                return "False or Misleading"

        # Check for true keywords (but avoid false positives)
        for keyword in self.true_keywords:
            if keyword in text_lower:
                # Avoid false positives where "true" appears in "false"
                if keyword == "true" and "false" in text_lower:
                    continue
                # Avoid false positives where "true" appears in "untrue"
                if keyword == "true" and "untrue" in text_lower:
                    continue
                return "True"

        # Check for no info keywords
        for keyword in self.no_info_keywords:
            if keyword in text_lower:
                return "Not enough information found"

        return None  # No keyword match found

    def classify_from_original_rating(self, original_rating: str) -> str:
        """
        Classify based on the original rating from fact-checking sources

        Args:
            original_rating: The original rating from the fact-checking source

        Returns:
            Normalized classification
        """
        if not isinstance(original_rating, str):
            return "Not enough information found"

        rating_lower = original_rating.lower().strip()

        # Check for false/misleading indicators in original rating
        for keyword in self.false_misleading_keywords:
            if keyword in rating_lower:
                return "False or Misleading"

        # Check for true indicators in original rating
        for keyword in self.true_keywords:
            if keyword in rating_lower:
                # Avoid false positives where "true" appears in "false"
                if keyword == "true" and "false" in rating_lower:
                    continue
                # Avoid false positives where "true" appears in "untrue"
                if keyword == "true" and "untrue" in rating_lower:
                    continue
                return "True"

        # Check for no info indicators
        for keyword in self.no_info_keywords:
            if keyword in rating_lower:
                return "Not enough information found"

        # If no keyword match, return None to fall back to other methods
        return None

    def classify_claim(self, text: str, original_rating: str = None) -> str:
        """
        Classify a claim using original rating first, then keyword matching, then transformer model

        Args:
            text: The claim text to classify
            original_rating: The original rating from fact-checking source

        Returns:
            Classification label
        """
        # Priority 1: Check original rating from fact-checking source
        if original_rating:
            rating_result = self.classify_from_original_rating(original_rating)
            if rating_result:
                return rating_result

        # Priority 2: Try fast keyword classification on claim text
        keyword_result = self.fast_keyword_classification(text)
        if keyword_result:
            return keyword_result

        # Priority 3: Fall back to transformer model
        try:
            result = self.classifier(
                text, candidate_labels=self.candidate_labels, multi_label=False
            )
            return result["labels"][0]
        except Exception as e:
            print(f"Error in transformer classification: {e}")
            return "Not enough information found"

    def classify_claims_batch(self, claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Classify a batch of claims

        Args:
            claims: List of claim dictionaries

        Returns:
            List of claims with normalized_rating field added
        """
        classified_claims = []

        for claim in claims:
            classified_claim = claim.copy()

            # Get claim text and original rating
            claim_text = claim.get("claim", "")
            if not isinstance(claim_text, str):
                claim_text = str(claim_text) if claim_text is not None else ""

            original_rating = claim.get("rating", "")
            if not isinstance(original_rating, str):
                original_rating = str(original_rating) if original_rating is not None else ""

            # Classify the claim using both text and original rating
            normalized_rating = self.classify_claim(claim_text, original_rating)
            classified_claim["normalized_rating"] = normalized_rating

            classified_claims.append(classified_claim)

        return classified_claims

    def get_classification_labels(self) -> List[str]:
        """Get available classification labels"""
        return self.candidate_labels.copy()
