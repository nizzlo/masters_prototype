"""
Ollama embedding client for generating text embeddings.
"""

import ollama
from typing import Optional
from loguru import logger

from config import settings


class EmbeddingClient:
    """Client for generating embeddings using Ollama."""
    
    def __init__(self, model: Optional[str] = None):
        """
        Initialize the embedding client.
        
        Args:
            model: Model name to use. Defaults to settings.embedding_model.
        """
        self.model = model or settings.embedding_model
        logger.info(f"EmbeddingClient initialized with model: {self.model}")
    
    def embed(self, text: str) -> list[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed.
            
        Returns:
            List of floats representing the embedding vector.
        """
        try:
            response = ollama.embeddings(
                model=self.model,
                prompt=text,
            )
            return response['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed.
            
        Returns:
            List of embedding vectors.
        """
        embeddings = []
        for i, text in enumerate(texts):
            logger.debug(f"Embedding text {i+1}/{len(texts)}")
            embedding = self.embed(text)
            embeddings.append(embedding)
        return embeddings
    
    def embed_query(self, query: str) -> list[float]:
        """
        Generate embedding for a query (alias for embed).
        
        Args:
            query: Query text to embed.
            
        Returns:
            Embedding vector.
        """
        return self.embed(query)
