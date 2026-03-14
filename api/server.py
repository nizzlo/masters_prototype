"""
FastAPI server for the Adaptive Knowledge System.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
from loguru import logger

from agents.orchestrator_agent import OrchestratorAgent
from config import settings


# Initialize FastAPI app
app = FastAPI(
    title="Adaptive Knowledge System API",
    description="API for automated vectorization and RAG-based querying",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator (singleton)
orchestrator = OrchestratorAgent()


# Request/Response Models
class QueryRequest(BaseModel):
    """Request model for queries."""
    query: str
    sources: Optional[list[str]] = None
    k: Optional[int] = 5


class QueryResponse(BaseModel):
    """Response model for queries."""
    query: str
    answer: str
    sources: list[str]
    chunks: list[dict]


class UploadResponse(BaseModel):
    """Response model for file uploads."""
    status: str
    file_name: str
    document_id: Optional[str] = None
    steps: dict
    error: Optional[str] = None


class StatsResponse(BaseModel):
    """Response model for statistics."""
    total_vectors: int
    sources: list[str]
    source_count: int


# Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Adaptive Knowledge System API", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a file.
    
    Supported formats: CSV, Excel, PDF, Word, Text
    """
    logger.info(f"Received file upload: {file.filename}")
    
    # Validate file extension
    supported = [".csv", ".xlsx", ".xls", ".pdf", ".docx", ".doc", ".txt", ".md"]
    ext = os.path.splitext(file.filename)[1].lower()
    
    if ext not in supported:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Supported: {supported}",
        )
    
    # Save to temp file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Process the file
        result = orchestrator.process_file(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return UploadResponse(
            status=result["status"],
            file_name=file.filename,
            document_id=result.get("steps", {}).get("ingestion", {}).get("document_id"),
            steps=result.get("steps", {}),
            error=result.get("error"),
        )
    
    except Exception as e:
        logger.error(f"Error processing upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """
    Query the knowledge base.
    
    Optionally filter by specific sources for scoped retrieval.
    """
    logger.info(f"Received query: {request.query}")
    
    try:
        result = orchestrator.query(
            query=request.query,
            sources=request.sources,
            k=request.k or 5,
        )
        
        return QueryResponse(
            query=result.query,
            answer=result.answer,
            sources=result.sources,
            chunks=[
                {
                    "content": chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content,
                    "source": chunk.source,
                    "score": chunk.score,
                }
                for chunk in result.retrieved_chunks
            ],
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get knowledge base statistics."""
    try:
        stats = orchestrator.get_stats()
        return StatsResponse(
            total_vectors=stats["total_vectors"],
            sources=stats["sources"],
            source_count=stats["source_count"],
        )
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/clear")
async def clear_knowledge_base():
    """Clear all data from the knowledge base."""
    try:
        orchestrator.clear_knowledge_base()
        return {"status": "success", "message": "Knowledge base cleared"}
    except Exception as e:
        logger.error(f"Error clearing knowledge base: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
