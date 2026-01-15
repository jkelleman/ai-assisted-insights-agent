# AI-Assisted Insights Agent

**An MCP agent that translates natural language questions into accurate, explainable, and reproducible data insights.**

[![CI](https://github.com/jkelleman/ai-assisted-insights-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/jkelleman/ai-assisted-insights-agent/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 📖 Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Architecture](#architecture)
- [About](#about)

## Overview

The AI-Assisted Insights Agent bridges the gap between business questions and data answers. Analysts and product teams spend hours translating stakeholder questions into SQL queries, validating results, and explaining findings. This agent automates that workflow while maintaining transparency and reproducibility.

## The Problem

**Time-Intensive Translation**
- Stakeholders ask: "Why did revenue drop last week?"
- Analysts spend hours writing queries, joining tables, debugging logic
- Results require extensive validation and explanation
- Process must be repeated for similar questions

**Accuracy and Trust Barriers**
- Non-technical stakeholders can't verify query logic
- Results lack context about data quality and limitations
- Difficult to reproduce analysis with updated data
- No audit trail for how insights were derived

**Communication Friction**
- Business language ("active customers") doesn't map cleanly to technical definitions
- Analysts become bottlenecks for routine questions
- Insights arrive too late to inform decisions
- Tribal knowledge locked in analyst teams

## The Solution

This agent provides natural language query translation with built-in explainability and reproducibility:

**Natural Language Interface**
- Ask questions in plain English: "What's our conversion rate for trial users last month?"
- Agent translates to SQL using trusted metric definitions
- Automatic query optimization and validation

**Explainability First**
- Show the SQL query generated
- Explain which tables and metrics were used
- Surface data quality indicators (freshness, completeness)
- Highlight assumptions and limitations

**Reproducibility by Default**
- Every insight includes the underlying query
- Query templates can be saved and rerun
- Version-controlled metric definitions ensure consistency
- Audit trail for compliance and validation

## Key Features

### 🤖 Natural Language Query Processing
Convert business questions to validated SQL queries:
```
"How many active users did we have last week?"
↓
SELECT COUNT(DISTINCT user_id) 
FROM analytics.user_events 
WHERE event_type = 'login' 
  AND event_date >= CURRENT_DATE - INTERVAL '7 days'
```

### 📊 Explainable Results
Every answer includes:
- **The Query** - Exact SQL that generated the result
- **Metric Definitions** - Which trusted metrics were used
- **Data Quality** - Freshness, completeness, known issues
- **Assumptions** - Time ranges, filters, exclusions applied

### 🧠 Intelligent Context
- Understands business terminology from metric definitions
- Suggests relevant follow-up questions
- Detects ambiguous queries and asks for clarification
- Learns from query history and patterns

### 🔗 Integration with Semantic Layer
Works seamlessly with semantic metrics:
- Pulls metric definitions from semantic layer
- Ensures consistent business logic across queries
- Validates queries against approved metrics
- Maintains governance and trust standards

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Option 1: Install from Source

```bash
# Clone the repository
git clone https://github.com/jkelleman/ai-assisted-insights-agent.git
cd ai-assisted-insights-agent

# Install with pip
pip install -e .

# Or install with uv (recommended)
uv pip install -e .
```

### Option 2: Install as Package

```bash
pip install git+https://github.com/jkelleman/ai-assisted-insights-agent.git
```

### Verify Installation

```bash
# Test the CLI
python -m insights_agent.cli

# Or run tests
pytest 05_tests/
```

## Quick Start

### 1. Configure the Agent

Create or edit `config.yaml`:

```yaml
metrics:
  active_users:
    name: Active Users
    description: Unique users who logged in
    sql_template: COUNT(DISTINCT user_id)
    table: analytics.user_events
    filter: event_type = 'login'
    unit: users

business_glossary:
  customers: users
  purchases: transactions
```

### 2. Start the MCP Server

```bash
python -m insights_agent.server
```

### 3. Use with Claude Desktop

#### Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python",
      "args": ["-m", "insights_agent.server"],
      "cwd": "C:\\path\\to\\ai-assisted-insights-agent"
    }
  }
}
```

#### macOS/Linux
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python3",
      "args": ["-m", "insights_agent.server"],
      "cwd": "/path/to/ai-assisted-insights-agent"
    }
  }
}
```

Restart Claude Desktop and start asking data questions!

### 4. Use the Interactive CLI

```bash
python -m insights_agent.cli

# In the CLI:
insights> ask How many active users did we have last week?
insights> generate revenue "last 30 days"
insights> compare active_users revenue "last month"
```

## Usage

### MCP Tools

The agent exposes 9 tools via MCP:

#### ask_question
Ask questions in natural language:
```python
ask_question("How many users signed up last month?")
```

#### generate_query
Generate SQL for specific metrics:
```python
generate_query("revenue", "last 30 days", "country='US'", "date")
```

#### validate_query
Validate SQL queries:
```python
validate_query("SELECT COUNT(*) FROM users WHERE date >= '2025-01-01'")
```

#### explain_result
Get context and interpretation:
```python
explain_result("1500", "active_users", "last 7 days")
```

#### suggest_followups
Get follow-up question suggestions:
```python
suggest_followups("How many active users last week?")
```

#### save_query_template
Save reusable query templates:
```python
save_query_template("Weekly Users", "SELECT COUNT(*) FROM users", "Weekly count")
```

#### list_templates
View saved templates:
```python
list_templates()
```

#### check_data_quality
Assess data quality:
```python
check_data_quality("revenue", "last 7 days")
```

#### compare_metrics
Compare two metrics:
```python
compare_metrics("active_users", "revenue", "last month")
```

### MCP Resources

Access data via resources:

- `metrics://catalog` - Complete metrics catalog
- `metrics://metric/{id}` - Specific metric definition
- `history://recent` - Recent query history
- `templates://list` - Saved query templates

### Python API

Use directly in Python code:

```python
from insights_agent.server import ask_question, generate_query

# Ask a question
result = ask_question("How many active users last week?")
print(result)

# Generate a query
query = generate_query("revenue", "last 30 days", "country='US'")
print(query)
```

See [02_examples/python-client](02_examples/python-client) for more examples.

## Configuration

### Metric Definitions

Define custom metrics in `config.yaml`:

```yaml
metrics:
  your_metric:
    name: Your Metric Name
    description: What this metric measures
    sql_template: COUNT(*) or SUM(column) or other aggregation
    table: schema.table_name
    filter: Optional WHERE clause conditions
    unit: users, dollars, percent, etc.
```

### Data Sources

Configure data sources:

```yaml
data_sources:
  production:
    type: postgresql
    host: db.example.com
    port: 5432
    database: analytics
    # Use environment variables for credentials
```

### Business Glossary

Map business terms:

```yaml
business_glossary:
  customers: users
  purchases: transactions
  sales: revenue
```

### Query Settings

Tune performance:

```yaml
query:
  max_results: 10000
  timeout_seconds: 30
  enable_caching: true
  cache_ttl_seconds: 300
```

## Examples

### Claude Desktop Integration
See [02_examples/claude-desktop](02_examples/claude-desktop)

### Python Client
See [02_examples/python-client](02_examples/python-client)

### Jupyter Notebook
See [02_examples/jupyter](02_examples/jupyter)

### Complete Usage Guide
See [02_examples/USAGE.md](02_examples/USAGE.md)

## Architecture

```
┌─────────────────────────────────────────┐
│  Natural Language Interface             │
├─────────────────────────────────────────┤
│  • parse_question()                     │
│  • generate_query()                     │
│  • explain_result()                     │
│  • suggest_followups()                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Query Translation Layer                │
├─────────────────────────────────────────┤
│  • Maps business terms to SQL           │
│  • Validates against metric definitions │
│  • Optimizes query performance          │
│  • Checks data quality constraints      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Semantic Metrics Repository            │
├─────────────────────────────────────────┤
│  • Trusted metric definitions           │
│  • Business glossary mappings           │
│  • Data quality metadata                │
│  • Historical query patterns            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Data Warehouse                         │
├─────────────────────────────────────────┤
│  • Snowflake, BigQuery, Redshift        │
│  • dbt models and metrics               │
│  • Raw and transformed tables           │
└─────────────────────────────────────────┘
```

## Alternative Installation (using uv)

```bash
# Clone the repository
git clone https://github.com/jkelleman/ai-assisted-insights-agent.git
cd ai-assisted-insights-agent

# Install dependencies with uv
uv add "mcp[cli]"
uv pip install -e .

# Configure database connection
export DATABASE_URL="your_warehouse_connection_string"

# Run the agent
uv run python -m insights_agent.server
```

### Usage Examples

**Ask a simple question:**
```python
ask_question("How many users signed up last month?")

# Returns:
# Answer: 1,247 users
# 
# Query Used:
# SELECT COUNT(DISTINCT user_id)
# FROM analytics.signups
# WHERE signup_date >= '2025-12-01' 
#   AND signup_date < '2026-01-01'
#
# Data Quality:
# ✓ Data is fresh (updated 2 hours ago)
# ✓ No missing days in date range
# ✓ Matches expected volume (within 2σ)
```

**Get explanation with context:**
```python
explain_query("Why did revenue drop 15% last week?")

# Returns:
# Investigating revenue drop...
#
# Revenue Breakdown:
# - Previous week: $245,000
# - Last week: $208,250 (-15%)
#
# Contributing Factors:
# 1. New user signups down 22% (from 450 to 351)
# 2. Average order value stable ($55 vs $54)
# 3. Conversion rate unchanged (2.3%)
#
# Recommended Analysis:
# • Check marketing campaign performance
# • Review signup funnel for blockers
# • Compare to same week last year (seasonal?)
```

**Save reproducible query:**
```python
save_query_template(
    question="Weekly active users",
    template="SELECT COUNT(DISTINCT user_id) FROM analytics.user_events WHERE event_date >= CURRENT_DATE - INTERVAL '7 days'"
)

# Query template saved. Rerun anytime with:
# run_template("Weekly active users")
```

## Design Principles

### 1. Explainability Over Black Boxes
Never return a number without showing how it was calculated. Transparency builds trust and enables validation.

### 2. Reproducibility as a Feature
Every insight should be reproducible with the same query. Version-controlled metric definitions ensure consistency over time.

### 3. Progressive Complexity
Start with simple answers. Offer drill-down paths for users who want more detail. Don't overwhelm non-technical stakeholders.

### 4. Human-in-the-Loop Validation
Agent assists but doesn't replace analysts. Complex queries should be reviewed before execution.

### 5. Governance Integration
Respect organizational metric definitions and data access policies. Don't bypass governance for convenience.

## Use Cases

### Product Manager
"I need to understand why feature adoption is lower than expected."

**Agent helps:**
- Parse "feature adoption" to the canonical metric definition
- Generate queries for adoption rate by cohort, segment, and time period
- Surface data quality issues (incomplete tracking, recent schema changes)
- Suggest follow-up questions about user behavior patterns

### Executive Stakeholder
"What's our customer lifetime value this quarter?"

**Agent helps:**
- Retrieve CLV metric from semantic layer
- Show calculation methodology and assumptions
- Compare to previous quarters with confidence intervals
- Provide reproducible query for quarterly reporting

### Data Analyst
"I need to validate whether our conversion funnel is working correctly."

**Agent helps:**
- Generate funnel queries with proper event sequencing
- Check for data integrity issues (duplicate events, missing steps)
- Compare to historical baseline for anomaly detection
- Export validated query for dashboard integration

## Technical Stack

- **Python 3.10+** - Core language
- **FastMCP** - Model Context Protocol implementation
- **SQLAlchemy** - Database abstraction and query building
- **SQLGlot** - SQL parsing and optimization
- **Pydantic** - Schema validation and type safety
- **Rich** - Terminal output formatting

## MCP Tools

### Core Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `ask_question()` | Translate natural language to SQL | "Active users last week?" |
| `generate_query()` | Create SQL from structured input | Build query with parameters |
| `explain_result()` | Add context to query results | Why this number? What assumptions? |
| `validate_query()` | Check query before execution | Catch errors, optimize performance |
| `suggest_followups()` | Recommend next questions | Drill-down paths based on result |
| `save_query_template()` | Store reusable query | Create report templates |
| `check_data_quality()` | Assess result reliability | Freshness, completeness, anomalies |
| `compare_metrics()` | Side-by-side analysis | Period over period, segment comparison |

## What This Demonstrates

### UX Skills
- **Abstraction Design** - Hiding SQL complexity while maintaining transparency
- **Progressive Disclosure** - Layered information architecture for varied technical depth
- **Trust Through Transparency** - Explainability as core design principle
- **Contextual Assistance** - Anticipating follow-up needs and surfacing relevant information

### Technical Skills
- **NLP Integration** - Natural language to structured query translation
- **SQL Generation** - Dynamic query building with optimization and validation
- **Data Quality Engineering** - Automated freshness and completeness checks
- **System Integration** - Connecting semantic layers, warehouses, and governance systems

### Domain Expertise
- **Analytics Workflows** - Understanding analyst pain points and bottlenecks
- **Business Intelligence** - Translating business questions to technical implementations
- **Data Governance** - Respecting organizational policies and metric standards
- **Decision Support** - Designing for actionability and confidence in insights

## Why This Project Matters

As a **Principal Content Designer at Microsoft** working with data and AI systems, this project demonstrates:

1. **Deep understanding of analytics workflows** - Direct experience with the bottleneck between business questions and data answers
2. **UX for AI-assisted tools** - Designing transparency and explainability into LLM-powered systems
3. **Governance-aware design** - Building systems that respect organizational standards while reducing friction
4. **Accessibility for non-technical users** - Democratizing data access without sacrificing accuracy

This represents human-centered design for AI augmentation: making analysts more efficient while empowering stakeholders with self-service insights.

## Integration with Other Projects

**Semantic Metrics Modeling Assistant**
- Pulls metric definitions for consistent business logic
- Validates queries against trusted metric repository
- Maintains governance standards across both systems

**MCP Agent Ecosystem**
- Follows established MCP patterns from previous agents
- Shares architectural principles and tool design patterns
- Demonstrates range of MCP agent applications

## About

**Jen Kelleman**  
Principal Content Designer @ Microsoft

I design AI and data experiences that reduce cognitive load and build trust through transparent, well-instrumented systems.

### Connect
- [LinkedIn](https://linkedin.com/in/jenniferkelleman)
- [Medium](https://jenkelleman.medium.com)
- [AI Content Design Handbook](https://jkelleman.github.io/ai-content-design-handbook/)

### Other Projects
- **[Semantic Metrics Modeling Assistant](https://github.com/jkelleman/semantics-metrics-modeling-assistant)** - MCP agent for metrics governance and trust
- **[MCP-Oreilly](https://github.com/jkelleman/MCP-Oreilly)** - Three production MCP agents for content design, meeting analysis, and documentation
- **[AI Content Design Handbook](https://github.com/jkelleman/ai-content-design-handbook)** - Comprehensive guide to UX writing for AI systems

---

**Making data insights accessible, explainable, and trustworthy.**
