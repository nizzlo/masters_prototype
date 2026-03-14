"""
Orchestrator Agent.

Coordinates the entire workflow from file upload to query answering.
"""

import os
from typing import Optional, Any
from loguru import logger

from core.models.document import Document, DocumentAnalysis, QueryResult
from agents.ingestion_agent import IngestionAgent
from agents.understanding_agent import UnderstandingAgent
from agents.vectorization_strategy_agent import VectorizationStrategyAgent
from agents.vectorization_agent import VectorizationAgent
from agents.retrieval_agent import RetrievalAgent
from vector_store.chroma_manager import ChromaManager
from core.llm.ollama_client import OllamaClient
from core.reasoning.prompts import RAG_SYSTEM_PROMPT, build_rag_prompt
from core.reasoning.context_builder import ContextBuilder


class OrchestratorAgent:
    """
    Main orchestrator agent that coordinates the entire pipeline.
    
    Handles:
    1. File processing: ingestion → understanding → strategy → vectorization → storage
    2. Query handling: retrieval → reasoning → response
    """
    
    def __init__(self):
        """Initialize all sub-agents."""
        self.ingestion_agent = IngestionAgent()
        self.understanding_agent = UnderstandingAgent()
        self.strategy_agent = VectorizationStrategyAgent()
        self.vectorization_agent = VectorizationAgent()
        self.retrieval_agent = RetrievalAgent()
        self.chroma_manager = ChromaManager()
        self.llm = OllamaClient()
        self.context_builder = ContextBuilder()
        
        logger.info("OrchestratorAgent initialized with all sub-agents")
    
    def process_file(self, file_path: str, source_name: Optional[str] = None) -> dict[str, Any]:
        """
        Process a file through the complete pipeline.
        
        Pipeline:
        1. Ingest file
        2. Analyze structure
        3. Select vectorization strategy
        4. Generate chunks and embeddings
        5. Store in vector database
        
        Args:
            file_path: Path to the file to process.
            source_name: Original filename to use as source (optional).
            
        Returns:
            Processing result with status and metadata.
        """
        logger.info(f"Processing file: {file_path}")
        result = {
            "file_path": file_path,
            "source_name": source_name or os.path.basename(file_path),
            "status": "pending",
            "steps": {},
        }
        
        try:
            # Step 1: Ingest
            logger.info("Step 1: Ingesting file")
            document = self.ingestion_agent.ingest(file_path, source_name=source_name)
            result["steps"]["ingestion"] = {
                "status": "success",
                "document_id": document.id,
                "content_length": len(document.content),
            }
            
            # Step 2: Analyze
            logger.info("Step 2: Analyzing document structure")
            analysis = self.understanding_agent.analyze(document)
            result["steps"]["understanding"] = {
                "status": "success",
                "document_type": analysis.document_type.value,
                "schema_info": analysis.schema_info is not None,
                "sections": len(analysis.sections) if analysis.sections else 0,
            }
            
            # Step 3: Select strategy
            logger.info("Step 3: Selecting vectorization strategy")
            strategy = self.strategy_agent.select_strategy(analysis)
            result["steps"]["strategy_selection"] = {
                "status": "success",
                "strategy": strategy.value,
            }
            
            # Step 4: Vectorize
            logger.info("Step 4: Generating embeddings")
            chunks = self.vectorization_agent.vectorize(document, strategy)
            result["steps"]["vectorization"] = {
                "status": "success",
                "chunk_count": len(chunks),
            }
            
            # Step 5: Store
            logger.info("Step 5: Storing in vector database")
            self.chroma_manager.add_chunks(chunks)
            result["steps"]["storage"] = {
                "status": "success",
                "chunks_stored": len(chunks),
            }
            
            result["status"] = "success"
            logger.info(f"File processing complete: {document.id}")
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def query(
        self,
        query: str,
        sources: Optional[list[str]] = None,
        k: int = 5,
    ) -> QueryResult:
        """
        Query the knowledge base and generate an answer.
        
        Pipeline:
        1. Retrieve relevant chunks
        2. Build context
        3. Generate answer with LLM
        
        Args:
            query: The user's question.
            sources: Optional list of sources to filter by.
            k: Number of chunks to retrieve.
            
        Returns:
            QueryResult with answer and sources.
        """
        logger.info(f"Processing query: {query}")
        
        # Step 1: Retrieve
        retrieved_chunks = self.retrieval_agent.retrieve(query, k, sources)
        
        if not retrieved_chunks:
            return QueryResult(
                query=query,
                answer="No relevant information found in the knowledge base.",
                retrieved_chunks=[],
                sources=[],
            )
        
        # Step 2: Build context
        context = self.context_builder.build(retrieved_chunks)
        used_sources = self.context_builder.extract_sources(retrieved_chunks)
        
        # Step 3: Generate answer
        prompt = build_rag_prompt(query, context)
        answer = self.llm.generate(prompt, RAG_SYSTEM_PROMPT)
        
        logger.info(f"Generated answer using {len(retrieved_chunks)} chunks from {len(used_sources)} sources")
        
        return QueryResult(
            query=query,
            answer=answer,
            retrieved_chunks=retrieved_chunks,
            sources=used_sources,
        )
    
    def get_stats(self) -> dict[str, Any]:
        """Get knowledge base statistics."""
        return self.chroma_manager.get_stats()
    
    def clear_knowledge_base(self) -> None:
        """Clear all data from the knowledge base."""
        self.chroma_manager.clear()
        logger.info("Knowledge base cleared")
