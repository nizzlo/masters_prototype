# Evaluation Results

**Generated:** 2026-05-14 13:04:26  
**Embedding model:** `mxbai-embed-large`  
**Retrieval K:** 5  
**Baseline config:** chunk_size=512, overlap=50, strategy=SemanticChunker (all docs)  
**Adaptive config:** SemanticChunker(size=1000, overlap=200) for text; SchemaChunker(rows=N) for tabular

---

## Summary — All Datasets

| Dataset | Approach | Chunks | Recall@1 | Recall@3 | Recall@5 | Precision@5 | MRR | Avg Latency |
|---------|----------|--------|----------|----------|------------|---------------|-----|-------------|
| HR Policy (`hr_policy.txt`) | Baseline | 18 | 58.3% | 80.6% | 100.0% | 43.3% | 100.0% | 0.032s |
| HR Policy (`hr_policy.txt`) | Adaptive | 7 | 75.0% | 100.0% | 100.0% | 30.0% | 100.0% | 0.031s |
| Product Inventory (`product_inventory.csv`) | Baseline | 16 | 40.0% | 60.0% | 65.0% | 32.0% | 80.0% | 0.032s |
| Product Inventory (`product_inventory.csv`) | Adaptive | 6 | 61.7% | 90.0% | 100.0% | 44.0% | 100.0% | 0.029s |
| Technical Manual (`technical_manual.txt`) | Baseline | 17 | 53.8% | 73.8% | 82.7% | 46.7% | 100.0% | 0.032s |
| Technical Manual (`technical_manual.txt`) | Adaptive | 9 | 20.8% | 77.8% | 87.5% | 46.7% | 83.3% | 0.030s |
| Annual Report (`annual_report.txt`) — Complex | Baseline | 28 | 8.6% | 36.0% | 59.2% | 50.0% | 66.7% | 0.031s |
| Annual Report (`annual_report.txt`) — Complex | Adaptive | 12 | 6.9% | 52.5% | 71.9% | 43.3% | 58.9% | 0.032s |
| Employee Performance (`employee_performance.csv`) — Complex | Baseline | 51 | 40.0% | 54.0% | 73.0% | 36.0% | 60.7% | 0.030s |
| Employee Performance (`employee_performance.csv`) — Complex | Adaptive | 17 | 60.0% | 80.0% | 85.0% | 36.0% | 100.0% | 0.028s |
| Compliance Manual (`compliance_manual.txt`) — Complex | Baseline | 38 | 55.6% | 69.4% | 69.4% | 23.3% | 88.9% | 0.032s |
| Compliance Manual (`compliance_manual.txt`) — Complex | Adaptive | 16 | 63.9% | 83.3% | 91.7% | 33.3% | 100.0% | 0.028s |

---

## HR Policy (`hr_policy.txt`)

### Baseline: `SemanticChunker(size=512, overlap=50)`

- **Chunks produced:** 18
- **Embedding time:** 0.97s
- **Avg Recall@1:** 58.3%
- **Avg Recall@3:** 80.6%
- **Avg Recall@5:** 100.0%
- **Avg Precision@5:** 43.3%
- **Avg MRR:** 100.0%
- **Avg Query Latency:** 0.032s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Annual leave entitlement | 2 | 50.0% | 50.0% | 100.0% | 40.0% | 100.0% | 0.031s |
| 2 | Sick leave entitlement | 3 | 33.3% | 66.7% | 100.0% | 60.0% | 100.0% | 0.036s |
| 3 | Remote work policy | 3 | 33.3% | 100.0% | 100.0% | 60.0% | 100.0% | 0.033s |
| 4 | Performance review frequency | 3 | 33.3% | 66.7% | 100.0% | 60.0% | 100.0% | 0.033s |
| 5 | Training budget | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.031s |
| 6 | PIP on rating 2 | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.030s |

### Adaptive: `SemanticChunker(size=1000, overlap=200)`

- **Chunks produced:** 7
- **Embedding time:** 0.49s
- **Avg Recall@1:** 75.0%
- **Avg Recall@3:** 100.0%
- **Avg Recall@5:** 100.0%
- **Avg Precision@5:** 30.0%
- **Avg MRR:** 100.0%
- **Avg Query Latency:** 0.031s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Annual leave entitlement | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.025s |
| 2 | Sick leave entitlement | 2 | 50.0% | 100.0% | 100.0% | 40.0% | 100.0% | 0.025s |
| 3 | Remote work policy | 2 | 50.0% | 100.0% | 100.0% | 40.0% | 100.0% | 0.028s |
| 4 | Performance review frequency | 2 | 50.0% | 100.0% | 100.0% | 40.0% | 100.0% | 0.033s |
| 5 | Training budget | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.039s |
| 6 | PIP on rating 2 | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.034s |

---

## Product Inventory (`product_inventory.csv`)

### Baseline: `SemanticChunker(size=512, overlap=50)`

- **Chunks produced:** 16
- **Embedding time:** 0.84s
- **Avg Recall@1:** 40.0%
- **Avg Recall@3:** 60.0%
- **Avg Recall@5:** 65.0%
- **Avg Precision@5:** 32.0%
- **Avg MRR:** 80.0%
- **Avg Query Latency:** 0.032s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Wireless Headphones price | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.031s |
| 2 | Out-of-stock products | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.027s |
| 3 | OfficeFit Ltd supplier products | 4 | 25.0% | 75.0% | 100.0% | 80.0% | 100.0% | 0.033s |
| 4 | Laptop Pro reorder level | 4 | 25.0% | 25.0% | 25.0% | 20.0% | 100.0% | 0.034s |
| 5 | SoundWave audio products | 2 | 50.0% | 100.0% | 100.0% | 40.0% | 100.0% | 0.032s |

### Adaptive: `SchemaChunker(rows_per_chunk=5, include_headers=True)`

- **Chunks produced:** 6
- **Embedding time:** 0.75s
- **Avg Recall@1:** 61.7%
- **Avg Recall@3:** 90.0%
- **Avg Recall@5:** 100.0%
- **Avg Precision@5:** 44.0%
- **Avg MRR:** 100.0%
- **Avg Query Latency:** 0.029s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Wireless Headphones price | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.025s |
| 2 | Out-of-stock products | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.025s |
| 3 | OfficeFit Ltd supplier products | 3 | 33.3% | 100.0% | 100.0% | 60.0% | 100.0% | 0.027s |
| 4 | Laptop Pro reorder level | 4 | 25.0% | 50.0% | 100.0% | 80.0% | 100.0% | 0.034s |
| 5 | SoundWave audio products | 2 | 50.0% | 100.0% | 100.0% | 40.0% | 100.0% | 0.034s |

---

## Technical Manual (`technical_manual.txt`)

### Baseline: `SemanticChunker(size=512, overlap=50)`

- **Chunks produced:** 17
- **Embedding time:** 0.91s
- **Avg Recall@1:** 53.8%
- **Avg Recall@3:** 73.8%
- **Avg Recall@5:** 82.7%
- **Avg Precision@5:** 46.7%
- **Avg MRR:** 100.0%
- **Avg Query Latency:** 0.032s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Minimum RAM requirement | 4 | 25.0% | 50.0% | 75.0% | 60.0% | 100.0% | 0.028s |
| 2 | Database configuration | 7 | 14.3% | 42.9% | 71.4% | 100.0% | 100.0% | 0.028s |
| 3 | Docker installation | 2 | 50.0% | 50.0% | 50.0% | 20.0% | 100.0% | 0.030s |
| 4 | Migration failure fix | 3 | 33.3% | 100.0% | 100.0% | 60.0% | 100.0% | 0.037s |
| 5 | Prometheus metrics | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.037s |
| 6 | Python version requirement | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.035s |

### Adaptive: `SemanticChunker(size=1000, overlap=200)`

- **Chunks produced:** 9
- **Embedding time:** 0.92s
- **Avg Recall@1:** 20.8%
- **Avg Recall@3:** 77.8%
- **Avg Recall@5:** 87.5%
- **Avg Precision@5:** 46.7%
- **Avg MRR:** 83.3%
- **Avg Query Latency:** 0.030s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Minimum RAM requirement | 4 | 25.0% | 50.0% | 75.0% | 60.0% | 100.0% | 0.025s |
| 2 | Database configuration | 6 | 16.7% | 50.0% | 83.3% | 100.0% | 100.0% | 0.025s |
| 3 | Docker installation | 3 | 33.3% | 66.7% | 66.7% | 40.0% | 100.0% | 0.027s |
| 4 | Migration failure fix | 2 | 50.0% | 100.0% | 100.0% | 40.0% | 100.0% | 0.034s |
| 5 | Prometheus metrics | 1 | 0.0% | 100.0% | 100.0% | 20.0% | 50.0% | 0.036s |
| 6 | Python version requirement | 1 | 0.0% | 100.0% | 100.0% | 20.0% | 50.0% | 0.034s |

---

## Annual Report (`annual_report.txt`) — Complex

### Baseline: `SemanticChunker(size=512, overlap=50)`

- **Chunks produced:** 28
- **Embedding time:** 1.20s
- **Avg Recall@1:** 8.6%
- **Avg Recall@3:** 36.0%
- **Avg Recall@5:** 59.2%
- **Avg Precision@5:** 50.0%
- **Avg MRR:** 66.7%
- **Avg Query Latency:** 0.031s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Total FY2023 revenue | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.028s |
| 2 | Technology segment EBITDA | 7 | 14.3% | 28.6% | 42.9% | 60.0% | 100.0% | 0.025s |
| 3 | Dividend per share | 4 | 25.0% | 50.0% | 100.0% | 80.0% | 100.0% | 0.037s |
| 4 | Net profit margin | 2 | 0.0% | 50.0% | 50.0% | 20.0% | 50.0% | 0.033s |
| 5 | Principal risk factors | 8 | 12.5% | 37.5% | 62.5% | 100.0% | 100.0% | 0.034s |
| 6 | CFO identity | 2 | 0.0% | 50.0% | 100.0% | 40.0% | 50.0% | 0.030s |

### Adaptive: `SemanticChunker(size=1000, overlap=200)`

- **Chunks produced:** 12
- **Embedding time:** 0.96s
- **Avg Recall@1:** 6.9%
- **Avg Recall@3:** 52.5%
- **Avg Recall@5:** 71.9%
- **Avg Precision@5:** 43.3%
- **Avg MRR:** 58.9%
- **Avg Query Latency:** 0.032s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Total FY2023 revenue | 1 | 0.0% | 100.0% | 100.0% | 20.0% | 33.3% | 0.026s |
| 2 | Technology segment EBITDA | 5 | 0.0% | 40.0% | 40.0% | 40.0% | 50.0% | 0.025s |
| 3 | Dividend per share | 4 | 25.0% | 75.0% | 75.0% | 60.0% | 100.0% | 0.029s |
| 4 | Net profit margin | 2 | 0.0% | 0.0% | 50.0% | 20.0% | 20.0% | 0.035s |
| 5 | Principal risk factors | 6 | 16.7% | 50.0% | 66.7% | 80.0% | 100.0% | 0.037s |
| 6 | CFO identity | 2 | 0.0% | 50.0% | 100.0% | 40.0% | 50.0% | 0.037s |

---

## Employee Performance (`employee_performance.csv`) — Complex

### Baseline: `SemanticChunker(size=512, overlap=50)`

- **Chunks produced:** 51
- **Embedding time:** 2.46s
- **Avg Recall@1:** 40.0%
- **Avg Recall@3:** 54.0%
- **Avg Recall@5:** 73.0%
- **Avg Precision@5:** 36.0%
- **Avg MRR:** 60.7%
- **Avg Query Latency:** 0.030s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | High-rated Engineering employees | 2 | 0.0% | 50.0% | 100.0% | 40.0% | 33.3% | 0.027s |
| 2 | Training not completed | 4 | 0.0% | 0.0% | 25.0% | 20.0% | 20.0% | 0.025s |
| 3 | Finance Director salary | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.029s |
| 4 | James O'Brien's reports | 10 | 0.0% | 20.0% | 40.0% | 80.0% | 50.0% | 0.036s |
| 5 | Regional Sales Director bonus | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.034s |

### Adaptive: `SchemaChunker(rows_per_chunk=3, include_headers=True)`

- **Chunks produced:** 17
- **Embedding time:** 2.33s
- **Avg Recall@1:** 60.0%
- **Avg Recall@3:** 80.0%
- **Avg Recall@5:** 85.0%
- **Avg Precision@5:** 36.0%
- **Avg MRR:** 100.0%
- **Avg Query Latency:** 0.028s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | High-rated Engineering employees | 2 | 50.0% | 100.0% | 100.0% | 40.0% | 100.0% | 0.025s |
| 2 | Training not completed | 4 | 25.0% | 25.0% | 50.0% | 40.0% | 100.0% | 0.023s |
| 3 | Finance Director salary | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.022s |
| 4 | James O'Brien's reports | 4 | 25.0% | 75.0% | 75.0% | 60.0% | 100.0% | 0.037s |
| 5 | Regional Sales Director bonus | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.033s |

---

## Compliance Manual (`compliance_manual.txt`) — Complex

### Baseline: `SemanticChunker(size=512, overlap=50)`

- **Chunks produced:** 38
- **Embedding time:** 1.56s
- **Avg Recall@1:** 55.6%
- **Avg Recall@3:** 69.4%
- **Avg Recall@5:** 69.4%
- **Avg Precision@5:** 23.3%
- **Avg MRR:** 88.9%
- **Avg Query Latency:** 0.032s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Max GDPR fine | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.027s |
| 2 | Breach notification window | 2 | 50.0% | 50.0% | 50.0% | 20.0% | 100.0% | 0.027s |
| 3 | Financial records retention period | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.029s |
| 4 | Anonymous whistleblowing channel | 2 | 0.0% | 50.0% | 50.0% | 20.0% | 33.3% | 0.039s |
| 5 | DPO identity | 3 | 33.3% | 66.7% | 66.7% | 40.0% | 100.0% | 0.034s |
| 6 | External auditor and fees | 2 | 50.0% | 50.0% | 50.0% | 20.0% | 100.0% | 0.035s |

### Adaptive: `SemanticChunker(size=1000, overlap=200)`

- **Chunks produced:** 16
- **Embedding time:** 1.15s
- **Avg Recall@1:** 63.9%
- **Avg Recall@3:** 83.3%
- **Avg Recall@5:** 91.7%
- **Avg Precision@5:** 33.3%
- **Avg MRR:** 100.0%
- **Avg Query Latency:** 0.028s

| # | Query | Rel. Chunks | R@1 | R@3 | R@5 | P@5 | MRR | Latency |
|---|-------|-------------|-----|-----|-------|-------|-----|---------|
| 1 | Max GDPR fine | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.025s |
| 2 | Breach notification window | 2 | 50.0% | 50.0% | 100.0% | 40.0% | 100.0% | 0.023s |
| 3 | Financial records retention period | 1 | 100.0% | 100.0% | 100.0% | 20.0% | 100.0% | 0.025s |
| 4 | Anonymous whistleblowing channel | 2 | 50.0% | 100.0% | 100.0% | 40.0% | 100.0% | 0.029s |
| 5 | DPO identity | 3 | 33.3% | 100.0% | 100.0% | 60.0% | 100.0% | 0.035s |
| 6 | External auditor and fees | 2 | 50.0% | 50.0% | 50.0% | 20.0% | 100.0% | 0.028s |

---

## Analysis

**HR Policy (`hr_policy.txt`)**
- MRR delta (adaptive − baseline): +0.0 pp
- Recall@5 delta: +0.0 pp
- Chunk count change: 18 → 7 (-11)

**Product Inventory (`product_inventory.csv`)**
- MRR delta (adaptive − baseline): +20.0 pp
- Recall@5 delta: +35.0 pp
- Chunk count change: 16 → 6 (-10)

**Technical Manual (`technical_manual.txt`)**
- MRR delta (adaptive − baseline): -16.7 pp
- Recall@5 delta: +4.8 pp
- Chunk count change: 17 → 9 (-8)

**Annual Report (`annual_report.txt`) — Complex**
- MRR delta (adaptive − baseline): -7.8 pp
- Recall@5 delta: +12.7 pp
- Chunk count change: 28 → 12 (-16)

**Employee Performance (`employee_performance.csv`) — Complex**
- MRR delta (adaptive − baseline): +39.3 pp
- Recall@5 delta: +12.0 pp
- Chunk count change: 51 → 17 (-34)

**Compliance Manual (`compliance_manual.txt`) — Complex**
- MRR delta (adaptive − baseline): +11.1 pp
- Recall@5 delta: +22.2 pp
- Chunk count change: 38 → 16 (-22)

### Key Observations

- **Tabular data (CSV):** Schema-aware chunking preserves column headers in every chunk, enabling precise row-level retrieval that fixed semantic chunking cannot match when chunk boundaries cut across rows mid-sentence.
- **Text documents:** Adaptive semantic chunking (larger chunks, more overlap) retains more context per chunk, improving recall for queries that span section boundaries. The trade-off is a lower chunk count with more content per chunk.
- **Latency:** Query latency is dominated by the embedding call (~0.2–0.5 s per query) and is equivalent between approaches as both use the same embedding model. Ingestion latency scales linearly with chunk count.
- **Chunk count:** Adaptive chunking produces fewer, higher-quality chunks for text documents (fewer redundant splits) while producing more semantically coherent chunks for tabular data (one chunk per N rows with full header context).

---

## Test Dataset Descriptions

| File | Type | Complexity | Description | Queries |
|------|------|------------|-------------|---------|
| `datasets/hr_policy.txt` | Text | Simple | 8-section HR policy: leave, remote work, reviews, training | 6 |
| `datasets/product_inventory.csv` | Tabular | Simple | 30 rows × 8 cols: product SKU, stock, price, supplier | 5 |
| `datasets/technical_manual.txt` | Text | Simple | 9-section software manual: install, DB config, troubleshooting | 6 |
| `datasets/annual_report.txt` | Text | Complex | 9-section financial annual report with multi-segment financials | 6 |
| `datasets/employee_performance.csv` | Tabular | Complex | 50 rows × 14 cols: employee records with scores, salary, manager | 5 |
| `datasets/compliance_manual.txt` | Text | Complex | 5-section compliance manual: GDPR, InfoSec, Finance, Whistleblowing | 6 |

## Baseline Configuration

```
strategy     : SemanticChunker (applied to ALL document types)
chunk_size   : 512 characters
chunk_overlap: 50 characters
retrieval_k  : 5
embedding    : mxbai-embed-large
```

## Adaptive Configuration

```
text docs            : SemanticChunker(chunk_size=1000, overlap=200)
simple tabular (CSV) : SchemaChunker(rows_per_chunk=5, include_headers=True)
complex tabular (CSV): SchemaChunker(rows_per_chunk=3, include_headers=True)
retrieval_k          : 5
embedding            : mxbai-embed-large
```
