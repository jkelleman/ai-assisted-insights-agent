# Jupyter Notebook Integration

Use the AI-Assisted Insights Agent interactively in Jupyter notebooks for data exploration and analysis.

## Setup

1. Install Jupyter:
```bash
pip install jupyter
```

2. Install the agent:
```bash
pip install -e /path/to/ai-assisted-insights-agent
```

3. Launch Jupyter:
```bash
jupyter notebook
```

## Quick Start

Create a new notebook and run:

```python
# Import the agent tools
from insights_agent.server import (
    ask_question,
    generate_query,
    validate_query,
    explain_result,
    compare_metrics,
    check_data_quality,
    METRIC_DEFINITIONS
)

# Ask a question
ask_question("How many active users did we have last week?")
```

## Example Notebook Workflow

### 1. Explore Available Metrics

```python
# List all available metrics
for metric_id, metric in METRIC_DEFINITIONS.items():
    print(f"{metric['name']}: {metric['description']}")
```

### 2. Ask Questions

```python
# Simple question
result = ask_question("What was our revenue last month?")
print(result)
```

### 3. Generate and Validate Queries

```python
# Generate a query
query = generate_query("active_users", "last 30 days", "", "date")
print(query)

# Extract SQL and validate
sql = """
SELECT date, COUNT(DISTINCT user_id)
FROM analytics.user_events
WHERE event_type = 'login'
  AND event_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY date
"""

validation = validate_query(sql)
print(validation)
```

### 4. Analyze Results

```python
# Get a result and explain it
result_value = "1500"
explanation = explain_result(result_value, "active_users", "last 7 days")
print(explanation)
```

### 5. Compare Metrics

```python
# Compare two related metrics
comparison = compare_metrics("active_users", "signups", "last 30 days")
print(comparison)
```

### 6. Check Data Quality

```python
# Before making decisions, check data quality
quality = check_data_quality("revenue", "last 7 days")
print(quality)
```

### 7. Build Analysis Pipeline

```python
def analyze_metric(metric_id, time_period):
    """Complete analysis pipeline for a metric."""
    
    # 1. Get the data
    result = ask_question(f"What was {metric_id} for {time_period}?")
    print("=" * 70)
    print("QUERY RESULT")
    print("=" * 70)
    print(result)
    
    # 2. Check data quality
    quality = check_data_quality(metric_id, time_period)
    print("\n" + "=" * 70)
    print("DATA QUALITY")
    print("=" * 70)
    print(quality)
    
    # 3. Generate reusable query
    query = generate_query(metric_id, time_period, "", "date")
    print("\n" + "=" * 70)
    print("REUSABLE QUERY")
    print("=" * 70)
    print(query)

# Run the pipeline
analyze_metric("active_users", "last 30 days")
```

### 8. Visualize Results (with pandas and matplotlib)

```python
import pandas as pd
import matplotlib.pyplot as plt

# In a real scenario, you'd execute the query and get actual data
# For demonstration, we'll show the pattern:

# 1. Generate query
query = generate_query("active_users", "last 30 days", "", "date")
print(query)

# 2. Execute query (simulated)
# data = pd.read_sql(sql, connection)
# For demo:
dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
values = [1200 + i * 10 for i in range(30)]
data = pd.DataFrame({"date": dates, "active_users": values})

# 3. Visualize
plt.figure(figsize=(12, 6))
plt.plot(data["date"], data["active_users"])
plt.title("Active Users - Last 30 Days")
plt.xlabel("Date")
plt.ylabel("Active Users")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## Tips for Jupyter

- Use `display()` for prettier output
- Save frequently used queries as notebook variables
- Create reusable analysis functions
- Document your findings with markdown cells
- Export queries for use in production
