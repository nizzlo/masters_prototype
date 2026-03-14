"""
Baseline static vectorization pipeline for comparison.
"""

from core.models.document import Document, Chunk
from core.vectorization.chunkers.semantic_chunker import SemanticChunker
from core.llm.embedding_client import EmbeddingClient


class BaselinePipeline:
    """
    Baseline pipeline that uses static semantic chunking for all documents.
    
    This is used for comparison against the adaptive vectorization approach.
    """
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """Initialize the baseline pipeline."""
        self.chunker = SemanticChunker(chunk_size, chunk_overlap)
        self.embedding_client = EmbeddingClient()
    
    def process(self, document: Document) -> list[Chunk]:
        """
        Process a document using static semantic chunking.
        
        Args:
            document: The document to process.
            
        Returns:
            List of chunks with embeddings.
        """
        # Chunk using fixed semantic chunking
        chunks = self.chunker.chunk(document)
        
        # Generate embeddings
        for chunk in chunks:
            chunk.embedding = self.embedding_client.embed(chunk.content)
        
        return chunks
