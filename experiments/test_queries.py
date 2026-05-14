"""
Ground-truth query definitions for evaluation.

Each query has:
  - query: the natural language question
  - relevant_phrases: substrings that must appear in a relevant chunk
    (at least one phrase must match; matching is case-insensitive)
  - dataset: which test file this query targets
  - description: human-readable label
"""

from dataclasses import dataclass, field


@dataclass
class TestQuery:
    query: str
    relevant_phrases: list[str]
    dataset: str
    description: str


# ---------------------------------------------------------------------------
# HR Policy queries  (datasets/hr_policy.txt)
# ---------------------------------------------------------------------------
HR_QUERIES: list[TestQuery] = [
    TestQuery(
        query="How many annual leave days are employees entitled to?",
        relevant_phrases=["20 days of annual leave", "annual leave", "20 days"],
        dataset="hr_policy",
        description="Annual leave entitlement",
    ),
    TestQuery(
        query="How many sick days do employees get per year?",
        relevant_phrases=["10 sick days", "sick leave", "sick days per calendar year"],
        dataset="hr_policy",
        description="Sick leave entitlement",
    ),
    TestQuery(
        query="Can employees work from home and how many days per week?",
        relevant_phrases=["3 days per week", "remote work", "hybrid working", "work remotely"],
        dataset="hr_policy",
        description="Remote work policy",
    ),
    TestQuery(
        query="How often are performance reviews conducted?",
        relevant_phrases=["bi-annually", "performance review", "mid-year reviews in June"],
        dataset="hr_policy",
        description="Performance review frequency",
    ),
    TestQuery(
        query="What is the annual training budget per employee?",
        relevant_phrases=["1,500", "$1,500", "training budget"],
        dataset="hr_policy",
        description="Training budget",
    ),
    TestQuery(
        query="What happens if an employee receives a rating of 2?",
        relevant_phrases=["performance improvement plan", "PIP", "60-day"],
        dataset="hr_policy",
        description="PIP on rating 2",
    ),
]

# ---------------------------------------------------------------------------
# Product Inventory queries  (datasets/product_inventory.csv)
# ---------------------------------------------------------------------------
INVENTORY_QUERIES: list[TestQuery] = [
    TestQuery(
        query="What is the unit price of the Wireless Headphones?",
        relevant_phrases=["Wireless Headphones", "149.99"],
        dataset="product_inventory",
        description="Wireless Headphones price",
    ),
    TestQuery(
        query="Which products have a stock quantity of zero or are out of stock?",
        relevant_phrases=["Network Switch", "Stock_Quantity: 0", "SKU-029"],
        dataset="product_inventory",
        description="Out-of-stock products",
    ),
    TestQuery(
        query="What products are supplied by OfficeFit Ltd?",
        relevant_phrases=["OfficeFit Ltd", "Office Chair", "Standing Desk"],
        dataset="product_inventory",
        description="OfficeFit Ltd supplier products",
    ),
    TestQuery(
        query="What is the reorder level for the Laptop Pro 15?",
        relevant_phrases=["Laptop Pro", "Reorder_Level: 10", "SKU-001"],
        dataset="product_inventory",
        description="Laptop Pro reorder level",
    ),
    TestQuery(
        query="Which audio products does SoundWave Ltd supply?",
        relevant_phrases=["SoundWave Ltd", "Wireless Headphones", "Bluetooth Speaker"],
        dataset="product_inventory",
        description="SoundWave audio products",
    ),
]

# ---------------------------------------------------------------------------
# Technical Manual queries  (datasets/technical_manual.txt)
# ---------------------------------------------------------------------------
TECH_QUERIES: list[TestQuery] = [
    TestQuery(
        query="What are the minimum RAM requirements to install DataFlow?",
        relevant_phrases=["8 GB", "RAM", "system requirements", "minimum"],
        dataset="technical_manual",
        description="Minimum RAM requirement",
    ),
    TestQuery(
        query="How do I configure the database connection?",
        relevant_phrases=["DATABASE_URL", "postgresql://", "database configuration"],
        dataset="technical_manual",
        description="Database configuration",
    ),
    TestQuery(
        query="How do I install DataFlow using Docker?",
        relevant_phrases=["docker run", "docker pull", "dataflow/platform"],
        dataset="technical_manual",
        description="Docker installation",
    ),
    TestQuery(
        query="How do I fix a migration failure error?",
        relevant_phrases=["db migrate --repair", "MigrationError", "migration"],
        dataset="technical_manual",
        description="Migration failure fix",
    ),
    TestQuery(
        query="What Prometheus metrics does DataFlow expose?",
        relevant_phrases=["dataflow_pipeline_runs_total", "Prometheus", "/metrics"],
        dataset="technical_manual",
        description="Prometheus metrics",
    ),
    TestQuery(
        query="What Python version is required for DataFlow?",
        relevant_phrases=["Python: 3.10", "3.11", "python version"],
        dataset="technical_manual",
        description="Python version requirement",
    ),
]

# ---------------------------------------------------------------------------
# All queries combined
# ---------------------------------------------------------------------------
ALL_QUERIES: list[TestQuery] = HR_QUERIES + INVENTORY_QUERIES + TECH_QUERIES
