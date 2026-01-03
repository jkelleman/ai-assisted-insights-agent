# Python Client Integration

Direct integration of the AI-Assisted Insights Agent in Python applications.

## Installation

```bash
pip install -e /path/to/ai-assisted-insights-agent
```

## Usage

```python
from insights_agent.server import (
    ask_question,
    generate_query,
    validate_query,
    explain_result,
    compare_metrics,
    check_data_quality
)

# Ask a question
result = ask_question("How many active users last week?")
print(result)

# Generate a SQL query
query = generate_query("revenue", "last 30 days", "country = 'US'")
print(query)

# Validate a query
validation = validate_query("SELECT COUNT(*) FROM users WHERE date >= '2025-01-01'")
print(validation)

# Explain a result
explanation = explain_result("1500", "active_users", "last 7 days")
print(explanation)

# Compare metrics
comparison = compare_metrics("active_users", "revenue", "last month")
print(comparison)

# Check data quality
quality = check_data_quality("conversion_rate", "last 7 days")
print(quality)
```

## Running the Example

```bash
python example.py
```

## Use Cases

### 1. Automated Reporting
```python
def generate_weekly_report():
    metrics = ["active_users", "revenue", "conversion_rate", "signups"]
    report = []
    
    for metric in metrics:
        result = ask_question(f"What was {metric} last week?")
        report.append(result)
    
    return "\n\n".join(report)
```

### 2. Data Quality Monitoring
```python
def monitor_data_quality():
    critical_metrics = ["revenue", "active_users"]
    alerts = []
    
    for metric in critical_metrics:
        quality = check_data_quality(metric, "today")
        if "⚠" in quality or "✗" in quality:
            alerts.append((metric, quality))
    
    return alerts
```

### 3. Query Generation for BI Tools
```python
def generate_dashboard_queries():
    queries = {}
    
    # Generate queries for each dashboard metric
    queries["daily_users"] = generate_query(
        "active_users", "last 30 days", "", "date"
    )
    queries["daily_revenue"] = generate_query(
        "revenue", "last 30 days", "", "date"
    )
    
    return queries
```

### 4. Metric Comparison Pipeline
```python
def analyze_metrics_correlation(metric1, metric2, period):
    # Compare metrics
    comparison = compare_metrics(metric1, metric2, period)
    
    # Check data quality for both
    quality1 = check_data_quality(metric1, period)
    quality2 = check_data_quality(metric2, period)
    
    return {
        "comparison": comparison,
        "quality": {
            metric1: quality1,
            metric2: quality2
        }
    }
```
