"""
Base class for all file parsers.

All format-specific parsers inherit from this abstract base class.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional
import uuid
import os

from core.models.document import Document, DocumentMetadata, FileType


class BaseParser(ABC):
    """Abstract base class for file parsers."""
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """List of file extensions this parser supports."""
        pass
    
    @property
    @abstractmethod
    def file_type(self) -> FileType:
        """The FileType this parser handles."""
        pass
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the given file."""
        ext = Path(file_path).suffix.lower()
        return ext in self.supported_extensions
    
    @abstractmethod
    def parse(self, file_path: str) -> Document:
        """
        Parse a file and return a Document object.
        
        Args:
            file_path: Path to the file to parse.
            
        Returns:
            A Document object with extracted content and metadata.
        """
        pass
    
    def _generate_document_id(self, file_path: str) -> str:
        """Generate a unique ID for a document."""
        return f"{Path(file_path).stem}_{uuid.uuid4().hex[:8]}"
    
    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(file_path)
    
    def _create_base_metadata(self, file_path: str) -> DocumentMetadata:
        """Create base metadata common to all file types."""
        return DocumentMetadata(
            source=Path(file_path).name,
            file_type=self.file_type,
            file_size=self._get_file_size(file_path),
        )
