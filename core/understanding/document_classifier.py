"""
Document classifier for detecting document types.
"""

from core.models.document import Document, DocumentType


class DocumentClassifier:
    """Classifies documents into types: tabular, document, structured."""
    
    def classify(self, document: Document) -> DocumentType:
        """
        Classify a document based on its content and metadata.
        
        Args:
            document: The document to classify.
            
        Returns:
            DocumentType enum value.
        """
        # If already classified, return existing type
        if document.metadata.document_type != DocumentType.UNKNOWN:
            return document.metadata.document_type
        
        # Check for tabular indicators
        if self._is_tabular(document):
            return DocumentType.TABULAR
        
        # Check for structured data indicators
        if self._is_structured(document):
            return DocumentType.STRUCTURED
        
        # Default to document
        return DocumentType.DOCUMENT
    
    def _is_tabular(self, document: Document) -> bool:
        """Check if document contains tabular data."""
        # Has columns metadata
        if document.metadata.columns and len(document.metadata.columns) > 0:
            return True
        
        # Has row/column counts
        if document.metadata.row_count and document.metadata.column_count:
            return True
        
        # Raw data is a DataFrame
        if document.raw_data is not None:
            try:
                import pandas as pd
                if isinstance(document.raw_data, pd.DataFrame):
                    return True
                if isinstance(document.raw_data, dict):
                    # Check if dict of DataFrames (Excel with multiple sheets)
                    for v in document.raw_data.values():
                        if isinstance(v, pd.DataFrame):
                            return True
            except ImportError:
                pass
        
        return False
    
    def _is_structured(self, document: Document) -> bool:
        """Check if document contains structured data like JSON/XML."""
        content = document.content.strip()
        
        # Check for JSON-like structure
        if content.startswith('{') or content.startswith('['):
            return True
        
        # Check for XML-like structure
        if content.startswith('<?xml') or content.startswith('<'):
            return True
        
        return False
