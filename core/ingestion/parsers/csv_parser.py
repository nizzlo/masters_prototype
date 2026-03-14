"""
CSV file parser.
"""

import pandas as pd
from pathlib import Path

from core.ingestion.parser_base import BaseParser
from core.models.document import Document, DocumentMetadata, FileType, DocumentType


class CSVParser(BaseParser):
    """Parser for CSV files."""
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".csv"]
    
    @property
    def file_type(self) -> FileType:
        return FileType.CSV
    
    def parse(self, file_path: str) -> Document:
        """Parse a CSV file into a Document."""
        df = pd.read_csv(file_path)
        
        # Create text representation
        content = self._dataframe_to_text(df)
        
        # Build metadata
        metadata = self._create_base_metadata(file_path)
        metadata.document_type = DocumentType.TABULAR
        metadata.row_count = len(df)
        metadata.column_count = len(df.columns)
        metadata.columns = df.columns.tolist()
        
        return Document(
            id=self._generate_document_id(file_path),
            content=content,
            metadata=metadata,
            raw_data=df,
        )
    
    def _dataframe_to_text(self, df: pd.DataFrame) -> str:
        """Convert a DataFrame to a text representation."""
        lines = []
        
        # Add column headers
        lines.append("Columns: " + ", ".join(df.columns.tolist()))
        lines.append("")
        
        # Add rows as text
        for idx, row in df.iterrows():
            row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
            lines.append(row_text)
        
        return "\n".join(lines)
