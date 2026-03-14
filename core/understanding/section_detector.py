"""
Section detector for document content.
"""

import re
from typing import Optional

from core.models.document import Document


class SectionDetector:
    """Detects sections and structure in documents."""
    
    def detect(self, document: Document) -> Optional[list[str]]:
        """
        Detect sections in a document.
        
        Args:
            document: The document to analyze.
            
        Returns:
            List of section headings, or None if no sections detected.
        """
        # Use existing sections if available
        if document.metadata.sections:
            return document.metadata.sections
        
        # Try to detect sections from content
        sections = self._detect_from_content(document.content)
        
        return sections if sections else None
    
    def _detect_from_content(self, content: str) -> list[str]:
        """Detect sections from document content."""
        sections = []
        
        # Detect markdown headings
        md_sections = self._detect_markdown_headings(content)
        if md_sections:
            sections.extend(md_sections)
        
        # Detect numbered sections
        numbered_sections = self._detect_numbered_sections(content)
        if numbered_sections:
            sections.extend(numbered_sections)
        
        # Detect uppercase headings
        uppercase_sections = self._detect_uppercase_headings(content)
        if uppercase_sections:
            sections.extend(uppercase_sections)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_sections = []
        for s in sections:
            if s not in seen:
                seen.add(s)
                unique_sections.append(s)
        
        return unique_sections
    
    def _detect_markdown_headings(self, content: str) -> list[str]:
        """Detect markdown-style headings."""
        pattern = r'^#{1,6}\s+(.+)$'
        matches = re.findall(pattern, content, re.MULTILINE)
        return [m.strip() for m in matches]
    
    def _detect_numbered_sections(self, content: str) -> list[str]:
        """Detect numbered sections like '1. Introduction' or '1.1 Overview'."""
        pattern = r'^[\d]+(?:\.[\d]+)*\.?\s+([A-Z][^\n]+)$'
        matches = re.findall(pattern, content, re.MULTILINE)
        return [m.strip() for m in matches]
    
    def _detect_uppercase_headings(self, content: str) -> list[str]:
        """Detect all-uppercase headings on their own lines."""
        sections = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            # Check if line is all uppercase and reasonably short (heading length)
            if line and line.isupper() and 3 <= len(line) <= 100:
                # Avoid false positives with common acronyms
                if len(line.split()) >= 2 or len(line) > 10:
                    sections.append(line.title())
        
        return sections
