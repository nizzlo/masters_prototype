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
# Annual Report queries  (datasets/annual_report.txt)
# ---------------------------------------------------------------------------
ANNUAL_REPORT_QUERIES: list[TestQuery] = [
    TestQuery(
        query="What was the total revenue for FY2023?",
        relevant_phrases=["$8.74 billion", "8.74 billion", "total revenue for fy2023", "record revenues"],
        dataset="annual_report",
        description="Total FY2023 revenue",
    ),
    TestQuery(
        query="What was the Technology segment EBITDA?",
        relevant_phrases=["$893 million", "893 million", "Technology Segment EBITDA", "technology segment"],
        dataset="annual_report",
        description="Technology segment EBITDA",
    ),
    TestQuery(
        query="What dividend per share was paid to shareholders?",
        relevant_phrases=["$0.48 per share", "0.48 per share", "dividend of $0.48", "dividend"],
        dataset="annual_report",
        description="Dividend per share",
    ),
    TestQuery(
        query="What was the net profit margin?",
        relevant_phrases=["18.3%", "net profit margin", "net margin"],
        dataset="annual_report",
        description="Net profit margin",
    ),
    TestQuery(
        query="What are the principal risk factors identified by the Board?",
        relevant_phrases=["cybersecurity", "macroeconomic", "supply chain", "talent retention", "risk factor"],
        dataset="annual_report",
        description="Principal risk factors",
    ),
    TestQuery(
        query="Who is the Chief Financial Officer?",
        relevant_phrases=["Rebecca Sung", "Chief Financial Officer", "CFO"],
        dataset="annual_report",
        description="CFO identity",
    ),
]

# ---------------------------------------------------------------------------
# Employee Performance queries  (datasets/employee_performance.csv)
# ---------------------------------------------------------------------------
EMPLOYEE_PERF_QUERIES: list[TestQuery] = [
    TestQuery(
        query="Which Engineering employees have an annual rating above 4.5?",
        relevant_phrases=["Fatima Al-Hassan", "Sophie Chen", "4.80", "4.60"],
        dataset="employee_performance",
        description="High-rated Engineering employees",
    ),
    TestQuery(
        query="Which employees have not completed their required training?",
        relevant_phrases=["Training_Completed: No"],
        dataset="employee_performance",
        description="Training not completed",
    ),
    TestQuery(
        query="What is the base salary of the Finance Director?",
        relevant_phrases=["Finance Director", "148000", "Claudia Venter"],
        dataset="employee_performance",
        description="Finance Director salary",
    ),
    TestQuery(
        query="Which employees report to James O'Brien?",
        relevant_phrases=["James O'Brien"],
        dataset="employee_performance",
        description="James O'Brien's reports",
    ),
    TestQuery(
        query="What is the bonus percentage for the Regional Sales Director?",
        relevant_phrases=["Regional Sales Director", "Bonus_Pct: 28", "Samuel Adeyemi"],
        dataset="employee_performance",
        description="Regional Sales Director bonus",
    ),
]

# ---------------------------------------------------------------------------
# Compliance Manual queries  (datasets/compliance_manual.txt)
# ---------------------------------------------------------------------------
COMPLIANCE_QUERIES: list[TestQuery] = [
    TestQuery(
        query="What is the maximum GDPR fine for serious infringements?",
        relevant_phrases=["€20 million", "4% of the total worldwide annual turnover", "gdpr fine", "Tier 2"],
        dataset="compliance_manual",
        description="Max GDPR fine",
    ),
    TestQuery(
        query="Within how many hours must a personal data breach be reported to the supervisory authority?",
        relevant_phrases=["72 hours", "72-hour", "within 72"],
        dataset="compliance_manual",
        description="Breach notification window",
    ),
    TestQuery(
        query="How long must financial records be retained?",
        relevant_phrases=["minimum of 7 years", "7 years", "retained for a minimum"],
        dataset="compliance_manual",
        description="Financial records retention period",
    ),
    TestQuery(
        query="How do employees report whistleblowing concerns anonymously?",
        relevant_phrases=["EthicsLine", "0800-ETHICS", "ethics.meridiangroup.com"],
        dataset="compliance_manual",
        description="Anonymous whistleblowing channel",
    ),
    TestQuery(
        query="Who is the Data Protection Officer?",
        relevant_phrases=["Helen Forsythe", "Data Protection Officer", "DPO"],
        dataset="compliance_manual",
        description="DPO identity",
    ),
    TestQuery(
        query="Who is the external auditor and what are their fees?",
        relevant_phrases=["Deloitte LLP", "external auditor", "$6.2 million"],
        dataset="compliance_manual",
        description="External auditor and fees",
    ),
]

# ---------------------------------------------------------------------------
# All queries combined
# ---------------------------------------------------------------------------
ALL_QUERIES: list[TestQuery] = (
    HR_QUERIES + INVENTORY_QUERIES + TECH_QUERIES
    + ANNUAL_REPORT_QUERIES + EMPLOYEE_PERF_QUERIES + COMPLIANCE_QUERIES
)
