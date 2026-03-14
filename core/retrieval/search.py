"""
Search functionality for the retrieval system.
"""

from typing import Optional, Any

from core.models.document import RetrievedChunk
from core.llm.embedding_client import EmbeddingClient
from vector_store.chroma_manager import ChromaManager
from config import settings


class SearchEngine:
    """Handles similarity search operations."""
    
    def __init__(self):
        """Initialize the search engine."""
        self.embedding_client = EmbeddingClient()
        self.chroma_manager = ChromaManager()
    
    def search(
        self,
        query: str,
        k: Optional[int] = None,
        sources: Optional[list[str]] = None,
    ) -> list[RetrievedChunk]:
        """
        Search for relevant chunks.
        
        Args:
            query: The search query.
            k: Number of results to return.
            sources: Optional list of sources to filter by.
            
        Returns:
            List of retrieved chunks.
        """
        k = k or settings.default_top_k
        
        # Generate query embedding
        query_embedding = self.embedding_client.embed_query(query)
        
        # Search
        if sources:
            return self.chroma_manager.search_by_sources(query_embedding, sources, k)
        else:
            return self.chroma_manager.search(query_embedding, k)
    
    def get_stats(self) -> dict[str, Any]:
        """Get search engine statistics."""
        return self.chroma_manager.get_stats()
