# Implementation Guide

This document describes how the Adaptive Knowledge System has been implemented.

---

## Architecture Overview

The system follows an **agent-based architecture** with specialized agents coordinated by an Orchestrator. Each agent handles a specific responsibility in the pipeline.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Orchestrator Agent                         │
│  Coordinates the entire pipeline from ingestion to response     │
└─────────────────────────────────────────────────────────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Ingestion   │   │ Understanding │   │  Retrieval    │
│     Agent     │   │     Agent     │   │    Agent      │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │
        ▼                    ▼
┌───────────────┐   ┌───────────────┐
│ Vectorization │   │ Vectorization │
│Strategy Agent │   │     Agent     │
└───────────────┘   └───────────────┘
```

---

## Directory Structure

```
masters_prototype/
├── agents/                     # Agent implementations
│   ├── orchestrator_agent.py   # Main coordinator
│   ├── ingestion_agent.py      # File parsing
│   ├── understanding_agent.py  # Document analysis
│   ├── vectorization_strategy_agent.py  # LLM strategy selection
│   ├── vectorization_agent.py  # Embedding generation
│   ├── retrieval_agent.py      # Query handling
│   └── evaluation_agent.py     # Experiments
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
│   │   ├── ollama_client.py    # LLM for reasoning
│   │   └── embedding_client.py # Embedding generation
│   ├── retrieval/
│   │   └── search.py           # Similarity search
│   └── reasoning/
│       ├── prompts.py          # RAG templates
│       └── context_builder.py
│
├── vector_store/
│   └── chroma_manager.py       # ChromaDB operations
│
├── api/
│   └── server.py               # FastAPI endpoints
│
├── ui/
│   └── streamlit_app.py        # Streamlit interface
│
├── experiments/
│   ├── baseline_pipeline.py    # Static chunking baseline
│   └── evaluation_metrics.py   # Recall@K, MRR, etc.
│
├── datasets/                   # Sample test data
├── logs/                       # Application logs
├── config.py                   # Configuration
├── main.py                     # CLI entry point
├── requirements.txt            # Dependencies
└── .env.example               # Environment template
```

---

## Data Models

All data structures are defined using **Pydantic** in `core/models/document.py`:

### Document
```python
class Document(BaseModel):
    id: str                      # Unique identifier
    content: str                 # Raw text content
    metadata: DocumentMetadata   # Source, type, etc.
    raw_data: Optional[Any]      # Original data (e.g., DataFrame)
```

### Chunk
```python
class Chunk(BaseModel):
    id: str                      # Unique chunk ID
    content: str                 # Text content
    metadata: ChunkMetadata      # Position, source, section
    embedding: Optional[list[float]]  # Vector embedding
```

### QueryResult
```python
class QueryResult(BaseModel):
    query: str                   # Original query
    answer: str                  # Generated answer
    retrieved_chunks: list[RetrievedChunk]
    sources: list[str]           # Source documents used
```

---

## Agent Implementations

### 1. Ingestion Agent (`agents/ingestion_agent.py`)

**Purpose:** Parse files and create standardized Document objects.

**Implementation:**
- Uses a registry of parsers (CSV, Excel, PDF, Word, Text)
- Each parser extends `BaseParser` abstract class
- Auto-detects file type from extension
- Returns `Document` with content and metadata

```python
class IngestionAgent:
    def __init__(self):
        self.parsers = [CSVParser(), ExcelParser(), PDFParser(), ...]
    
    def ingest(self, file_path: str) -> Document:
        parser = self.get_parser(file_path)
        return parser.parse(file_path)
```

**Parsers:**
| Parser | Library | Output |
|--------|---------|--------|
| CSVParser | pandas | Text + DataFrame |
| ExcelParser | pandas + openpyxl | Text + multi-sheet DataFrames |
| PDFParser | pdfplumber | Extracted text |
| WordParser | python-docx | Text + detected headings |
| TextParser | built-in | Raw text + markdown sections |

---

### 2. Understanding Agent (`agents/understanding_agent.py`)

**Purpose:** Analyze document structure to inform vectorization strategy.

**Components:**
1. **DocumentClassifier** - Classifies as `tabular`, `document`, or `structured`
2. **SchemaExtractor** - Extracts column names, types, samples from tabular data
3. **SectionDetector** - Detects headings/sections in documents

```python
class UnderstandingAgent:
    def analyze(self, document: Document) -> DocumentAnalysis:
        doc_type = self.classifier.classify(document)
        schema = self.schema_extractor.extract(document) if tabular
        sections = self.section_detector.detect(document) if document
        return DocumentAnalysis(...)
```

---

### 3. Vectorization Strategy Agent (`agents/vectorization_strategy_agent.py`)

**Purpose:** Use LLM to select optimal vectorization strategy.

**Strategies:**
| Strategy | Use Case |
|----------|----------|
| `semantic_chunking` | Text documents, PDFs, Word files |
| `schema_aware_embedding` | CSV, Excel (tabular data) |
| `relational_embedding` | JSON, structured data |

**Implementation:**
```python
def select_strategy(self, analysis: DocumentAnalysis) -> VectorizationStrategy:
    prompt = f"""
    Document type: {analysis.document_type}
    Columns: {analysis.schema_info.columns if tabular}
    
    Choose: semantic_chunking, schema_aware_embedding, or relational_embedding
    """
    response = self.llm.generate(prompt)
    return self._parse_strategy(response)
```

Falls back to rule-based selection if LLM fails.

---

### 4. Vectorization Agent (`agents/vectorization_agent.py`)

**Purpose:** Chunk documents and generate embeddings.

**Chunkers:**

1. **SemanticChunker** - Uses LangChain's `RecursiveCharacterTextSplitter`
   - Configurable chunk_size (default: 512)
   - Configurable overlap (default: 50)

2. **SchemaChunker** - For tabular data
   - Groups rows into chunks
   - Preserves column headers in each chunk

3. **RelationalChunker** - For structured data
   - Preserves relationships in JSON
   - Groups related items together

**Embedding Generation:**
```python
def _embed_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
    for chunk in chunks:
        chunk.embedding = self.embedding_client.embed(chunk.content)
    return chunks
```

Uses Ollama's `nomic-embed-text` model via `core/llm/embedding_client.py`.

---

### 5. Retrieval Agent (`agents/retrieval_agent.py`)

**Purpose:** Handle queries and retrieve relevant context.

**Features:**
- **Global retrieval** - Search entire knowledge base
- **Scoped retrieval** - Filter by specific source documents

```python
def retrieve(self, query: str, sources: Optional[list[str]] = None) -> list[RetrievedChunk]:
    query_embedding = self.embedding_client.embed_query(query)
    
    if sources:
        return self.chroma_manager.search_by_sources(query_embedding, sources, k=5)
    return self.chroma_manager.search(query_embedding, k=5)
```

---

### 6. Orchestrator Agent (`agents/orchestrator_agent.py`)

**Purpose:** Coordinate the full pipeline.

**File Processing Pipeline:**
```
process_file(file_path)
    │
    ├── 1. Ingestion Agent → Document
    │
    ├── 2. Understanding Agent → DocumentAnalysis
    │
    ├── 3. Strategy Agent → VectorizationStrategy
    │
    ├── 4. Vectorization Agent → list[Chunk] with embeddings
    │
    └── 5. ChromaDB Manager → Store vectors
```

**Query Pipeline:**
```
query(question, sources)
    │
    ├── 1. Retrieval Agent → list[RetrievedChunk]
    │
    ├── 2. Context Builder → Formatted context string
    │
    └── 3. LLM (Ollama) → Generated answer
```

---

## Vector Database (ChromaDB)

Implemented in `vector_store/chroma_manager.py`.

**Features:**
- Persistent storage in `vector_store/chroma_db/`
- Cosine similarity search
- Metadata filtering by source

**Operations:**
```python
class ChromaManager:
    def add_chunks(chunks: list[Chunk])      # Store embeddings
    def search(query_embedding, k=5)         # Global search
    def search_by_sources(embedding, sources, k)  # Filtered search
    def get_stats()                          # Collection info
    def delete_by_source(source)             # Remove documents
    def clear()                              # Clear all data
```

---

## API Endpoints

Implemented in `api/server.py` using **FastAPI**.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root - API status |
| `/health` | GET | Health check |
| `/upload` | POST | Upload and process file |
| `/query` | POST | Query knowledge base |
| `/stats` | GET | Get KB statistics |
| `/clear` | DELETE | Clear knowledge base |

**Example Query Request:**
```json
{
  "query": "What was the revenue growth?",
  "sources": ["report.pdf"],
  "k": 5
}
```

---

## Streamlit UI

Implemented in `ui/streamlit_app.py`.

**Pages:**

1. **📤 Upload Data**
   - File upload widget
   - Processing status display
   - Step-by-step progress

2. **📚 Knowledge Base**
   - Document count
   - Vector count
   - List of indexed sources
   - Clear button

3. **💬 Ask the AI Agent**
   - Query input
   - Retrieval mode toggle (Global/Scoped)
   - Source filter multiselect
   - Retrieved chunks display
   - AI-generated answer

---

## Configuration

All settings in `config.py` using Pydantic Settings:

```python
class Settings(BaseSettings):
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    reasoning_model: str = "llama3"
    embedding_model: str = "nomic-embed-text"
    
    # ChromaDB
    chroma_persist_directory: str = "./vector_store/chroma_db"
    chroma_collection_name: str = "knowledge_base"
    
    # Vectorization
    default_chunk_size: int = 512
    default_chunk_overlap: int = 50
    
    # Retrieval
    default_top_k: int = 5
```

Override via `.env` file or environment variables.

---

## RAG Prompting

Prompts defined in `core/reasoning/prompts.py`:

```python
RAG_QUERY_TEMPLATE = """
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{query}

If the answer is not in the context, say "Insufficient information in the knowledge base."
Cite your sources.
"""
```

---

## Running the System

### Prerequisites
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3
ollama pull nomic-embed-text

# Start Ollama
ollama serve
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Options

**CLI:**
```bash
# Start Streamlit UI
python main.py ui

# Start FastAPI server
python main.py api

# Process a single file
python main.py process /path/to/file.pdf

# Query the knowledge base
python main.py query "What is the revenue?"
```

**Direct:**
```bash
# Streamlit
streamlit run ui/streamlit_app.py

# FastAPI
uvicorn api.server:app --reload
```

---

## Evaluation Module

For comparing adaptive vs baseline approaches.

**Metrics** (`experiments/evaluation_metrics.py`):
- Recall@K
- Mean Reciprocal Rank (MRR)
- Precision@K

**Baseline** (`experiments/baseline_pipeline.py`):
- Fixed semantic chunking (512 tokens, 50 overlap)
- No adaptive strategy selection

---

## Dependencies

| Package | Purpose |
|---------|---------|
| langchain | Text splitting, orchestration |
| chromadb | Vector database |
| ollama | LLM client |
| fastapi | REST API |
| streamlit | Web UI |
| pandas | Tabular data |
| pdfplumber | PDF parsing |
| python-docx | Word parsing |
| pydantic | Data validation |
| loguru | Logging |

---

## Extension Points

1. **Add new file parser**: Extend `BaseParser` in `core/ingestion/parsers/`
2. **Add new chunking strategy**: Add to `core/vectorization/chunkers/`
3. **Add new retrieval method**: Extend `SearchEngine` in `core/retrieval/`
4. **Customize prompts**: Edit `core/reasoning/prompts.py`
