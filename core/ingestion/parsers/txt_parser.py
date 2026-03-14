"""
Plain text file parser.
"""

from pathlib import Path

from core.ingestion.parser_base import BaseParser
from core.models.document import Document, DocumentMetadata, FileType, DocumentType


class TextParser(BaseParser):
    """Parser for plain text files (.txt, .md)."""
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".txt", ".md"]
    
    @property
    def file_type(self) -> FileType:
        return FileType.TEXT
    
    def parse(self, file_path: str) -> Document:
        """Parse a text file into a Document."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Detect sections from markdown headings if .md
        sections = None
        if file_path.endswith('.md'):
            sections = self._extract_markdown_sections(content)
        
        # Build metadata
        metadata = self._create_base_metadata(file_path)
        metadata.document_type = DocumentType.DOCUMENT
        metadata.sections = sections
        
        return Document(
            id=self._generate_document_id(file_path),
            content=content,
            metadata=metadata,
        )
    
    def _extract_markdown_sections(self, content: str) -> list[str]:
        """Extract section headings from markdown content."""
        sections = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                # Remove # symbols and whitespace
                heading = line.lstrip('#').strip()
                if heading:
                    sections.append(heading)
        return sections if sections else None
