"""
Vectorization Strategy Agent.

Uses an LLM to determine the optimal embedding strategy for a document.
"""

from loguru import logger

from core.models.document import DocumentAnalysis, DocumentType
from core.vectorization.strategies import VectorizationStrategy, get_all_strategies
from core.llm.ollama_client import OllamaClient


class VectorizationStrategyAgent:
    """
    Agent responsible for selecting the optimal vectorization strategy.
    
    Uses an LLM to analyze document structure and recommend the best
    approach for embedding the content.
    """
    
    def __init__(self):
        """Initialize the strategy agent."""
        self.llm = OllamaClient()
        logger.info("VectorizationStrategyAgent initialized")
    
    def select_strategy(self, analysis: DocumentAnalysis) -> VectorizationStrategy:
        """
        Select the optimal vectorization strategy for a document.
        
        Args:
            analysis: The document analysis result.
            
        Returns:
            Selected VectorizationStrategy.
        """
        logger.info(f"Selecting strategy for document: {analysis.document_id}")
        
        # Build context for the LLM
        context = self._build_context(analysis)
        
        # Generate prompt
        prompt = self._build_prompt(context)
        
        # Get LLM recommendation
        try:
            response = self.llm.generate(prompt)
            strategy = self._parse_strategy(response)
            logger.info(f"Selected strategy: {strategy}")
            return strategy
        except Exception as e:
            logger.warning(f"LLM strategy selection failed: {e}, using fallback")
            return self._fallback_strategy(analysis)
    
    def _build_context(self, analysis: DocumentAnalysis) -> str:
        """Build context description for the LLM."""
        lines = [f"Document type: {analysis.document_type.value}"]
        
        if analysis.schema_info:
            if "columns" in analysis.schema_info:
                cols = analysis.schema_info["columns"]
                if isinstance(cols, list) and len(cols) > 0:
                    if isinstance(cols[0], dict):
                        col_names = [c.get("name", str(c)) for c in cols]
                    else:
                        col_names = [str(c) for c in cols]
                    lines.append(f"Columns: {', '.join(col_names[:10])}")
            if "row_count" in analysis.schema_info:
                lines.append(f"Row count: {analysis.schema_info['row_count']}")
        
        if analysis.sections:
            lines.append(f"Sections: {', '.join(analysis.sections[:5])}")
        
        return "\n".join(lines)
    
    def _build_prompt(self, context: str) -> str:
        """Build the LLM prompt for strategy selection."""
        strategies = "\n".join([f"{i+1}. {s}" for i, s in enumerate(get_all_strategies())])
        
        return f"""You are selecting a vectorization strategy for a document.

{context}

Choose the best strategy from:

{strategies}

Guidelines:
- Use "semantic_chunking" for text documents, PDFs, Word files
- Use "schema_aware_embedding" for tabular data like CSV, Excel
- Use "relational_embedding" for JSON or structured data with relationships

Return ONLY the strategy name, nothing else."""
    
    def _parse_strategy(self, response: str) -> VectorizationStrategy:
        """Parse the LLM response to extract the strategy."""
        response = response.strip().lower()
        
        # Try exact match
        for strategy in VectorizationStrategy:
            if strategy.value in response:
                return strategy
        
        # Try partial match
        if "semantic" in response:
            return VectorizationStrategy.SEMANTIC_CHUNKING
        if "schema" in response:
            return VectorizationStrategy.SCHEMA_AWARE
        if "relational" in response:
            return VectorizationStrategy.RELATIONAL
        
        # Default
        return VectorizationStrategy.SEMANTIC_CHUNKING
    
    def _fallback_strategy(self, analysis: DocumentAnalysis) -> VectorizationStrategy:
        """Fallback strategy selection without LLM."""
        if analysis.document_type == DocumentType.TABULAR:
            return VectorizationStrategy.SCHEMA_AWARE
        elif analysis.document_type == DocumentType.STRUCTURED:
            return VectorizationStrategy.RELATIONAL
        else:
            return VectorizationStrategy.SEMANTIC_CHUNKING
