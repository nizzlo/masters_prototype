"""
Excel file parser.
"""

import pandas as pd
from pathlib import Path

from core.ingestion.parser_base import BaseParser
from core.models.document import Document, DocumentMetadata, FileType, DocumentType


class ExcelParser(BaseParser):
    """Parser for Excel files (.xlsx, .xls)."""
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".xlsx", ".xls"]
    
    @property
    def file_type(self) -> FileType:
        return FileType.EXCEL
    
    def parse(self, file_path: str) -> Document:
        """Parse an Excel file into a Document."""
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        all_content = []
        total_rows = 0
        all_columns = []
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            sheet_content = self._dataframe_to_text(df, sheet_name)
            all_content.append(sheet_content)
            total_rows += len(df)
            all_columns.extend(df.columns.tolist())
        
        content = "\n\n".join(all_content)
        
        # Build metadata
        metadata = self._create_base_metadata(file_path)
        metadata.document_type = DocumentType.TABULAR
        metadata.row_count = total_rows
        metadata.column_count = len(set(all_columns))
        metadata.columns = list(set(all_columns))
        metadata.extra["sheet_names"] = excel_file.sheet_names
        metadata.extra["sheet_count"] = len(excel_file.sheet_names)
        
        return Document(
            id=self._generate_document_id(file_path),
            content=content,
            metadata=metadata,
            raw_data={sheet: pd.read_excel(excel_file, sheet_name=sheet) for sheet in excel_file.sheet_names},
        )
    
    def _dataframe_to_text(self, df: pd.DataFrame, sheet_name: str) -> str:
        """Convert a DataFrame to a text representation."""
        lines = [f"Sheet: {sheet_name}"]
        lines.append("Columns: " + ", ".join(df.columns.tolist()))
        lines.append("")
        
        for idx, row in df.iterrows():
            row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
            lines.append(row_text)
        
        return "\n".join(lines)
