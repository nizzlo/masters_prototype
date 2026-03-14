"""
Central configuration for the Adaptive Knowledge System.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal
import os
import uuid


# Generate a unique session ID for this instance
SESSION_ID = str(uuid.uuid4())[:8]

# Available reasoning models
AVAILABLE_MODELS = {
    "llama3:8b": {"name": "Llama 3 (8B)", "description": "Best quality, ~5GB RAM", "speed": "slower"},
    "llama3.2:3b": {"name": "Llama 3.2 (3B)", "description": "Balanced, ~2GB RAM", "speed": "medium"},
    "llama3.2:1b": {"name": "Llama 3.2 (1B)", "description": "Fastest, ~1GB RAM", "speed": "fast"},
}


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Ollama Configuration
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    reasoning_model: str = Field(default="llama3:8b", env="REASONING_MODEL")
    embedding_model: str = Field(default="mxbai-embed-large", env="EMBEDDING_MODEL")
    
    # ChromaDB Configuration
    chroma_persist_directory: str = Field(default="./vector_store/chroma_db", env="CHROMA_PERSIST_DIR")
    chroma_collection_name: str = Field(default=f"kb_{SESSION_ID}", env="CHROMA_COLLECTION_NAME")
    
    # Vectorization Settings
    default_chunk_size: int = Field(default=1000, env="DEFAULT_CHUNK_SIZE")
    default_chunk_overlap: int = Field(default=200, env="DEFAULT_CHUNK_OVERLAP")
    
    # Retrieval Settings
    default_top_k: int = Field(default=10, env="DEFAULT_TOP_K")
    
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
