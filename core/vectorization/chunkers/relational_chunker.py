"""
Relational chunker for structured data.
"""

from typing import Any
import json

from core.models.document import Document, Chunk, ChunkMetadata


class RelationalChunker:
    """Chunks structured data while preserving relationships."""
    
    def __init__(self, max_depth: int = 3, max_items_per_chunk: int = 5):
        """
        Initialize the relational chunker.
        
        Args:
            max_depth: Maximum depth to traverse in nested structures.
            max_items_per_chunk: Maximum number of related items per chunk.
        """
        self.max_depth = max_depth
        self.max_items_per_chunk = max_items_per_chunk
    
    def chunk(self, document: Document) -> list[Chunk]:
        """
        Split structured data into chunks preserving relationships.
        
        Args:
            document: The document to chunk.
            
        Returns:
            List of Chunk objects.
        """
        # Try to parse content as JSON
        try:
            data = json.loads(document.content)
            return self._chunk_json(document, data)
        except json.JSONDecodeError:
            pass
        
        # Fall back to semantic chunking for non-JSON content
        from core.vectorization.chunkers.semantic_chunker import SemanticChunker
        return SemanticChunker().chunk(document)
    
    def _chunk_json(self, document: Document, data: Any) -> list[Chunk]:
        """Chunk JSON data."""
        chunks = []
        
        if isinstance(data, list):
            # Chunk list items
            for i in range(0, len(data), self.max_items_per_chunk):
                end_idx = min(i + self.max_items_per_chunk, len(data))
                items = data[i:end_idx]
                
                content = self._format_items(items)
                chunk = Chunk(
                    id=f"{document.id}_chunk_{i // self.max_items_per_chunk}",
                    content=content,
                    metadata=ChunkMetadata(
                        document_id=document.id,
                        source=document.metadata.source,
                        chunk_index=i // self.max_items_per_chunk,
                        total_chunks=(len(data) + self.max_items_per_chunk - 1) // self.max_items_per_chunk,
                    ),
                )
                chunks.append(chunk)
        
        elif isinstance(data, dict):
            # Chunk dictionary by top-level keys
            keys = list(data.keys())
            for i in range(0, len(keys), self.max_items_per_chunk):
                end_idx = min(i + self.max_items_per_chunk, len(keys))
                subset_keys = keys[i:end_idx]
                subset = {k: data[k] for k in subset_keys}
                
                content = self._format_dict(subset)
                chunk = Chunk(
                    id=f"{document.id}_chunk_{i // self.max_items_per_chunk}",
                    content=content,
                    metadata=ChunkMetadata(
                        document_id=document.id,
                        source=document.metadata.source,
                        chunk_index=i // self.max_items_per_chunk,
                        total_chunks=(len(keys) + self.max_items_per_chunk - 1) // self.max_items_per_chunk,
                    ),
                )
                chunks.append(chunk)
        
        else:
            # Single value, create one chunk
            chunk = Chunk(
                id=f"{document.id}_chunk_0",
                content=str(data),
                metadata=ChunkMetadata(
                    document_id=document.id,
                    source=document.metadata.source,
                    chunk_index=0,
                    total_chunks=1,
                ),
            )
            chunks.append(chunk)
        
        return chunks
    
    def _format_items(self, items: list) -> str:
        """Format list items as text."""
        lines = []
        for item in items:
            if isinstance(item, dict):
                lines.append(self._format_dict(item))
            else:
                lines.append(str(item))
        return "\n\n".join(lines)
    
    def _format_dict(self, d: dict, depth: int = 0) -> str:
        """Format dictionary as text."""
        if depth >= self.max_depth:
            return json.dumps(d, indent=2)
        
        lines = []
        for key, value in d.items():
            if isinstance(value, dict):
                nested = self._format_dict(value, depth + 1)
                lines.append(f"{key}:\n{nested}")
            elif isinstance(value, list):
                items = ", ".join([str(v) for v in value[:5]])
                if len(value) > 5:
                    items += f"... ({len(value)} total)"
                lines.append(f"{key}: [{items}]")
            else:
                lines.append(f"{key}: {value}")
        
        return "\n".join(lines)
