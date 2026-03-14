"""
PDF file parser.
"""

import pdfplumber
from pathlib import Path

from core.ingestion.parser_base import BaseParser
from core.models.document import Document, DocumentMetadata, FileType, DocumentType


class PDFParser(BaseParser):
    """Parser for PDF files."""
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".pdf"]
    
    @property
    def file_type(self) -> FileType:
        return FileType.PDF
    
    def parse(self, file_path: str) -> Document:
        """Parse a PDF file into a Document."""
        pages_text = []
        page_count = 0
        
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
        
        content = "\n\n".join(pages_text)
        
        # Build metadata
        metadata = self._create_base_metadata(file_path)
        metadata.document_type = DocumentType.DOCUMENT
        metadata.page_count = page_count
        
        return Document(
            id=self._generate_document_id(file_path),
            content=content,
            metadata=metadata,
        )
