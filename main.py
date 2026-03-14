"""
Adaptive Knowledge System - Main Entry Point

This system automatically converts heterogeneous enterprise data into a 
vectorized knowledge base that can be queried by an AI agent.
"""

import argparse
import sys
from loguru import logger

from config import settings


def setup_logging():
    """Configure logging with loguru."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level="DEBUG"
    )


def run_api():
    """Start the FastAPI server."""
    import uvicorn
    from api.server import app
    
    logger.info(f"Starting API server on {settings.api_host}:{settings.api_port}")
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)


def run_ui():
    """Start the Streamlit UI."""
    import subprocess
    
    logger.info("Starting Streamlit UI...")
    subprocess.run(["streamlit", "run", "ui/streamlit_app.py"])


def process_file(file_path: str):
    """Process a single file through the pipeline."""
    from agents.orchestrator_agent import OrchestratorAgent
    
    logger.info(f"Processing file: {file_path}")
    orchestrator = OrchestratorAgent()
    result = orchestrator.process_file(file_path)
    logger.info(f"Processing complete: {result}")
    return result


def query_knowledge_base(query: str, sources: list[str] | None = None):
    """Query the knowledge base."""
    from agents.orchestrator_agent import OrchestratorAgent
    
    logger.info(f"Query: {query}")
    orchestrator = OrchestratorAgent()
    result = orchestrator.query(query, sources=sources)
    print(f"\nAnswer: {result['answer']}")
    print(f"\nSources: {result['sources']}")
    return result


def main():
    """Main entry point."""
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description="Adaptive Knowledge System - Automated vectorization and RAG"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # API command
    api_parser = subparsers.add_parser("api", help="Start the FastAPI server")
    
    # UI command
    ui_parser = subparsers.add_parser("ui", help="Start the Streamlit UI")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process a file")
    process_parser.add_argument("file", help="Path to the file to process")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the knowledge base")
    query_parser.add_argument("question", help="Question to ask")
    query_parser.add_argument("--sources", nargs="*", help="Filter by specific sources")
    
    args = parser.parse_args()
    
    if args.command == "api":
        run_api()
    elif args.command == "ui":
        run_ui()
    elif args.command == "process":
        process_file(args.file)
    elif args.command == "query":
        query_knowledge_base(args.question, args.sources)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
