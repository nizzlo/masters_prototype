"""
Data Ingestion Agent.

Handles file parsing and extraction for various file formats.
Detects file type, parses content, and creates standardized document objects.
"""

from pathlib import Path
from typing import Optional
from loguru import logger

from core.models.document import Document, FileType
from core.ingestion.parser_base import BaseParser
from core.ingestion.parsers.csv_parser import CSVParser
from core.ingestion.parsers.excel_parser import ExcelParser
from core.ingestion.parsers.pdf_parser import PDFParser
from core.ingestion.parsers.docx_parser import WordParser
from core.ingestion.parsers.txt_parser import TextParser
from config import SUPPORTED_EXTENSIONS


class IngestionAgent:
    """
    Agent responsible for ingesting and parsing files.
    
    This agent detects file types and routes them to appropriate parsers
    to create standardized Document objects.
    """
    
    def __init__(self):
        """Initialize the ingestion agent with all available parsers."""
        self.parsers: list[BaseParser] = [
            CSVParser(),
            ExcelParser(),
            PDFParser(),
            WordParser(),
            TextParser(),
        ]
        logger.info("IngestionAgent initialized with parsers: " + 
                   ", ".join([p.__class__.__name__ for p in self.parsers]))
    
    def detect_file_type(self, file_path: str) -> FileType:
        """
        Detect the type of a file based on its extension.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            FileType enum value.
        """
        ext = Path(file_path).suffix.lower()
        
        if ext in [".csv"]:
            return FileType.CSV
        elif ext in [".xlsx", ".xls"]:
            return FileType.EXCEL
        elif ext in [".pdf"]:
            return FileType.PDF
        elif ext in [".docx", ".doc"]:
            return FileType.WORD
        elif ext in [".txt", ".md"]:
            return FileType.TEXT
        else:
            return FileType.UNKNOWN
    
    def get_parser(self, file_path: str) -> Optional[BaseParser]:
        """
        Get the appropriate parser for a file.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            A parser that can handle the file, or None if unsupported.
        """
        for parser in self.parsers:
            if parser.can_parse(file_path):
                return parser
        return None
    
    def ingest(self, file_path: str) -> Document:
        """
        Ingest a file and return a Document object.
        
        This is the main entry point for the ingestion agent.
        
        Args:
            file_path: Path to the file to ingest.
            
        Returns:
            A Document object with extracted content and metadata.
            
        Raises:
            ValueError: If the file type is not supported.
            FileNotFoundError: If the file does not exist.
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        logger.info(f"Ingesting file: {file_path}")
        
        # Detect file type
        file_type = self.detect_file_type(file_path)
        logger.debug(f"Detected file type: {file_type}")
        
        # Get appropriate parser
        parser = self.get_parser(file_path)
        
        if parser is None:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        
        logger.debug(f"Using parser: {parser.__class__.__name__}")
        
        # Parse the file
        document = parser.parse(file_path)
        
        logger.info(f"Successfully ingested document: {document.id}")
        logger.debug(f"Document metadata: {document.metadata}")
        
        return document
    
    def ingest_multiple(self, file_paths: list[str]) -> list[Document]:
        """
        Ingest multiple files.
        
        Args:
            file_paths: List of file paths to ingest.
            
        Returns:
            List of Document objects.
        """
        documents = []
        for file_path in file_paths:
            try:
                doc = self.ingest(file_path)
                documents.append(doc)
            except Exception as e:
                logger.error(f"Failed to ingest {file_path}: {e}")
        return documents
    
    def get_supported_extensions(self) -> list[str]:
        """Get list of all supported file extensions."""
        extensions = []
        for parser in self.parsers:
            extensions.extend(parser.supported_extensions)
        return extensions
