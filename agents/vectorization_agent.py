"""
Vectorization Agent.

Converts documents into embeddings using the selected strategy.
"""

from loguru import logger

from core.models.document import Document, Chunk, DocumentAnalysis
from core.vectorization.strategies import VectorizationStrategy
from core.vectorization.chunkers.semantic_chunker import SemanticChunker
from core.vectorization.chunkers.schema_chunker import SchemaChunker
from core.vectorization.chunkers.relational_chunker import RelationalChunker
from core.llm.embedding_client import EmbeddingClient


class VectorizationAgent:
    """
    Agent responsible for vectorizing documents.
    
    Takes a document and a strategy, chunks the content appropriately,
    and generates embeddings for each chunk.
    """
    
    def __init__(self):
        """Initialize the vectorization agent."""
        self.embedding_client = EmbeddingClient()
        self.chunkers = {
            VectorizationStrategy.SEMANTIC_CHUNKING: SemanticChunker(),
            VectorizationStrategy.SCHEMA_AWARE: SchemaChunker(),
            VectorizationStrategy.RELATIONAL: RelationalChunker(),
        }
        logger.info("VectorizationAgent initialized")
    
    def vectorize(
        self, 
        document: Document, 
        strategy: VectorizationStrategy
    ) -> list[Chunk]:
        """
        Vectorize a document using the specified strategy.
        
        Args:
            document: The document to vectorize.
            strategy: The vectorization strategy to use.
            
        Returns:
            List of Chunks with embeddings.
        """
        logger.info(f"Vectorizing document {document.id} with strategy {strategy}")
        
        # Get appropriate chunker
        chunker = self.chunkers.get(strategy)
        if chunker is None:
            logger.warning(f"Unknown strategy {strategy}, using semantic chunking")
            chunker = self.chunkers[VectorizationStrategy.SEMANTIC_CHUNKING]
        
        # Chunk the document
        chunks = chunker.chunk(document)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Generate embeddings
        chunks = self._embed_chunks(chunks)
        
        return chunks
    
    def _embed_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        """Generate embeddings for all chunks."""
        logger.info(f"Generating embeddings for {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            logger.debug(f"Embedding chunk {i+1}/{len(chunks)}")
            embedding = self.embedding_client.embed(chunk.content)
            chunk.embedding = embedding
        
        logger.info("Embedding generation complete")
        return chunks
    
    def chunk_only(
        self, 
        document: Document, 
        strategy: VectorizationStrategy
    ) -> list[Chunk]:
        """
        Chunk a document without generating embeddings.
        
        Args:
            document: The document to chunk.
            strategy: The chunking strategy to use.
            
        Returns:
            List of Chunks without embeddings.
        """
        chunker = self.chunkers.get(strategy, self.chunkers[VectorizationStrategy.SEMANTIC_CHUNKING])
        return chunker.chunk(document)
