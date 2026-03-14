"""
Retrieval Agent.

Handles user queries by searching the vector database.
"""

from typing import Optional
from loguru import logger

from core.models.document import RetrievedChunk
from core.retrieval.search import SearchEngine
from config import settings


class RetrievalAgent:
    """
    Agent responsible for retrieving relevant context from the knowledge base.
    
    Takes a query, embeds it, searches the vector database, and returns
    the most relevant chunks.
    """
    
    def __init__(self):
        """Initialize the retrieval agent."""
        self.search_engine = SearchEngine()
        logger.info("RetrievalAgent initialized")
    
    def retrieve(
        self,
        query: str,
        k: Optional[int] = None,
        sources: Optional[list[str]] = None,
    ) -> list[RetrievedChunk]:
        """
        Retrieve relevant chunks for a query.
        
        Args:
            query: The search query.
            k: Number of results to return.
            sources: Optional list of sources to filter by (scoped retrieval).
            
        Returns:
            List of retrieved chunks sorted by relevance.
        """
        k = k or settings.default_top_k
        
        logger.info(f"Retrieving for query: {query[:50]}...")
        
        if sources:
            logger.info(f"Scoped search with sources: {sources}")
        
        chunks = self.search_engine.search(query, k, sources)
        
        logger.info(f"Retrieved {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            logger.debug(f"  {i+1}. {chunk.source} (score: {chunk.score:.3f})")
        
        return chunks
    
    def format_context(self, chunks: list[RetrievedChunk]) -> str:
        """
        Format retrieved chunks as context for the LLM.
        
        Args:
            chunks: List of retrieved chunks.
            
        Returns:
            Formatted context string.
        """
        if not chunks:
            return "No relevant context found."
        
        context_parts = []
        for i, chunk in enumerate(chunks):
            context_parts.append(f"[Source: {chunk.source}]\n{chunk.content}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def get_sources(self, chunks: list[RetrievedChunk]) -> list[str]:
        """Extract unique sources from retrieved chunks."""
        return list(set(chunk.source for chunk in chunks))
    
    def get_stats(self) -> dict:
        """Get knowledge base statistics."""
        return self.search_engine.get_stats()
