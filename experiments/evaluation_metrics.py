"""
Evaluation metrics for comparing vectorization approaches.
"""

from typing import Any
from core.models.document import RetrievedChunk


def recall_at_k(
    retrieved: list[RetrievedChunk],
    relevant_ids: set[str],
    k: int,
) -> float:
    """
    Calculate Recall@K.
    
    Args:
        retrieved: List of retrieved chunks.
        relevant_ids: Set of IDs that are relevant.
        k: Number of top results to consider.
        
    Returns:
        Recall score between 0 and 1.
    """
    if not relevant_ids:
        return 0.0
    
    top_k = retrieved[:k]
    retrieved_ids = {chunk.id for chunk in top_k}
    
    hits = len(retrieved_ids & relevant_ids)
    return hits / len(relevant_ids)


def mean_reciprocal_rank(
    retrieved: list[RetrievedChunk],
    relevant_ids: set[str],
) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR).
    
    Args:
        retrieved: List of retrieved chunks.
        relevant_ids: Set of IDs that are relevant.
        
    Returns:
        MRR score between 0 and 1.
    """
    for i, chunk in enumerate(retrieved):
        if chunk.id in relevant_ids:
            return 1.0 / (i + 1)
    return 0.0


def precision_at_k(
    retrieved: list[RetrievedChunk],
    relevant_ids: set[str],
    k: int,
) -> float:
    """
    Calculate Precision@K.
    
    Args:
        retrieved: List of retrieved chunks.
        relevant_ids: Set of IDs that are relevant.
        k: Number of top results to consider.
        
    Returns:
        Precision score between 0 and 1.
    """
    top_k = retrieved[:k]
    if not top_k:
        return 0.0
    
    hits = sum(1 for chunk in top_k if chunk.id in relevant_ids)
    return hits / len(top_k)


class EvaluationResults:
    """Container for evaluation results."""
    
    def __init__(self):
        self.metrics: dict[str, list[float]] = {
            "recall@1": [],
            "recall@3": [],
            "recall@5": [],
            "mrr": [],
            "precision@5": [],
        }
    
    def add_result(
        self,
        retrieved: list[RetrievedChunk],
        relevant_ids: set[str],
    ):
        """Add results for a single query."""
        self.metrics["recall@1"].append(recall_at_k(retrieved, relevant_ids, 1))
        self.metrics["recall@3"].append(recall_at_k(retrieved, relevant_ids, 3))
        self.metrics["recall@5"].append(recall_at_k(retrieved, relevant_ids, 5))
        self.metrics["mrr"].append(mean_reciprocal_rank(retrieved, relevant_ids))
        self.metrics["precision@5"].append(precision_at_k(retrieved, relevant_ids, 5))
    
    def get_averages(self) -> dict[str, float]:
        """Get average scores for all metrics."""
        return {
            name: sum(values) / len(values) if values else 0.0
            for name, values in self.metrics.items()
        }
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "averages": self.get_averages(),
            "raw_scores": self.metrics,
            "num_queries": len(self.metrics["mrr"]),
        }
