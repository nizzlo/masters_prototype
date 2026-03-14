"""
Document models for the Adaptive Knowledge System.

These Pydantic models define the standardized data structures used throughout
the system for representing documents, chunks, and metadata.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    """Types of documents the system can process."""
    TABULAR = "tabular"
    DOCUMENT = "document"
    STRUCTURED = "structured"
    UNKNOWN = "unknown"


class FileType(str, Enum):
    """Supported file types."""
    CSV = "csv"
    EXCEL = "excel"
    PDF = "pdf"
    WORD = "word"
    TEXT = "text"
    UNKNOWN = "unknown"


class DocumentMetadata(BaseModel):
    """Metadata associated with a document."""
    source: str = Field(..., description="Original file path or name")
    file_type: FileType = Field(..., description="Type of the source file")
    document_type: DocumentType = Field(default=DocumentType.UNKNOWN, description="Classified document type")
    created_at: datetime = Field(default_factory=datetime.now, description="When the document was ingested")
    file_size: Optional[int] = Field(default=None, description="File size in bytes")
    page_count: Optional[int] = Field(default=None, description="Number of pages (for PDFs)")
    row_count: Optional[int] = Field(default=None, description="Number of rows (for tabular data)")
    column_count: Optional[int] = Field(default=None, description="Number of columns (for tabular data)")
    columns: Optional[list[str]] = Field(default=None, description="Column names (for tabular data)")
    sections: Optional[list[str]] = Field(default=None, description="Document sections (for documents)")
    extra: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Document(BaseModel):
    """Represents a parsed document ready for processing."""
    id: str = Field(..., description="Unique document identifier")
    content: str = Field(..., description="Raw text content of the document")
    metadata: DocumentMetadata = Field(..., description="Document metadata")
    raw_data: Optional[Any] = Field(default=None, description="Original parsed data (e.g., DataFrame for tabular)")


class ChunkMetadata(BaseModel):
    """Metadata associated with a document chunk."""
    document_id: str = Field(..., description="Parent document ID")
    source: str = Field(..., description="Original file source")
    chunk_index: int = Field(..., description="Index of this chunk within the document")
    total_chunks: int = Field(..., description="Total number of chunks from the document")
    section: Optional[str] = Field(default=None, description="Section this chunk belongs to")
    row_range: Optional[tuple[int, int]] = Field(default=None, description="Row range for tabular chunks")
    extra: dict[str, Any] = Field(default_factory=dict, description="Additional chunk metadata")


class Chunk(BaseModel):
    """Represents a chunk of text ready for embedding."""
    id: str = Field(..., description="Unique chunk identifier")
    content: str = Field(..., description="Text content of the chunk")
    metadata: ChunkMetadata = Field(..., description="Chunk metadata")
    embedding: Optional[list[float]] = Field(default=None, description="Vector embedding")


class DocumentAnalysis(BaseModel):
    """Result of analyzing a document's structure."""
    document_id: str = Field(..., description="ID of the analyzed document")
    document_type: DocumentType = Field(..., description="Classified document type")
    schema_info: Optional[dict[str, Any]] = Field(default=None, description="Schema for tabular data")
    sections: Optional[list[str]] = Field(default=None, description="Detected sections")
    key_entities: Optional[list[str]] = Field(default=None, description="Key entities found")
    summary: Optional[str] = Field(default=None, description="Brief summary of content")
    recommended_strategy: Optional[str] = Field(default=None, description="Recommended vectorization strategy")


class VectorEntry(BaseModel):
    """Represents an entry in the vector database."""
    id: str = Field(..., description="Unique vector ID")
    vector: list[float] = Field(..., description="Embedding vector")
    content: str = Field(..., description="Original text content")
    metadata: dict[str, Any] = Field(..., description="Associated metadata")


class RetrievedChunk(BaseModel):
    """A chunk retrieved from the vector database."""
    id: str = Field(..., description="Chunk ID")
    content: str = Field(..., description="Text content")
    source: str = Field(..., description="Source document")
    score: float = Field(..., description="Similarity score")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class QueryResult(BaseModel):
    """Result of a query to the knowledge base."""
    query: str = Field(..., description="Original query")
    answer: str = Field(..., description="Generated answer")
    retrieved_chunks: list[RetrievedChunk] = Field(..., description="Retrieved context chunks")
    sources: list[str] = Field(..., description="Source documents used")
    confidence: Optional[float] = Field(default=None, description="Confidence score")
