# Implementation Guide

This document provides comprehensive technical documentation for the Adaptive Knowledge System.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Data Models](#data-models)
4. [Agent Implementations](#agent-implementations)
5. [Core Modules](#core-modules)
6. [Vector Database](#vector-database-chromadb)
7. [API Endpoints](#api-endpoints)
8. [Streamlit UI](#streamlit-ui)
9. [Configuration](#configuration)
10. [RAG Pipeline](#rag-pipeline)
11. [Running the System](#running-the-system)
12. [Evaluation Module](#evaluation-module)
13. [Dependencies](#dependencies)
14. [Extension Points](#extension-points)

---

## Architecture Overview

The system follows an **agent-based architecture** with specialized agents coordinated by an Orchestrator. Each agent handles a specific responsibility in the pipeline.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Orchestrator Agent                         │
│       Coordinates the pipeline from ingestion to response       │
└─────────────────────────────────────────────────────────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Ingestion   │   │ Understanding │   │   Retrieval   │
│     Agent     │ → │     Agent     │   │     Agent     │
└───────────────┘   └───────────────┘   └───────────────┘
                            │
                            ▼
                    ┌───────────────┐   ┌───────────────┐
                    │   Strategy    │ → │ Vectorization │
                    │     Agent     │   │     Agent     │
                    └───────────────┘   └───────────────┘
```

### Pipeline Stages

| Stage | Agent | Description |
|-------|-------|-------------|
| 1. Ingestion | `IngestionAgent` | Parse file, extract text, create Document |
| 2. Understanding | `UnderstandingAgent` | Analyze structure, detect type, extract schema |
| 3. Strategy | `VectorizationStrategyAgent` | LLM selects optimal chunking strategy |
| 4. Vectorization | `VectorizationAgent` | Chunk content, generate embeddings |
| 5. Storage | `ChromaManager` | Persist vectors to ChromaDB |
| 6. Retrieval | `RetrievalAgent` | Vector search on user queries |
| 7. Reasoning | `OllamaClient` | Generate RAG-grounded answers |

---

## Directory Structure

```
masters_prototype/
├── agents/                     # Agent implementations
│   ├── orchestrator_agent.py   # Main pipeline coordinator
│   ├── ingestion_agent.py      # File parsing
│   ├── understanding_agent.py  # Document structure analysis
│   ├── vectorization_strategy_agent.py  # LLM strategy selection
│   ├── vectorization_agent.py  # Chunking & embedding generation
│   ├── retrieval_agent.py      # Vector search & query handling
│   └── evaluation_agent.py     # Experiment metrics
│
├── core/                       # Core modules
│   ├── models/
│   │   └── document.py         # Pydantic data models
│   ├── ingestion/
│   │   ├── parser_base.py      # Abstract parser class
│   │   └── parsers/            # Format-specific parsers
│   │       ├── csv_parser.py
│   │       ├── excel_parser.py
│   │       ├── pdf_parser.py
│   │       ├── docx_parser.py
│   │       └── txt_parser.py
│   ├── understanding/
│   │   ├── document_classifier.py
│   │   ├── schema_extractor.py
│   │   └── section_detector.py
│   ├── vectorization/
│   │   ├── strategies.py       # Strategy enum
│   │   └── chunkers/
│   │       ├── semantic_chunker.py
│   │       ├── schema_chunker.py
│   │       └── relational_chunker.py
│   ├── llm/
│   │   ├── ollama_client.py    # LLM client for reasoning
│   │   └── embedding_client.py # Embedding generation
│   ├── retrieval/
│   │   └── search.py           # Similarity search engine
│   └── reasoning/
│       ├── prompts.py          # RAG prompt templates
│       └── context_builder.py  # Context formatting
│
├── vector_store/
│   ├── chroma_manager.py       # ChromaDB operations
│   └── chroma_db/              # Persistent vector storage
│
├── api/
│   └── server.py               # FastAPI REST endpoints
│
├── ui/
│   └── streamlit_app.py        # Streamlit web interface
│
├── experiments/
│   ├── baseline_pipeline.py    # Static chunking baseline
│   └── evaluation_metrics.py   # Recall@K, MRR, Precision@K
│
├── datasets/                   # Sample test data
├── logs/                       # Application logs & PID files
├── config.py                   # Central configuration
├── main.py                     # CLI entry point
├── run.sh                      # Start all services
├── stop.sh                     # Stop all services
└── requirements.txt            # Python dependencies
```

---

## Data Models

All data structures are defined using **Pydantic** in `core/models/document.py`:

### Document

Primary container for parsed file content:

```python
class Document(BaseModel):
    id: str                      # Unique identifier (UUID)
    content: str                 # Raw text content
    metadata: DocumentMetadata   # Source filename, type, timestamps
    raw_data: Optional[Any]      # Original data (e.g., pandas DataFrame)
```

### DocumentMetadata

```python
class DocumentMetadata(BaseModel):
    source: str                  # Original filename
    file_type: str               # Extension (csv, pdf, etc.)
    created_at: datetime         # Processing timestamp
    document_type: DocumentType  # tabular, document, structured
    schema_info: Optional[SchemaInfo]  # For tabular data
    sections: Optional[list[str]]      # For documents
```

### Chunk

Represents a vectorizable text segment:

```python
class Chunk(BaseModel):
    id: str                      # Unique chunk ID
    content: str                 # Text content
    metadata: ChunkMetadata      # Source, position, section
    embedding: Optional[list[float]]  # 1024-dim vector (mxbai-embed-large)
```

### QueryResult

RAG response container:

```python
class QueryResult(BaseModel):
    query: str                   # Original user query
    answer: str                  # LLM-generated answer
    retrieved_chunks: list[RetrievedChunk]  # Context used
    sources: list[str]           # Source documents cited
```

### RetrievedChunk

```python
class RetrievedChunk(BaseModel):
    content: str                 # Chunk text
    source: str                  # Source document
    score: float                 # Similarity score (0-1)
    metadata: dict               # Additional metadata
```

---

## Agent Implementations

### 1. Orchestrator Agent

**File:** `agents/orchestrator_agent.py`

**Purpose:** Coordinate the entire pipeline from file upload to query response.

**Initialization:**
```python
class OrchestratorAgent:
    def __init__(self):
        self.ingestion_agent = IngestionAgent()
        self.understanding_agent = UnderstandingAgent()
        self.strategy_agent = VectorizationStrategyAgent()
        self.vectorization_agent = VectorizationAgent()
        self.retrieval_agent = RetrievalAgent()
        self.chroma_manager = ChromaManager()
        self.llm = OllamaClient()
        self.context_builder = ContextBuilder()
```

**File Processing Pipeline:**
```python
def process_file(self, file_path: str, source_name: str = None) -> dict:
    # Step 1: Ingest file
    document = self.ingestion_agent.ingest(file_path, source_name)
    
    # Step 2: Analyze structure
    analysis = self.understanding_agent.analyze(document)
    
    # Step 3: Select vectorization strategy (LLM-based)
    strategy = self.strategy_agent.select_strategy(analysis)
    
    # Step 4: Chunk and embed
    chunks = self.vectorization_agent.vectorize(document, strategy)
    
    # Step 5: Store in ChromaDB
    self.chroma_manager.add_chunks(chunks)
    
    return {"status": "success", "chunks": len(chunks), ...}
```

**Query Pipeline:**
```python
def query(self, query: str, sources: list[str] = None, k: int = 5) -> QueryResult:
    # Step 1: Retrieve relevant chunks
    retrieved_chunks = self.retrieval_agent.retrieve(query, k, sources)
    
    # Step 2: Build context from chunks
    context = self.context_builder.build(retrieved_chunks)
    
    # Step 3: Generate answer with LLM
    answer = self.llm.generate_with_context(query, context)
    
    return QueryResult(query=query, answer=answer, retrieved_chunks=retrieved_chunks, ...)
```

---

### 2. Ingestion Agent

**File:** `agents/ingestion_agent.py`

**Purpose:** Parse files and create standardized Document objects.

**Parser Registry:**
| Parser | Library | Input | Output |
|--------|---------|-------|--------|
| `CSVParser` | pandas | `.csv` | Text representation + DataFrame |
| `ExcelParser` | pandas + openpyxl | `.xlsx`, `.xls` | Multi-sheet text + DataFrames |
| `PDFParser` | pdfplumber | `.pdf` | Extracted text |
| `DocxParser` | python-docx | `.docx`, `.doc` | Text + heading detection |
| `TxtParser` | built-in | `.txt`, `.md` | Raw text + markdown sections |

**Implementation:**
```python
class IngestionAgent:
    def __init__(self):
        self.parsers = {
            'csv': CSVParser(),
            'excel': ExcelParser(),
            'pdf': PDFParser(),
            'word': DocxParser(),
            'text': TxtParser(),
        }
    
    def ingest(self, file_path: str, source_name: str = None) -> Document:
        file_type = self._detect_type(file_path)
        parser = self.parsers[file_type]
        return parser.parse(file_path, source_name)
```

---

### 3. Understanding Agent

**File:** `agents/understanding_agent.py`

**Purpose:** Analyze document structure to inform vectorization strategy.

**Components:**

1. **DocumentClassifier** (`core/understanding/document_classifier.py`)
   - Classifies documents as `tabular`, `document`, or `structured`
   - Uses heuristics based on content characteristics

2. **SchemaExtractor** (`core/understanding/schema_extractor.py`)
   - Extracts column names, data types, sample values
   - For tabular data (CSV, Excel)

3. **SectionDetector** (`core/understanding/section_detector.py`)
   - Detects headings and sections
   - For text documents (PDF, Word, Text)

**Output:**
```python
class DocumentAnalysis(BaseModel):
    document_type: DocumentType  # tabular, document, structured
    schema_info: Optional[SchemaInfo]  # columns, types, samples
    sections: Optional[list[str]]  # detected section headings
    recommendations: dict  # analysis metadata
```

---

### 4. Vectorization Strategy Agent

**File:** `agents/vectorization_strategy_agent.py`

**Purpose:** Use LLM to select optimal vectorization strategy.

**Available Strategies:**
| Strategy | Use Case | Chunker Used |
|----------|----------|--------------|
| `semantic_chunking` | Text documents (PDF, Word, Text) | `SemanticChunker` |
| `schema_aware_embedding` | Tabular data (CSV, Excel) | `SchemaChunker` |
| `relational_embedding` | Structured/JSON data | `RelationalChunker` |

**LLM Prompt:**
```python
def select_strategy(self, analysis: DocumentAnalysis) -> VectorizationStrategy:
    prompt = f"""
    You are selecting the optimal vectorization strategy for a document.
    
    Document type: {analysis.document_type}
    Schema: {analysis.schema_info if analysis.schema_info else 'N/A'}
    Sections: {analysis.sections if analysis.sections else 'N/A'}
    
    Choose the best strategy:
    1. semantic_chunking - for text documents
    2. schema_aware_embedding - for tabular data
    3. relational_embedding - for structured/JSON data
    
    Return ONLY the strategy name.
    """
    response = self.llm.generate(prompt)
    return self._parse_strategy(response)
```

**Fallback:** Rule-based selection if LLM fails or returns invalid strategy.

---

### 5. Vectorization Agent

**File:** `agents/vectorization_agent.py`

**Purpose:** Chunk documents and generate embeddings.

**Chunkers:**

| Chunker | Strategy | Library | Configuration |
|---------|----------|---------|---------------|
| `SemanticChunker` | `semantic_chunking` | LangChain | chunk_size=1000, overlap=200 |
| `SchemaChunker` | `schema_aware_embedding` | Custom | rows_per_chunk=10 |
| `RelationalChunker` | `relational_embedding` | Custom | preserve_hierarchy=True |

**Implementation:**
```python
class VectorizationAgent:
    def vectorize(self, document: Document, strategy: VectorizationStrategy) -> list[Chunk]:
        # Select chunker based on strategy
        chunker = self._get_chunker(strategy)
        
        # Chunk the document
        chunks = chunker.chunk(document)
        
        # Generate embeddings
        for chunk in chunks:
            chunk.embedding = self.embedding_client.embed(chunk.content)
        
        return chunks
```

**Embedding Model:** `mxbai-embed-large` (1024-dimensional vectors)

---

### 6. Retrieval Agent

**File:** `agents/retrieval_agent.py`

**Purpose:** Handle queries and retrieve relevant context.

**Features:**
- **Global retrieval** — Search entire knowledge base
- **Scoped retrieval** — Filter by specific source documents
- **Configurable top-k** — Number of chunks to retrieve (default: 15)

```python
class RetrievalAgent:
    def retrieve(self, query: str, k: int, sources: list[str] = None) -> list[RetrievedChunk]:
        # Embed query
        query_embedding = self.embedding_client.embed_query(query)
        
        # Search with optional source filter
        if sources:
            results = self.chroma_manager.search_by_sources(query_embedding, sources, k)
        else:
            results = self.chroma_manager.search(query_embedding, k)
        
        return results
```

---

## Core Modules

### LLM Client (`core/llm/ollama_client.py`)

Interfaces with Ollama for reasoning tasks:

```python
class OllamaClient:
    def __init__(self, model: str = None):
        self.model = model or settings.reasoning_model  # llama3:8b
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = ollama.chat(model=self.model, messages=messages)
        return response['message']['content']
    
    def generate_with_context(self, query: str, context: str) -> str:
        # RAG-style generation
        system = "Answer using ONLY the provided context. Cite sources."
        prompt = f"Context:\n{context}\n\nQuestion:\n{query}"
        return self.generate(prompt, system)
```

### Embedding Client (`core/llm/embedding_client.py`)

Generates embeddings using Ollama:

```python
class EmbeddingClient:
    def __init__(self):
        self.model = settings.embedding_model  # mxbai-embed-large
    
    def embed(self, text: str) -> list[float]:
        response = ollama.embeddings(model=self.model, prompt=text)
        return response['embedding']  # 1024-dim vector
    
    def embed_query(self, query: str) -> list[float]:
        return self.embed(query)
```

### Context Builder (`core/reasoning/context_builder.py`)

Formats retrieved chunks for LLM context:

```python
class ContextBuilder:
    def build(self, chunks: list[RetrievedChunk]) -> str:
        context_parts = []
        for i, chunk in enumerate(chunks):
            context_parts.append(f"[Source: {chunk.source}]\n{chunk.content}")
        return "\n\n---\n\n".join(context_parts)
```

---

## Vector Database (ChromaDB)

**File:** `vector_store/chroma_manager.py`

**Features:**
- Persistent storage in `vector_store/chroma_db/`
- Cosine similarity search
- Metadata filtering by source
- Session-based collection naming

**Operations:**
```python
class ChromaManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,  # kb_{session_id}
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_chunks(self, chunks: list[Chunk]) -> None:
        self.collection.add(
            ids=[c.id for c in chunks],
            embeddings=[c.embedding for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[{"source": c.metadata.source, ...} for c in chunks]
        )
    
    def search(self, query_embedding: list[float], k: int = 5) -> list[RetrievedChunk]:
        results = self.collection.query(query_embeddings=[query_embedding], n_results=k)
        return self._parse_results(results)
    
    def search_by_sources(self, query_embedding, sources: list[str], k: int) -> list[RetrievedChunk]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where={"source": {"$in": sources}}
        )
        return self._parse_results(results)
    
    def get_stats(self) -> dict:
        return {
            "total_vectors": self.collection.count(),
            "sources": self._get_unique_sources(),
            "source_count": len(self._get_unique_sources())
        }
    
    def clear(self) -> None:
        self.client.delete_collection(self.collection.name)
```

---

## API Endpoints

**File:** `api/server.py`

FastAPI REST API with the following endpoints:

| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| `/` | GET | API status | - | `{"message": "...", "status": "running"}` |
| `/health` | GET | Health check | - | `{"status": "healthy"}` |
| `/upload` | POST | Process file | `file: UploadFile` | `UploadResponse` |
| `/query` | POST | Query KB | `QueryRequest` | `QueryResponse` |
| `/stats` | GET | KB statistics | - | `StatsResponse` |
| `/clear` | DELETE | Clear KB | - | `{"status": "cleared"}` |

**Request/Response Models:**
```python
class QueryRequest(BaseModel):
    query: str
    sources: Optional[list[str]] = None
    k: Optional[int] = 5

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: list[str]
    chunks: list[dict]
```

**API Documentation:** http://localhost:8000/docs

---

## Streamlit UI

**File:** `ui/streamlit_app.py`

### Pages

**1. Upload Data**
- File upload widget (CSV, Excel, PDF, Word, Text)
- Processing status with step-by-step progress
- Shows document ID and chunk count

**2. Knowledge Base**
- Document count and vector count metrics
- List of indexed sources
- Clear knowledge base button

**3. AI Agent**
- Query input text area
- Retrieval mode toggle (Global / Scoped)
- Source filter multiselect (for Scoped mode)
- Retrieval metrics display:
  - Chunks retrieved, Avg similarity, Top score, Confidence
  - Score distribution chart
  - IR metrics: Recall@K, Precision@K, MRR, nDCG, F1@K, AP@K
- Retrieved chunks with expand/collapse
- AI-generated answer with source citations

### Sidebar

- **Model selector** — Switch between llama3:8b, llama3.2:3b, llama3.2:1b
- **Model info** — Shows RAM requirements and speed
- **Session ID** — Unique identifier for the current session

---

## Configuration

**File:** `config.py`

Uses Pydantic Settings for configuration:

```python
AVAILABLE_MODELS = {
    "llama3:8b": {"name": "Llama 3 (8B)", "description": "Best quality, ~5GB RAM", "speed": "slower"},
    "llama3.2:3b": {"name": "Llama 3.2 (3B)", "description": "Balanced, ~2GB RAM", "speed": "medium"},
    "llama3.2:1b": {"name": "Llama 3.2 (1B)", "description": "Fastest, ~1GB RAM", "speed": "fast"},
}

class Settings(BaseSettings):
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    reasoning_model: str = "llama3:8b"
    embedding_model: str = "mxbai-embed-large"
    
    # ChromaDB
    chroma_persist_directory: str = "./vector_store/chroma_db"
    chroma_collection_name: str = f"kb_{SESSION_ID}"  # Session-unique
    
    # Vectorization
    default_chunk_size: int = 1000
    default_chunk_overlap: int = 200
    
    # Retrieval
    default_top_k: int = 15
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Logging
    log_level: str = "INFO"
```

**Override methods:**
1. Environment variables: `OLLAMA_BASE_URL=http://...`
2. `.env` file
3. Streamlit UI (for reasoning model)

---

## RAG Pipeline

### Prompt Templates

**File:** `core/reasoning/prompts.py`

```python
RAG_SYSTEM_PROMPT = """
You are an AI assistant that answers questions using ONLY the provided context.
Rules:
1. Base your answer ONLY on the context provided
2. If the answer is not in the context, say "Insufficient information in the knowledge base"
3. Cite which source documents you used
4. Be concise and accurate
"""

RAG_QUERY_TEMPLATE = """
Context:
{context}

Question:
{query}
"""
```

### Answer Generation Flow

```
Query → Embed → Vector Search → Top-K Chunks → Build Context → LLM → Answer
```

---

## Running the System

### Service Management Scripts

**`run.sh` — Start All Services**
```bash
./run.sh
```

Features:
- Creates `logs/` directory
- Activates virtual environment
- Checks/installs dependencies
- Verifies Ollama and models
- Starts FastAPI (port 8000) and Streamlit (port 8501)
- Saves PIDs to `logs/*.pid`

**`stop.sh` — Stop All Services**
```bash
./stop.sh
```

### Manual Startup

```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: Streamlit UI
streamlit run ui/streamlit_app.py

# Or: FastAPI only
uvicorn api.server:app --host 0.0.0.0 --port 8000
```

### CLI Commands

```bash
python main.py api        # Start API server
python main.py ui         # Start Streamlit UI
python main.py process /path/to/file.pdf  # Process file
python main.py query "What is...?"        # Query KB
```

---

## Evaluation Module

**Files:** `experiments/evaluation_metrics.py`, `experiments/baseline_pipeline.py`

### Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| **Recall@K** | relevant_in_top_k / total_relevant | % of relevant chunks retrieved |
| **Precision@K** | relevant_in_top_k / K | % of top-K that are relevant |
| **MRR** | 1 / rank_of_first_relevant | How quickly relevant results appear |
| **nDCG** | DCG / IDCG | Ranking quality (position-weighted) |
| **F1@K** | 2 × (P × R) / (P + R) | Harmonic mean of P and R |
| **AP@K** | Σ(P@i × rel_i) / relevant | Average precision at each position |

### Baseline Comparison

**Baseline pipeline:**
- Fixed semantic chunking (512 tokens, 50 overlap)
- No adaptive strategy selection

**Adaptive pipeline:**
- LLM-selected chunking strategy
- Document-type-aware chunking

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | ≥0.1.0 | Orchestration |
| langchain-text-splitters | ≥0.0.1 | Text chunking |
| chromadb | ≥0.4.0 | Vector database |
| ollama | ≥0.1.0 | LLM client |
| fastapi | ≥0.100.0 | REST API |
| uvicorn | ≥0.22.0 | ASGI server |
| streamlit | ≥1.25.0 | Web UI |
| pandas | ≥2.0.0 | Data processing |
| pdfplumber | ≥0.9.0 | PDF parsing |
| python-docx | ≥0.8.11 | Word parsing |
| openpyxl | ≥3.1.0 | Excel parsing |
| pydantic | ≥2.0.0 | Data validation |
| pydantic-settings | ≥2.0.0 | Configuration |
| loguru | ≥0.7.0 | Logging |
| python-multipart | ≥0.0.6 | File uploads |

---

## Extension Points

### Add New File Parser

1. Create parser in `core/ingestion/parsers/`:
```python
from core.ingestion.parser_base import BaseParser

class JsonParser(BaseParser):
    def parse(self, file_path: str, source_name: str = None) -> Document:
        # Implementation
        pass
```

2. Register in `IngestionAgent`:
```python
self.parsers['json'] = JsonParser()
```

3. Add extension mapping in `config.py`:
```python
SUPPORTED_EXTENSIONS['.json'] = 'json'
```

### Add New Chunking Strategy

1. Create chunker in `core/vectorization/chunkers/`:
```python
class CustomChunker:
    def chunk(self, document: Document) -> list[Chunk]:
        # Implementation
        pass
```

2. Add strategy enum in `config.py`:
```python
class VectorizationStrategy:
    CUSTOM = "custom_chunking"
```

3. Register in `VectorizationAgent`

### Add New Retrieval Method

1. Extend `SearchEngine` in `core/retrieval/search.py`
2. Add hybrid search, reranking, or other retrieval enhancements

### Customize Prompts

Edit `core/reasoning/prompts.py` to modify:
- System prompts
- Query templates
- Strategy selection prompts
