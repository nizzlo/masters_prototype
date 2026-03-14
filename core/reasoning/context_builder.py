"""
Context builder for RAG.
"""

from core.models.document import RetrievedChunk


class ContextBuilder:
    """Builds context from retrieved chunks."""
    
    def __init__(self, max_context_length: int = 8000):
        """
        Initialize the context builder.
        
        Args:
            max_context_length: Maximum character length for context.
        """
        self.max_context_length = max_context_length
    
    def build(self, chunks: list[RetrievedChunk]) -> str:
        """
        Build context string from retrieved chunks.
        
        Args:
            chunks: List of retrieved chunks.
            
        Returns:
            Formatted context string.
        """
        if not chunks:
            return "No relevant context found."
        
        context_parts = []
        current_length = 0
        
        for i, chunk in enumerate(chunks):
            chunk_text = f"[Source: {chunk.source}]\n{chunk.content}"
            chunk_length = len(chunk_text)
            
            if current_length + chunk_length > self.max_context_length:
                # Truncate if needed
                remaining = self.max_context_length - current_length
                if remaining > 100:  # Only add if meaningful amount of space
                    chunk_text = chunk_text[:remaining] + "..."
                    context_parts.append(chunk_text)
                break
            
            context_parts.append(chunk_text)
            current_length += chunk_length + 10  # Account for separator
        
        return "\n\n---\n\n".join(context_parts)
    
    def extract_sources(self, chunks: list[RetrievedChunk]) -> list[str]:
        """Extract unique sources from chunks."""
        return list(set(chunk.source for chunk in chunks))
