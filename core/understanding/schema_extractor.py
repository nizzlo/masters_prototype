"""
Schema extractor for tabular data.
"""

from typing import Any, Optional
import pandas as pd

from core.models.document import Document


class SchemaExtractor:
    """Extracts schema information from tabular data."""
    
    def extract(self, document: Document) -> Optional[dict[str, Any]]:
        """
        Extract schema from a document containing tabular data.
        
        Args:
            document: The document to analyze.
            
        Returns:
            Schema dictionary with column info, or None if not tabular.
        """
        if document.raw_data is None:
            return self._extract_from_content(document)
        
        # Handle DataFrame
        if isinstance(document.raw_data, pd.DataFrame):
            return self._extract_from_dataframe(document.raw_data)
        
        # Handle dict of DataFrames (Excel with multiple sheets)
        if isinstance(document.raw_data, dict):
            schemas = {}
            for sheet_name, df in document.raw_data.items():
                if isinstance(df, pd.DataFrame):
                    schemas[sheet_name] = self._extract_from_dataframe(df)
            return {"sheets": schemas} if schemas else None
        
        return None
    
    def _extract_from_dataframe(self, df: pd.DataFrame) -> dict[str, Any]:
        """Extract schema from a pandas DataFrame."""
        columns = []
        for col in df.columns:
            col_info = {
                "name": str(col),
                "dtype": str(df[col].dtype),
                "non_null_count": int(df[col].notna().sum()),
                "null_count": int(df[col].isna().sum()),
                "unique_count": int(df[col].nunique()),
            }
            
            # Add sample values
            non_null_values = df[col].dropna()
            if len(non_null_values) > 0:
                col_info["sample_values"] = non_null_values.head(3).tolist()
            
            columns.append(col_info)
        
        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": columns,
        }
    
    def _extract_from_content(self, document: Document) -> Optional[dict[str, Any]]:
        """Extract schema from document content (fallback)."""
        if document.metadata.columns:
            return {
                "row_count": document.metadata.row_count,
                "column_count": document.metadata.column_count,
                "columns": [{"name": col} for col in document.metadata.columns],
            }
        return None
