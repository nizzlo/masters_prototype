"""
Vectorization strategies enumeration and configuration.
"""

from enum import Enum
from typing import Any


class VectorizationStrategy(str, Enum):
    """Available vectorization strategies."""
    SEMANTIC_CHUNKING = "semantic_chunking"
    SCHEMA_AWARE = "schema_aware_embedding"
    RELATIONAL = "relational_embedding"


# Strategy configurations
STRATEGY_CONFIGS: dict[VectorizationStrategy, dict[str, Any]] = {
    VectorizationStrategy.SEMANTIC_CHUNKING: {
        "description": "Split document into semantic chunks based on content",
        "suitable_for": ["document", "text"],
        "default_chunk_size": 512,
        "default_overlap": 50,
    },
    VectorizationStrategy.SCHEMA_AWARE: {
        "description": "Embed tabular data preserving schema context",
        "suitable_for": ["tabular"],
        "rows_per_chunk": 10,
        "include_headers": True,
    },
    VectorizationStrategy.RELATIONAL: {
        "description": "Preserve relationships in structured data",
        "suitable_for": ["structured", "tabular"],
        "preserve_relations": True,
    },
}


def get_strategy_config(strategy: VectorizationStrategy) -> dict[str, Any]:
    """Get configuration for a strategy."""
    return STRATEGY_CONFIGS.get(strategy, {})


def get_all_strategies() -> list[str]:
    """Get list of all strategy names."""
    return [s.value for s in VectorizationStrategy]
