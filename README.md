# Automated Vectorization and Knowledge Base Enablement for AI Agents

## Prototype Implementation Plan

## 1. Overview

This project implements a **prototype system that automatically converts heterogeneous enterprise data into a vectorized knowledge base that can be queried by an AI agent**.

The system demonstrates the full **knowledge lifecycle automation pipeline** proposed in the research:

1. Data ingestion from multiple file formats
2. Automatic structure and metadata analysis
3. Adaptive vectorization strategy selection using an LLM
4. Vector embedding generation and storage
5. Retrieval-augmented AI reasoning over the knowledge base
6. A user interface for uploading data and querying the system

The prototype is designed to support the research objective:

> Design and evaluate an automated system that converts heterogeneous data sources into a unified vector knowledge base that AI agents can reason over.

The system will run **fully locally using Ollama** for the language model.

---

# 2. System Architecture

The system consists of five main layers:

1. Data Ingestion Layer
2. Data Understanding Layer
3. Adaptive Vectorization Layer
4. Vector Knowledge Base
5. Retrieval-Augmented AI Agent

The architecture pipeline:

```
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
| Reasoning Model      | llama3 / mistral                |
| Vector Database      | ChromaDB                        |
| UI                   | Streamlit                       |
| API Backend          | FastAPI                         |
| Orchestration        | LangChain                       |
| File Parsing         | pandas, pdfplumber, python-docx |

---

# 4. Installing Ollama

The system uses **Ollama to run language models locally**.

Install Ollama:

Mac / Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Windows:

Download installer from:

https://ollama.com

Start Ollama service:

```bash
ollama serve
```

---

# 5. Download Required Models

Pull the models required for the prototype.

Main reasoning model:

```bash
ollama pull llama3
```

Alternative faster model:

```bash
ollama pull mistral
```

Embedding model:

```bash
ollama pull nomic-embed-text
```

---

# 6. Project Folder Structure

```
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

The prototype uses an **agent-based architecture** where each system component is implemented as a specialized agent.

## Orchestrator Agent

The orchestrator coordinates the full pipeline.

Pipeline executed by orchestrator:

```
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

The ingestion agent handles parsing and extraction of raw data from uploaded files.

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
2. Parse file content
3. Extract raw text or structured data
4. Pass data to the understanding layer

Example output document object:

```
{
  content: "...",
  metadata: {
      source: "report.pdf",
      type: "document"
  }
}
```

---

# 9. Data Understanding Agent

This agent analyzes the structure of the extracted data.

Responsibilities:

* detect data type
* extract metadata
* identify schema for tabular data
* detect document sections

Example output:

For tabular data:

```
{
 type: "tabular",
 columns: ["Date", "Revenue", "Region"],
 rows: 500
}
```

For documents:

```
{
 type: "document",
 sections: ["Introduction", "Results", "Conclusion"]
}
```

---

# 10. Vectorization Strategy Agent

This agent selects the **best vectorization strategy using an LLM**.

Input:

* data type
* metadata
* structure

Example prompt to LLM:

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

| Data Type           | Strategy               |
| ------------------- | ---------------------- |
| Document            | Semantic chunking      |
| Tabular             | Schema-aware embedding |
| Structured datasets | Relational embedding   |

---

# 11. Vectorization Agent

The vectorization agent converts documents into embeddings.

Pipeline:

```
Document
   ↓
Chunking
   ↓
Embedding generation
   ↓
Metadata attachment
   ↓
Vector database storage
```

Embeddings generated using:

```
Ollama embedding model: nomic-embed-text
```

Example embedding call:

```python
requests.post(
 "http://localhost:11434/api/embeddings",
 json={
   "model": "nomic-embed-text",
   "prompt": text
 }
)
```

---

# 12. Vector Database

All embeddings are stored in a centralized vector store.

Vector database:

```
ChromaDB
```

Each vector entry stores:

```
vector
metadata
source document
structure information
```

Example entry:

```
{
 vector: [...],
 metadata: {
   source: "report.pdf",
   section: "summary"
 }
}
```

---

# 13. Retrieval Agent

Handles knowledge retrieval when a user asks a question.

Pipeline:

```
User Query
   ↓
Query Embedding
   ↓
Vector Search
   ↓
Top-K Relevant Documents
```

Optional improvements:

* metadata filtering
* hybrid search
* reranking

---

# 14. AI Agent (Reasoning Layer)

The AI agent answers questions using retrieved context.

Prompt template:

```
Answer the question using ONLY the provided context.

Context:
{retrieved_documents}

Question:
{user_query}

If the answer is not in the context say "insufficient information".
```

The system returns:

* generated answer
* source references

---

# 15. Web UI (Streamlit)

A Streamlit interface will be built for demonstration.

The UI contains three pages.

---

## Upload Data Page

Allows users to upload enterprise files.

Supported formats:

* CSV
* Excel
* PDF
* Word

Processing steps displayed:

```
✓ Format detected
✓ Structure analyzed
✓ Vectorization strategy selected
✓ Embeddings generated
```

---

## Knowledge Base Viewer

Displays vector database statistics.

Example:

```
Documents indexed: 12
Vector entries: 245

Sources:
- report.pdf
- finance.xlsx
- policy.docx
```

---

## Ask the AI Agent

Allows users to query the knowledge base.

Example query:

```
"What were the key findings in the financial report?"
```

Example response:

```
Answer:
Revenue increased by 18% in Q2.

Sources:
report.pdf (section 3)
finance.xlsx (sheet revenue)
```

---

# 16. Backend API

The backend uses FastAPI.

### Upload Endpoint

```
POST /upload
```

Triggers ingestion and vectorization pipeline.

---

### Query Endpoint

```
POST /query
```

Triggers retrieval and AI reasoning.

---

### Statistics Endpoint

```
GET /stats
```

Returns knowledge base statistics.

---

# 17. Evaluation Module

The system will compare two pipelines:

```
Baseline: Static vectorization
Proposed: Adaptive vectorization
```

Evaluation metrics:

* Recall@k
* Mean Reciprocal Rank (MRR)
* Grounding accuracy
* Response relevance

---

# 18. Development Timeline

Week 1
Project setup and architecture.

Week 2
Implement ingestion and parsing modules.

Week 3
Implement data understanding layer.

Week 4
Implement adaptive vectorization strategy.

Week 5
Implement vector database integration.

Week 6
Implement retrieval pipeline.

Week 7
Implement AI agent reasoning.

Week 8
Implement Streamlit UI and evaluation experiments.

---

# 19. Final Prototype Pipeline

```
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

The prototype demonstrates an **end-to-end automated knowledge system capable of transforming heterogeneous data into a knowledge base that AI agents can reason over.**
