from typing import Any, Dict, List

from transformers import pipeline

from src.app.core.config import settings


class ClaimClassificationService:
    """Service for classifying claims using transformers pipeline."""

    def __init__(self) -> None:
        self.model_name = settings.classification_model
        self.classifier = None
        # Candidate labels and keyword vocabularies are configured via config/local.yaml
        self.candidate_labels = settings.classification_candidate_labels
        self._load_model()
        self._setup_keywords()

    def _load_model(self) -> None:
        """Load the classification model."""
        try:
            # Load the classification model using the pipeline from transformers
            self.classifier = pipeline("zero-shot-classification", model=self.model_name)
        except Exception as e:
            print(f"Error loading classification model: {e}")
            raise

    def _setup_keywords(self) -> None:
        """Setup keyword lists for fast classification from static configuration."""

        # True keywords
        self.true_keywords = settings.classification_true_keywords
        # False/misleading keywords
        self.false_misleading_keywords = settings.classification_false_keywords
        # No info keywords
        self.no_info_keywords = settings.classification_no_info_keywords

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
            # Get original rating from the claim
            original_rating = claim.get("rating", "")
            # If original rating is not a string, convert it to a string
            if not isinstance(original_rating, str):
                original_rating = str(original_rating) if original_rating is not None else ""

            # Classify the claim using both text and original rating
            normalized_rating = self.classify_claim(claim_text, original_rating)
            # Add the normalized rating to the classified claim
            classified_claim["normalized_rating"] = normalized_rating

            # Add the classified claim to the list of classified claims
            classified_claims.append(classified_claim)

        return classified_claims

    def get_classification_labels(self) -> List[str]:
        """Get available classification labels"""
        # Return a copy of the candidate labels
        return self.candidate_labels.copy()