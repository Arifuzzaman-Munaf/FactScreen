import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any
from src.app.core.config import settings


class SimilarityFilterService:
    """Service for filtering claims based on similarity to query using sentence transformers"""

    def __init__(self):
        self.model_name = settings.sentence_transformer_model
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            print(f"Error loading sentence transformer model: {e}")
            raise

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors
        Args:
            a: First vector
            b: Second vector

        Returns:
            Cosine similarity score
        """
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

    def filter_claims_by_similarity(
        self, claims: List[Dict[str, Any]], query: str, similarity_threshold: float = None
    ) -> List[Dict[str, Any]]:
        """
        Filter claims by similarity threshold to the query

        Args:
            claims: List of claim dictionaries
            query: Search query string
            similarity_threshold: Minimum similarity score to keep (default from settings)

        Returns:
            List of filtered claims with similarity scores
        """
        # If similarity threshold is not provided, use the default from settings
        if similarity_threshold is None:
            similarity_threshold = settings.similarity_threshold

        # If no claims are provided, return an empty list
        if not claims:
            return []

        # Extract claim texts
        claim_texts = []
        for claim in claims:
            claim_text = claim.get("claim", "")
            if not isinstance(claim_text, str):
                claim_text = str(claim_text) if claim_text is not None else ""
            claim_texts.append(claim_text)

        # Generate embeddings using the sentence transformer model
        try:
            query_embedding = self.model.encode([query])[0]
            claim_embeddings = self.model.encode(claim_texts)
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []

        # Calculate similarity scores and filter
        filtered_claims = []
        for i, claim in enumerate(claims):
            similarity_score = self.cosine_similarity(query_embedding, claim_embeddings[i])

            if similarity_score >= similarity_threshold:
                # Add similarity score to the claim
                filtered_claim = claim.copy()
                filtered_claim["query_similarity_score"] = similarity_score
                filtered_claims.append(filtered_claim)

        # Sort by similarity score (descending)
        filtered_claims.sort(key=lambda x: x["query_similarity_score"], reverse=True)

        return filtered_claims

    def filter_claims_dataframe(
        self, df: pd.DataFrame, query: str, similarity_threshold: float = None
    ) -> pd.DataFrame:
        """
        Filter claims DataFrame by similarity threshold to the query

        Args:
            df: Pandas DataFrame with a 'claim' column
            query: Search query string
            similarity_threshold: Minimum similarity score to keep

        Returns:
            Filtered DataFrame with similarity scores
        """
        if similarity_threshold is None:
            similarity_threshold = settings.similarity_threshold

        if "claim" not in df.columns:
            raise ValueError("DataFrame must have a 'claim' column.")

        claim_texts = df["claim"].fillna("").tolist()

        try:
            query_embedding = self.model.encode([query])[0]
            claim_embeddings = self.model.encode(claim_texts)
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return pd.DataFrame()

        # Calculate similarity scores
        scores = [self.cosine_similarity(query_embedding, emb) for emb in claim_embeddings]

        # Add scores to DataFrame and filter
        df_with_scores = df.copy()
        df_with_scores["query_similarity_score"] = scores
        filtered_df = df_with_scores[
            df_with_scores["query_similarity_score"] >= similarity_threshold
        ]
        filtered_df = filtered_df.sort_values("query_similarity_score", ascending=False)

        return filtered_df.reset_index(drop=True)