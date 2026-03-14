"""
ChromaDB manager for vector storage operations.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import Optional, Any
from loguru import logger

from config import settings
from core.models.document import Chunk, RetrievedChunk


class ChromaManager:
    """Manages ChromaDB vector database operations."""
    
    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: Optional[str] = None,
    ):
        """
        Initialize the ChromaDB manager.
        
        Args:
            persist_directory: Directory to persist the database.
            collection_name: Name of the collection to use.
        """
        self.persist_directory = persist_directory or settings.chroma_persist_directory
        self.collection_name = collection_name or settings.chroma_collection_name
        
        # Initialize client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        
        logger.info(f"ChromaManager initialized with collection: {self.collection_name}")
    
    def add_chunks(self, chunks: list[Chunk]) -> None:
        """
        Add chunks to the vector database.
        
        Args:
            chunks: List of chunks with embeddings to add.
        """
        if not chunks:
            logger.warning("No chunks to add")
            return
        
        ids = []
        embeddings = []
        documents = []
        metadatas = []
        
        for chunk in chunks:
            if chunk.embedding is None:
                logger.warning(f"Chunk {chunk.id} has no embedding, skipping")
                continue
            
            ids.append(chunk.id)
            embeddings.append(chunk.embedding)
            documents.append(chunk.content)
            metadatas.append({
                "document_id": chunk.metadata.document_id,
                "source": chunk.metadata.source,
                "chunk_index": chunk.metadata.chunk_index,
                "total_chunks": chunk.metadata.total_chunks,
                "section": chunk.metadata.section or "",
            })
        
        if ids:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
            )
            logger.info(f"Added {len(ids)} chunks to collection")
    
    def search(
        self,
        query_embedding: list[float],
        k: int = 5,
        filter_dict: Optional[dict[str, Any]] = None,
    ) -> list[RetrievedChunk]:
        """
        Search for similar chunks.
        
        Args:
            query_embedding: Query embedding vector.
            k: Number of results to return.
            filter_dict: Optional metadata filter.
            
        Returns:
            List of retrieved chunks with similarity scores.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=filter_dict,
            include=["documents", "metadatas", "distances"],
        )
        
        retrieved = []
        if results["ids"] and results["ids"][0]:
            for i, chunk_id in enumerate(results["ids"][0]):
                # Convert distance to similarity score (cosine distance to similarity)
                distance = results["distances"][0][i] if results["distances"] else 0
                score = 1 - distance  # For cosine distance
                
                retrieved.append(RetrievedChunk(
                    id=chunk_id,
                    content=results["documents"][0][i],
                    source=results["metadatas"][0][i].get("source", ""),
                    score=score,
                    metadata=results["metadatas"][0][i],
                ))
        
        return retrieved
    
    def search_by_sources(
        self,
        query_embedding: list[float],
        sources: list[str],
        k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Search within specific source documents.
        
        Args:
            query_embedding: Query embedding vector.
            sources: List of source file names to filter by.
            k: Number of results to return.
            
        Returns:
            List of retrieved chunks.
        """
        filter_dict = {"source": {"$in": sources}}
        return self.search(query_embedding, k, filter_dict)
    
    def get_stats(self) -> dict[str, Any]:
        """Get statistics about the collection."""
        count = self.collection.count()
        
        # Get unique sources
        all_data = self.collection.get(include=["metadatas"])
        sources = set()
        if all_data["metadatas"]:
            for meta in all_data["metadatas"]:
                if meta.get("source"):
                    sources.add(meta["source"])
        
        return {
            "total_vectors": count,
            "sources": list(sources),
            "source_count": len(sources),
        }
    
    def delete_by_source(self, source: str) -> None:
        """Delete all chunks from a specific source."""
        self.collection.delete(where={"source": source})
        logger.info(f"Deleted chunks from source: {source}")
    
    def clear(self) -> None:
        """Clear all data from the collection."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("Collection cleared")
