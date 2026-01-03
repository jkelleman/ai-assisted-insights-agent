# API Documentation

Complete API reference for the AI-Assisted Insights Agent.

## Table of Contents

1. [Tools](#tools)
2. [Prompts](#prompts)
3. [Configuration](#configuration)
4. [Query History](#query-history)
5. [Helper Functions](#helper-functions)

---

## Tools

MCP tools exposed by the agent for natural language data querying.

### ask_question

Ask a data question in natural language and get an explainable answer.

**Signature:**
```python
ask_question(question: str, time_period: str = "last 7 days") -> str
```

**Parameters:**
- `question` (str): Natural language question (e.g., "How many users signed up last month?")
- `time_period` (str, optional): Time range for the query. Defaults to "last 7 days"

**Returns:**
- str: Answer with explanation, SQL query, and data quality context

**Example:**
```python
result = ask_question("How many active users did we have last week?")
```

**Response Format:**
```
Question: How many active users did we have last week?
Time Period: last 7 days

Answer: 12,470 users

Query Used:
SELECT COUNT(DISTINCT user_id)
FROM analytics.user_events
WHERE event_type = 'login'
  AND event_date >= CURRENT_DATE - INTERVAL '7 days'

Explanation:
This query counts unique users who logged in at least once...

Data Quality:
✓ Data is fresh (updated 2 hours ago)
...
```

---

### generate_query

Generate a SQL query for a specific metric with structured parameters.

**Signature:**
```python
generate_query(
    metric: str,
    time_period: str = "last 7 days",
    filters: str = "",
    group_by: str = ""
) -> str
```

**Parameters:**
- `metric` (str): Metric name (e.g., "active_users", "revenue", "conversion_rate")
- `time_period` (str, optional): Time range. Defaults to "last 7 days"
- `filters` (str, optional): Additional WHERE clause filters
- `group_by` (str, optional): GROUP BY clause

**Returns:**
- str: SQL query with explanation

**Example:**
```python
query = generate_query("revenue", "last 30 days", "country = 'US'", "date")
```

---

### validate_query

Validate a SQL query for syntax, performance, and data quality issues.

**Signature:**
```python
validate_query(sql_query: str) -> str
```

**Parameters:**
- `sql_query` (str): SQL query to validate

**Returns:**
- str: Validation report with issues and recommendations

**Example:**
```python
validation = validate_query("SELECT COUNT(*) FROM users WHERE date >= '2025-01-01'")
```

**Validation Checks:**
- Basic syntax validation
- Performance warnings (SELECT *, missing WHERE clause)
- Best practices (date filters, GROUP BY usage)

---

### explain_result

Explain a query result with context, comparisons, and interpretation.

**Signature:**
```python
explain_result(
    result_value: str,
    metric: str,
    time_period: str = "last 7 days"
) -> str
```

**Parameters:**
- `result_value` (str): The numeric result to explain
- `metric` (str): Which metric this result represents
- `time_period` (str, optional): Time period for the result

**Returns:**
- str: Contextual explanation with comparisons and insights

**Example:**
```python
explanation = explain_result("1500", "active_users", "last 7 days")
```

---

### suggest_followups

Suggest relevant follow-up questions based on the current query.

**Signature:**
```python
suggest_followups(question: str, result: str = "") -> str
```

**Parameters:**
- `question` (str): Original question asked
- `result` (str, optional): Optional result value to inform suggestions

**Returns:**
- str: List of suggested follow-up questions

**Example:**
```python
suggestions = suggest_followups("How many active users last week?")
```

---

### save_query_template

Save a query as a reusable template for reproducibility.

**Signature:**
```python
save_query_template(name: str, sql_query: str, description: str = "") -> str
```

**Parameters:**
- `name` (str): Template name (e.g., "Weekly Active Users Report")
- `sql_query` (str): SQL query to save
- `description` (str, optional): Optional description

**Returns:**
- str: Confirmation with template details

**Example:**
```python
result = save_query_template(
    "Weekly Users Report",
    "SELECT COUNT(*) FROM users WHERE date >= CURRENT_DATE - 7",
    "Weekly active users count"
)
```

---

### list_templates

List all saved query templates.

**Signature:**
```python
list_templates() -> str
```

**Returns:**
- str: List of saved templates with metadata

**Example:**
```python
templates = list_templates()
```

---

### check_data_quality

Assess data quality for a specific metric and time period.

**Signature:**
```python
check_data_quality(metric: str, time_period: str = "last 7 days") -> str
```

**Parameters:**
- `metric` (str): Metric to check
- `time_period` (str, optional): Time period to assess

**Returns:**
- str: Data quality report with freshness, completeness, and anomalies

**Example:**
```python
quality = check_data_quality("revenue", "last 7 days")
```

**Quality Checks:**
- Freshness: When data was last updated
- Completeness: Coverage of date range
- Anomaly Detection: Unusual patterns or values
- Overall Quality Score: 0-100

---

### compare_metrics

Compare two metrics side-by-side for the same time period.

**Signature:**
```python
compare_metrics(metric1: str, metric2: str, time_period: str = "last 7 days") -> str
```

**Parameters:**
- `metric1` (str): First metric to compare
- `metric2` (str): Second metric to compare
- `time_period` (str, optional): Time period for comparison

**Returns:**
- str: Side-by-side comparison with insights

**Example:**
```python
comparison = compare_metrics("active_users", "revenue", "last 30 days")
```

---

## Prompts

### insights_query_guide

Guide for asking effective data questions.

**Signature:**
```python
insights_query_guide() -> str
```

**Returns:**
- str: Best practices and examples for natural language queries

**Usage in Claude:**
```
Please show me the insights query guide.
```

**Contents:**
- Best practices for asking questions
- Example questions (simple, comparative, investigative)
- Available metrics
- Tips for getting better answers

---

## Configuration

### Config Class

Manage agent configuration from YAML or JSON files.

**Usage:**
```python
from insights_agent.config import Config

# Load configuration
config = Config("config.yaml")

# Get metrics
metrics = config.get_metrics()

# Get data sources
sources = config.get_data_sources()

# Add custom metric
config.add_metric("custom_metric", {
    "name": "Custom Metric",
    "description": "My custom metric",
    "sql_template": "COUNT(*)",
    "table": "my_table",
    "filter": "",
    "unit": "count"
})

# Save configuration
config.save()
```

**Configuration File Structure:**
```yaml
server:
  name: ai-insights-agent
  version: 0.1.0

storage:
  type: sqlite
  path: insights_agent.db

metrics:
  metric_id:
    name: Metric Name
    description: What it measures
    sql_template: SQL aggregation
    table: schema.table_name
    filter: Optional WHERE clause
    unit: Unit of measurement

data_sources:
  source_id:
    type: postgresql
    host: localhost
    port: 5432
    database: analytics

business_glossary:
  business_term: technical_term
```

---

## Query History

### QueryHistory Class

Persistent storage for query history using SQLite.

**Usage:**
```python
from insights_agent.history import QueryHistory

# Initialize
history = QueryHistory("insights_agent.db")

# Add query
query_id = history.add_query(
    question="How many active users?",
    time_period="last 7 days",
    sql_query="SELECT COUNT(*) FROM users",
    result_value=1500,
    metric_id="active_users"
)

# Get history
recent = history.get_history(limit=10)

# Search history
results = history.search_history("revenue")

# Get statistics
stats = history.get_statistics()

# Export history
history.export_history("queries.json", format="json")
history.export_history("queries.csv", format="csv")

# Clear old history
deleted = history.clear_history(older_than_days=30)
```

**Template Management:**
```python
# Save template
history.save_template(
    template_id="weekly_users",
    name="Weekly Active Users",
    sql_query="SELECT COUNT(*) FROM users WHERE date >= CURRENT_DATE - 7",
    description="Weekly user count",
    tags=["weekly", "users"]
)

# Get template
template = history.get_template("weekly_users")

# List templates
templates = history.list_templates()

# Delete template
deleted = history.delete_template("weekly_users")
```

---

## Helper Functions

Internal helper functions used by the tools.

### _parse_question

Parse natural language question to identify metrics and intent.

**Signature:**
```python
_parse_question(question: str) -> Dict[str, Any]
```

**Returns:**
```python
{
    "metrics": ["active_users"],
    "time_period": "last 7 days",
    "original_question": "How many active users?"
}
```

---

### _generate_sql_query

Generate SQL query from parsed question.

**Signature:**
```python
_generate_sql_query(parsed: Dict[str, Any], time_period: str) -> Dict[str, Any]
```

**Returns:**
```python
{
    "sql": "SELECT COUNT(DISTINCT user_id) FROM ...",
    "error": None
}
```

---

### _parse_time_period

Convert time period string to SQL date filter.

**Signature:**
```python
_parse_time_period(time_period: str) -> str
```

**Examples:**
- "last 7 days" → "event_date >= CURRENT_DATE - INTERVAL '7 days'"
- "this month" → "event_date >= DATE_TRUNC('month', CURRENT_DATE)"
- "last month" → Complex date range for previous month

---

### _simulate_query_execution

Simulate query execution with realistic values (for demo purposes).

**Signature:**
```python
_simulate_query_execution(sql: str) -> float
```

---

## Data Structures

### METRIC_DEFINITIONS

Dictionary of available metrics.

**Structure:**
```python
{
    "metric_id": {
        "name": "Display Name",
        "description": "What it measures",
        "sql_template": "SQL aggregation",
        "table": "schema.table_name",
        "filter": "Optional WHERE filter",
        "unit": "units"
    }
}
```

### BUSINESS_GLOSSARY

Mappings of business terms to technical terms.

**Structure:**
```python
{
    "customers": "users",
    "purchases": "transactions",
    "sales": "revenue"
}
```

### QUERY_HISTORY

In-memory list of recent queries (persisted via QueryHistory class).

**Structure:**
```python
[
    {
        "question": "Natural language question",
        "time_period": "last 7 days",
        "sql": "Generated SQL",
        "result": 1500.0,
        "timestamp": "2026-01-03T10:30:00"
    }
]
```

### QUERY_TEMPLATES

Dictionary of saved query templates.

**Structure:**
```python
{
    "template_id": {
        "name": "Template Name",
        "sql": "SQL query",
        "description": "Description",
        "created_at": "2026-01-03T10:00:00",
        "run_count": 5
    }
}
```
