# Automated Vectorization and Knowledge Base Enablement for AI Agents

## Prototype Implementation Plan (Full System)

## 1. Overview

This project implements a **prototype system that automatically converts heterogeneous enterprise data into a vectorized knowledge base that can be queried by an AI agent**.

The system demonstrates the full **automated knowledge lifecycle pipeline**:

1. Data ingestion from heterogeneous file formats
2. Automatic structure and metadata analysis
3. Adaptive vectorization strategy selection using an LLM
4. Embedding generation and vector database storage
5. Retrieval-Augmented Generation (RAG) for answering queries
6. A UI for uploading data and interacting with the AI agent

The prototype is designed to support the research objective:

> Design and evaluate an automated system that converts heterogeneous data sources into a unified vector knowledge base that AI agents can reason over.

The system runs **fully locally using Ollama** for LLM inference.

---

# 2. System Architecture

The architecture consists of five main layers.

1. Data Ingestion Layer
2. Data Understanding Layer
3. Adaptive Vectorization Layer
4. Vector Knowledge Base
5. Retrieval-Augmented AI Agent

Pipeline:

```text
User Upload
     ↓
Data Ingestion
     ↓
Structure Understanding
     ↓
Vectorization Strategy Selection (LLM)
     ↓
Embedding Generation
     ↓
Vector Database Storage
     ↓
Retrieval System
     ↓
AI Agent Reasoning
     ↓
Answer + Sources
```

---

# 3. Technology Stack

| Component            | Technology                      |
| -------------------- | ------------------------------- |
| Programming Language | Python                          |
| LLM Runtime          | Ollama                          |
| Embedding Model      | nomic-embed-text                |
| Reasoning Model      | llama3:8b                       |
| Vector Database      | ChromaDB                        |
| UI                   | Streamlit                       |
| Backend API          | FastAPI                         |
| Orchestration        | LangChain                       |
| Parsing Libraries    | pandas, pdfplumber, python-docx |

---

# 4. Installing Ollama

The system uses **Ollama to run local LLM models**.

Install Ollama.

Mac / Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Windows:

Download installer from:

https://ollama.com

Start Ollama:

```bash
ollama serve
```

---

# 5. Required Models

Pull required models.

Reasoning model:

```bash
ollama pull llama3:8b
```

Alternative:

```bash
ollama pull mistral
```

Embedding model:

```bash
ollama pull nomic-embed-text
```

---

# 6. Project Structure

```text
adaptive-knowledge-system/

agents/
  orchestrator_agent.py
  ingestion_agent.py
  understanding_agent.py
  vectorization_strategy_agent.py
  vectorization_agent.py
  retrieval_agent.py
  evaluation_agent.py

core/
  ingestion/
  parsing/
  vectorization/
  retrieval/

vector_store/
  chroma_db/

api/
  server.py

ui/
  streamlit_app.py

datasets/
experiments/

main.py
```

---

# 7. Agent-Based System Design

The system is implemented using **specialized agents coordinated by an Orchestrator Agent**.

## Orchestrator Agent

Coordinates the entire workflow.

Pipeline:

```text
Upload file
   ↓
Ingestion Agent
   ↓
Understanding Agent
   ↓
Vectorization Strategy Agent
   ↓
Vectorization Agent
   ↓
Vector Store
   ↓
Retrieval Agent
   ↓
AI Agent
   ↓
Answer
```

---

# 8. Data Ingestion Agent

Handles file parsing and extraction.

Supported formats:

* CSV
* Excel
* PDF
* Word
* Text

Libraries used:

* pandas
* pdfplumber
* python-docx

Responsibilities:

1. Detect file type
2. Parse file
3. Extract text or structured data
4. Create standardized document object

Example:

```python
{
  "content": "...",
  "metadata": {
      "source": "report.pdf",
      "type": "document"
  }
}
```

---

# 9. Data Understanding Agent

Analyzes structure and metadata.

Responsibilities:

* detect document type
* extract metadata
* detect schema for tabular data
* detect document sections

Example:

Tabular:

```python
{
 type: "tabular",
 columns: ["Date", "Revenue", "Region"]
}
```

Document:

```python
{
 type: "document",
 sections: ["Introduction", "Results", "Conclusion"]
}
```

---

# 10. Vectorization Strategy Agent

Uses an LLM to determine the optimal embedding strategy.

Example prompt:

```
You are selecting a vectorization strategy.

Document type: tabular
Columns: Date, Revenue, Region

Choose the best strategy:

1. semantic chunking
2. schema aware embedding
3. relational embedding

Return only the strategy name.
```

Possible strategies:

| Data Type          | Strategy               |
| ------------------ | ---------------------- |
| Document           | Semantic chunking      |
| Tabular            | Schema-aware embedding |
| Structured dataset | Relational embedding   |

---

# 11. Vectorization Agent

Converts documents into embeddings.

Pipeline:

```text
Document
   ↓
Chunking
   ↓
Embedding Generation
   ↓
Metadata Attachment
   ↓
Vector Storage
```

Embeddings generated using:

```
nomic-embed-text
```

Example:

```python
POST http://localhost:11434/api/embeddings
```

---

# 12. Vector Knowledge Base

Embeddings are stored in **ChromaDB**.

Each vector entry contains:

```python
{
 vector: [...],
 metadata: {
   source: "report.pdf",
   section: "summary"
 }
}
```

Metadata enables:

* source filtering
* document filtering
* section filtering

---

# 13. Retrieval System

The retrieval agent handles user queries.

Pipeline:

```text
User Query
   ↓
Query Embedding
   ↓
Vector Search
   ↓
Top-K Retrieved Chunks
```

Optional improvements:

* metadata filtering
* hybrid search
* reranking

---

# 14. Retrieval Modes

The UI supports two retrieval modes.

## Global Retrieval

Search entire knowledge base.

```python
vector_store.similarity_search(query, k=5)
```

## Scoped Retrieval

Search only selected sources.

Example:

```python
vector_store.similarity_search(
 query,
 k=5,
 filter={"source": {"$in": selected_sources}}
)
```

This allows users to restrict queries to specific documents.

---

# 15. Retrieved Chunk Visualization

Before generating the final answer, the system displays retrieved chunks.

Pipeline:

```text
User Query
   ↓
Vector Search
   ↓
Retrieved Chunks
   ↓
Display in UI
   ↓
AI Agent Reasoning
   ↓
Final Answer
```

Example display:

```
Retrieved Context

Chunk 1
Source: report.pdf
Revenue increased by 18% in Q2.

Chunk 2
Source: finance.xlsx
Revenue increased from $4.2M to $4.96M.
```

---

# 16. AI Agent (Reasoning Layer)

The AI agent generates answers using retrieved context.

Prompt template:

```
Answer the question using ONLY the provided context.

Context:
{retrieved_chunks}

Question:
{query}

If the answer is not in the context say "insufficient information".
```

Outputs:

* generated answer
* source references

---

# 17. Web UI (Streamlit)

The prototype includes a Streamlit UI.

Three main pages.

## Upload Data

Users upload enterprise data.

Supported formats:

* CSV
* Excel
* PDF
* Word

Processing display:

```
✓ File detected
✓ Structure analyzed
✓ Vectorization strategy selected
✓ Embeddings generated
```

---

## Knowledge Base Viewer

Displays vector database information.

Example:

```
Documents indexed: 12
Vector entries: 245

Sources:
report.pdf
finance.xlsx
policy.docx
```

---

## Ask the AI Agent

Users ask questions.

UI features:

* query input
* retrieval mode selection
* source filtering
* retrieved chunk visualization
* AI response display

Example query:

```
"What were the key findings in the financial report?"
```

---

# 18. Backend API

FastAPI provides endpoints.

Upload endpoint:

```
POST /upload
```

Query endpoint:

```
POST /query
```

Statistics endpoint:

```
GET /stats
```

---

# 19. Evaluation Module

The prototype compares two pipelines.

Baseline:

```
Static vectorization
```

Proposed:

```
Adaptive vectorization
```

Evaluation metrics:

* Recall@k
* Mean Reciprocal Rank (MRR)
* grounding accuracy
* response relevance

---

# 20. Development Timeline

Week 1
Project setup and architecture.

Week 2
Implement ingestion and parsing modules.

Week 3
Implement data understanding layer.

Week 4
Implement vectorization strategy agent.

Week 5
Implement vector database integration.

Week 6
Implement retrieval system.

Week 7
Implement AI reasoning agent.

Week 8
Implement Streamlit UI and evaluation experiments.

---

# 21. Final Prototype Pipeline

```text
Heterogeneous Data
      ↓
Automated Ingestion
      ↓
Structure Understanding
      ↓
Adaptive Vectorization
      ↓
Vector Knowledge Base
      ↓
Retrieval-Augmented AI Agent
      ↓
Grounded Response
```

This prototype demonstrates a **fully automated knowledge system capable of transforming heterogeneous data into a knowledge base that AI agents can reason over**.
