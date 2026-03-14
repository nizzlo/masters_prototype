"""
Central configuration for the Adaptive Knowledge System.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Ollama Configuration
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    reasoning_model: str = Field(default="llama3.2:1b", env="REASONING_MODEL")
    embedding_model: str = Field(default="nomic-embed-text", env="EMBEDDING_MODEL")
    
    # ChromaDB Configuration
    chroma_persist_directory: str = Field(default="./vector_store/chroma_db", env="CHROMA_PERSIST_DIR")
    chroma_collection_name: str = Field(default="knowledge_base", env="CHROMA_COLLECTION_NAME")
    
    # Vectorization Settings
    default_chunk_size: int = Field(default=1024, env="DEFAULT_CHUNK_SIZE")
    default_chunk_overlap: int = Field(default=100, env="DEFAULT_CHUNK_OVERLAP")
    
    # Retrieval Settings
    default_top_k: int = Field(default=5, env="DEFAULT_TOP_K")
    
    # API Settings
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    
    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()


# Vectorization Strategies
class VectorizationStrategy:
    SEMANTIC_CHUNKING = "semantic_chunking"
    SCHEMA_AWARE = "schema_aware_embedding"
    RELATIONAL = "relational_embedding"
    
    ALL_STRATEGIES = [SEMANTIC_CHUNKING, SCHEMA_AWARE, RELATIONAL]


# Document Types
class DocumentType:
    TABULAR = "tabular"
    DOCUMENT = "document"
    STRUCTURED = "structured"
    UNKNOWN = "unknown"


# Supported File Extensions
SUPPORTED_EXTENSIONS = {
    ".csv": "csv",
    ".xlsx": "excel",
    ".xls": "excel",
    ".pdf": "pdf",
    ".docx": "word",
    ".doc": "word",
    ".txt": "text",
    ".md": "text",
}
