"""
Semantic chunker for document text.
"""

from typing import Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings
from core.models.document import Document, Chunk, ChunkMetadata


class SemanticChunker:
    """Chunks documents using semantic/recursive text splitting."""
    
    def __init__(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ):
        """
        Initialize the semantic chunker.
        
        Args:
            chunk_size: Maximum size of each chunk.
            chunk_overlap: Number of characters to overlap between chunks.
        """
        self.chunk_size = chunk_size or settings.default_chunk_size
        self.chunk_overlap = chunk_overlap or settings.default_chunk_overlap
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
    
    def chunk(self, document: Document) -> list[Chunk]:
        """
        Split a document into chunks.
        
        Args:
            document: The document to chunk.
            
        Returns:
            List of Chunk objects.
        """
        # Split the content
        text_chunks = self.splitter.split_text(document.content)
        
        chunks = []
        for i, text in enumerate(text_chunks):
            chunk = Chunk(
                id=f"{document.id}_chunk_{i}",
                content=text,
                metadata=ChunkMetadata(
                    document_id=document.id,
                    source=document.metadata.source,
                    chunk_index=i,
                    total_chunks=len(text_chunks),
                ),
            )
            chunks.append(chunk)
        
        return chunks
