"""
Schema-aware chunker for tabular data.
"""

from typing import Optional
import pandas as pd

from core.models.document import Document, Chunk, ChunkMetadata


class SchemaChunker:
    """Chunks tabular data while preserving schema context."""
    
    def __init__(self, rows_per_chunk: int = 2, include_headers: bool = True):
        """
        Initialize the schema chunker.
        
        Args:
            rows_per_chunk: Number of rows to include in each chunk.
            include_headers: Whether to include column headers in each chunk.
        """
        self.rows_per_chunk = rows_per_chunk
        self.include_headers = include_headers
    
    def chunk(self, document: Document) -> list[Chunk]:
        """
        Split tabular data into chunks.
        
        Args:
            document: The document to chunk (must contain tabular data).
            
        Returns:
            List of Chunk objects.
        """
        if document.raw_data is None:
            # Fall back to content-based chunking
            return self._chunk_from_content(document)
        
        if isinstance(document.raw_data, pd.DataFrame):
            return self._chunk_dataframe(document, document.raw_data)
        
        if isinstance(document.raw_data, dict):
            # Multiple sheets
            all_chunks = []
            for sheet_name, df in document.raw_data.items():
                if isinstance(df, pd.DataFrame):
                    chunks = self._chunk_dataframe(document, df, sheet_name)
                    all_chunks.extend(chunks)
            return all_chunks
        
        return self._chunk_from_content(document)
    
    def _chunk_dataframe(
        self, 
        document: Document, 
        df: pd.DataFrame,
        sheet_name: Optional[str] = None
    ) -> list[Chunk]:
        """Chunk a DataFrame."""
        chunks = []
        total_rows = len(df)
        num_chunks = (total_rows + self.rows_per_chunk - 1) // self.rows_per_chunk
        
        header_text = ""
        if self.include_headers:
            header_text = "Columns: " + ", ".join(df.columns.tolist()) + "\n\n"
        
        for i in range(0, total_rows, self.rows_per_chunk):
            end_idx = min(i + self.rows_per_chunk, total_rows)
            chunk_df = df.iloc[i:end_idx]
            
            # Convert chunk to text
            rows_text = []
            for idx, row in chunk_df.iterrows():
                row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
                rows_text.append(row_text)
            
            content = header_text + "\n".join(rows_text)
            
            chunk_idx = i // self.rows_per_chunk
            chunk = Chunk(
                id=f"{document.id}_chunk_{chunk_idx}",
                content=content,
                metadata=ChunkMetadata(
                    document_id=document.id,
                    source=document.metadata.source,
                    chunk_index=chunk_idx,
                    total_chunks=num_chunks,
                    row_range=(i, end_idx),
                    section=sheet_name,
                ),
            )
            chunks.append(chunk)
        
        return chunks
    
    def _chunk_from_content(self, document: Document) -> list[Chunk]:
        """Fallback: chunk from content text."""
        lines = document.content.split('\n')
        chunks = []
        
        # Simple line-based chunking
        for i in range(0, len(lines), self.rows_per_chunk):
            end_idx = min(i + self.rows_per_chunk, len(lines))
            content = '\n'.join(lines[i:end_idx])
            
            chunk_idx = i // self.rows_per_chunk
            chunk = Chunk(
                id=f"{document.id}_chunk_{chunk_idx}",
                content=content,
                metadata=ChunkMetadata(
                    document_id=document.id,
                    source=document.metadata.source,
                    chunk_index=chunk_idx,
                    total_chunks=(len(lines) + self.rows_per_chunk - 1) // self.rows_per_chunk,
                ),
            )
            chunks.append(chunk)
        
        return chunks
