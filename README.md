# Adaptive Knowledge System

> Research Prototype: Automated Vectorization and Knowledge Base Enablement for AI Agents

## Overview

This system automatically converts **heterogeneous enterprise data** into a **vectorized knowledge base** that AI agents can query using **Retrieval-Augmented Generation (RAG)**. It runs fully locally using **Ollama** for LLM inference.

### Research Objective

> Design and evaluate an automated system that converts heterogeneous data sources into a unified vector knowledge base that AI agents can reason over.

### Key Features

- **Multi-format ingestion** — CSV, Excel, PDF, Word, Text/Markdown
- **Adaptive vectorization** — LLM-selected chunking strategies based on document structure
- **Local LLM inference** — Ollama with multiple model options (llama3:8b, llama3.2:3b, llama3.2:1b)
- **RAG-based Q&A** — Context-grounded answers with source citations
- **Retrieval metrics** — Real-time Recall@K, Precision@K, MRR, nDCG, F1
- **Scoped queries** — Filter by specific source documents
- **Modern UI** — Streamlit interface with Material icons

---

## Quick Start

### 1. Prerequisites

**Install Ollama:**
```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from https://ollama.com
```

**Pull required models:**
```bash
# Reasoning model (choose based on RAM)
ollama pull llama3:8b        # Best quality (~5GB)
ollama pull llama3.2:3b      # Balanced (~2GB)
ollama pull llama3.2:1b      # Fastest (~1GB)

# Embedding model (required)
ollama pull mxbai-embed-large
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 3. Start Services

**Recommended: Use the startup script**
```bash
./run.sh
```

This starts Ollama, FastAPI (port 8000), and Streamlit (port 8501) automatically.

**Or start manually:**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Streamlit UI
streamlit run ui/streamlit_app.py
```

### 4. Access the UI

Open **http://localhost:8501** in your browser.

### 5. Stop Services

```bash
./stop.sh
```

---

## System Architecture

```text
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

### Pipeline Flow

```
User Upload → Ingestion → Structure Analysis → Strategy Selection → Chunking → Embedding → Storage → Query → RAG Answer
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| LLM Runtime | Ollama |
| Embedding Model | mxbai-embed-large |
| Reasoning Models | llama3:8b, llama3.2:3b, llama3.2:1b |
| Vector Database | ChromaDB |
| UI Framework | Streamlit |
| API Framework | FastAPI |
| Orchestration | LangChain |
| Data Parsing | pandas, pdfplumber, python-docx, openpyxl |
| Validation | Pydantic |

---

## Usage

### Streamlit UI (Recommended)

**Upload Data** — Upload files (CSV, Excel, PDF, Word, Text) to build the knowledge base.

**Knowledge Base** — View indexed documents, vector counts, and clear data.

**AI Agent** — Query the knowledge base with natural language:
- **Global mode**: Search all documents
- **Scoped mode**: Filter by specific sources

### CLI

```bash
# Process a file
python main.py process /path/to/document.pdf

# Query the knowledge base
python main.py query "What were the key findings?"

# Start API server only
python main.py api

# Start UI only
python main.py ui
```

### REST API

```bash
# Upload a file
curl -X POST http://localhost:8000/upload -F "file=@document.pdf"

# Query the knowledge base
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the revenue?", "k": 5}'

# Get statistics
curl http://localhost:8000/stats
```

API documentation: **http://localhost:8000/docs**

---

## Configuration

Settings are managed via `config.py` and can be overridden with environment variables or a `.env` file:

| Setting | Default | Description |
|---------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `REASONING_MODEL` | `llama3:8b` | Model for reasoning (switchable in UI) |
| `EMBEDDING_MODEL` | `mxbai-embed-large` | Model for embeddings |
| `DEFAULT_CHUNK_SIZE` | `1000` | Characters per chunk |
| `DEFAULT_CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `DEFAULT_TOP_K` | `15` | Number of chunks to retrieve |

---

## Project Structure

```
masters_prototype/
├── agents/                     # Agent implementations
│   ├── orchestrator_agent.py   # Main pipeline coordinator
│   ├── ingestion_agent.py      # File parsing
│   ├── understanding_agent.py  # Document structure analysis
│   ├── vectorization_strategy_agent.py  # LLM strategy selection
│   ├── vectorization_agent.py  # Chunking & embedding
│   ├── retrieval_agent.py      # Vector search
│   └── evaluation_agent.py     # Metrics & experiments
│
├── core/                       # Core modules
│   ├── models/document.py      # Pydantic data models
│   ├── ingestion/parsers/      # Format-specific parsers
│   ├── understanding/          # Classifiers & extractors
│   ├── vectorization/chunkers/ # Chunking strategies
│   ├── llm/                    # Ollama clients
│   ├── retrieval/              # Search engine
│   └── reasoning/              # RAG prompts
│
├── vector_store/               # ChromaDB persistence
├── api/server.py               # FastAPI endpoints
├── ui/streamlit_app.py         # Streamlit interface
├── experiments/                # Evaluation scripts
├── datasets/                   # Sample data
├── logs/                       # Application logs
├── config.py                   # Configuration
├── main.py                     # CLI entry point
├── run.sh                      # Start all services
├── stop.sh                     # Stop all services
└── requirements.txt            # Dependencies
```

---

## Evaluation Metrics

The UI displays real-time retrieval metrics for each query:

| Metric | Description |
|--------|-------------|
| **Recall@K** | % of relevant chunks retrieved |
| **Precision@K** | % of retrieved chunks that are relevant |
| **MRR** | Mean Reciprocal Rank — how fast relevant results appear |
| **nDCG** | Normalized Discounted Cumulative Gain |
| **F1@K** | Harmonic mean of Precision and Recall |
| **AP@K** | Average Precision considering rank order |

---

## Supported File Types

| Format | Extension | Parser |
|--------|-----------|--------|
| CSV | `.csv` | pandas |
| Excel | `.xlsx`, `.xls` | pandas + openpyxl |
| PDF | `.pdf` | pdfplumber |
| Word | `.docx`, `.doc` | python-docx |
| Text | `.txt`, `.md` | built-in |

---

## Vectorization Strategies

The system automatically selects the optimal chunking strategy based on document structure:

| Strategy | Use Case |
|----------|----------|
| **Semantic Chunking** | Text documents (PDF, Word, Text) |
| **Schema-Aware Embedding** | Tabular data (CSV, Excel) |
| **Relational Embedding** | Structured/JSON data |

---

## Running the Evaluation Test Suite

The evaluation suite benchmarks **Baseline (fixed chunking)** against **Adaptive (strategy-selected chunking)** across three sample datasets.

### Test Datasets

| File | Type | Content |
|------|------|---------|
| `datasets/hr_policy.txt` | Text | 8-section HR policy manual |
| `datasets/product_inventory.csv` | Tabular | 30-row product inventory (8 columns) |
| `datasets/technical_manual.txt` | Text | 9-section software technical manual |

### Prerequisites

Ollama must be running with the embedding model pulled:

```bash
ollama serve                    # if not already running
ollama pull mxbai-embed-large   # if not already pulled
```

### Run the Evaluation

```bash
# Activate the virtual environment
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Run all experiments
python experiments/run_evaluation.py
```

The script will:
1. Load each dataset and chunk it with both approaches
2. Embed all chunks using `mxbai-embed-large` into isolated ChromaDB collections
3. Run 17 ground-truth queries across the three datasets
4. Compute Recall@1/3/5, Precision@5, MRR, and per-query latency
5. Print a summary table to the console
6. Write the full report to **`EVALUATION_RESULTS.md`**

### Configuration

The evaluation parameters are set at the top of `experiments/run_evaluation.py`:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `BASELINE_CHUNK_SIZE` | `512` | Fixed chunk size (chars) for baseline |
| `BASELINE_CHUNK_OVERLAP` | `50` | Overlap (chars) for baseline |
| `RETRIEVAL_K` | `5` | Top-K results retrieved per query |
| `EMBEDDING_MODEL` | `mxbai-embed-large` | Ollama embedding model |

### Add or Edit Queries

Ground-truth queries are defined in `experiments/test_queries.py`. Each `TestQuery` specifies:

```python
TestQuery(
    query="How many annual leave days are employees entitled to?",
    relevant_phrases=["20 days of annual leave", "annual leave"],  # substring match
    dataset="hr_policy",
    description="Annual leave entitlement",
)
```

A retrieved chunk is marked relevant if its content contains **any** of the `relevant_phrases` (case-insensitive). Add new queries to `HR_QUERIES`, `INVENTORY_QUERIES`, or `TECH_QUERIES` — they are automatically picked up by the runner.

---

## Development

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for technical implementation details.

**Extension points:**
1. Add new parser: Extend `BaseParser` in `core/ingestion/parsers/`
2. Add chunking strategy: Add to `core/vectorization/chunkers/`
3. Add retrieval method: Extend `SearchEngine` in `core/retrieval/`

---

## License

Research prototype — Academic use.
