"""
Data Understanding Agent.

Analyzes document structure and metadata to prepare for vectorization.
"""

from loguru import logger

from core.models.document import Document, DocumentAnalysis, DocumentType
from core.understanding.document_classifier import DocumentClassifier
from core.understanding.schema_extractor import SchemaExtractor
from core.understanding.section_detector import SectionDetector


class UnderstandingAgent:
    """
    Agent responsible for analyzing document structure and metadata.
    
    This agent classifies documents, extracts schemas for tabular data,
    and detects sections for documents.
    """
    
    def __init__(self):
        """Initialize the understanding agent with analyzers."""
        self.classifier = DocumentClassifier()
        self.schema_extractor = SchemaExtractor()
        self.section_detector = SectionDetector()
        logger.info("UnderstandingAgent initialized")
    
    def analyze(self, document: Document) -> DocumentAnalysis:
        """
        Analyze a document's structure and content.
        
        Args:
            document: The document to analyze.
            
        Returns:
            DocumentAnalysis with classification and structural info.
        """
        logger.info(f"Analyzing document: {document.id}")
        
        # Classify document type
        doc_type = self.classifier.classify(document)
        logger.debug(f"Document classified as: {doc_type}")
        
        # Extract schema for tabular data
        schema_info = None
        if doc_type == DocumentType.TABULAR:
            schema_info = self.schema_extractor.extract(document)
            logger.debug(f"Extracted schema: {schema_info}")
        
        # Detect sections for documents
        sections = None
        if doc_type == DocumentType.DOCUMENT:
            sections = self.section_detector.detect(document)
            logger.debug(f"Detected sections: {sections}")
        
        # Create analysis result
        analysis = DocumentAnalysis(
            document_id=document.id,
            document_type=doc_type,
            schema_info=schema_info,
            sections=sections,
        )
        
        logger.info(f"Analysis complete for document: {document.id}")
        return analysis
    
    def analyze_multiple(self, documents: list[Document]) -> list[DocumentAnalysis]:
        """
        Analyze multiple documents.
        
        Args:
            documents: List of documents to analyze.
            
        Returns:
            List of DocumentAnalysis objects.
        """
        return [self.analyze(doc) for doc in documents]
