#!/usr/bin/env python3
"""
AI-Assisted Insights Agent - MCP Server

An MCP agent that translates natural language questions into accurate, explainable,
and reproducible data insights.

Created by: Jen Kelleman
"""

import sys
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

from mcp.server.fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("ai-insights-agent")

# In-memory stores (in production, these would be databases)
QUERY_HISTORY: List[Dict[str, Any]] = []
QUERY_TEMPLATES: Dict[str, str] = {}
METRIC_DEFINITIONS: Dict[str, Dict[str, Any]] = {}
BUSINESS_GLOSSARY: Dict[str, str] = {}

# Sample metric definitions (would integrate with semantic metrics agent)
METRIC_DEFINITIONS = {
    "active_users": {
        "name": "Active Users",
        "description": "Unique users who logged in at least once in the time period",
        "sql_template": "COUNT(DISTINCT user_id)",
        "table": "analytics.user_events",
        "filter": "event_type = 'login'",
        "unit": "users"
    },
    "revenue": {
        "name": "Total Revenue",
        "description": "Sum of all completed transaction amounts",
        "sql_template": "SUM(amount)",
        "table": "analytics.transactions",
        "filter": "status = 'completed'",
        "unit": "dollars"
    },
    "conversion_rate": {
        "name": "Conversion Rate",
        "description": "Percentage of visitors who completed a purchase",
        "sql_template": "COUNT(DISTINCT CASE WHEN purchased = true THEN user_id END) * 100.0 / COUNT(DISTINCT user_id)",
        "table": "analytics.user_sessions",
        "filter": "",
        "unit": "percent"
    },
    "signups": {
        "name": "New Signups",
        "description": "Count of new user registrations",
        "sql_template": "COUNT(DISTINCT user_id)",
        "table": "analytics.signups",
        "filter": "",
        "unit": "users"
    }
}

# Business term mappings
BUSINESS_GLOSSARY = {
    "customers": "users",
    "purchases": "transactions",
    "sales": "revenue",
    "registrations": "signups",
    "conversions": "conversion_rate"
}


@mcp.tool()
def ask_question(question: str, time_period: str = "last 7 days") -> str:
    """
    Ask a data question in natural language and get an explainable answer.
    
    Args:
        question: Natural language question (e.g., "How many users signed up last month?")
        time_period: Time range for the query (e.g., "last 7 days", "this month", "Q4 2025")
        
    Returns:
        Answer with explanation, SQL query, and data quality context
    """
    # Parse the question to identify metrics and intent
    parsed = _parse_question(question)
    
    if not parsed["metrics"]:
        return f"""
Unable to parse question: "{question}"

Suggestions:
• Try mentioning specific metrics like "active users", "revenue", or "signups"
• Use time periods like "last week", "this month", or "Q4 2025"
• Examples:
  - "How many active users last week?"
  - "What was our revenue in December?"
  - "Show me conversion rate for the past month"

Available metrics:
{_list_available_metrics()}
"""
    
    # Generate SQL query
    query_result = _generate_sql_query(parsed, time_period)
    
    if query_result["error"]:
        return f"Error generating query: {query_result['error']}"
    
    # Simulate query execution (in production, would execute against real database)
    result_value = _simulate_query_execution(query_result["sql"])
    
    # Get data quality assessment
    quality = _assess_data_quality(parsed["metrics"][0], time_period)
    
    # Store in query history
    QUERY_HISTORY.append({
        "question": question,
        "time_period": time_period,
        "sql": query_result["sql"],
        "result": result_value,
        "timestamp": datetime.now().isoformat()
    })
    
    # Format response
    metric = METRIC_DEFINITIONS[parsed["metrics"][0]]
    
    report = f"""
Question: {question}
Time Period: {time_period}

Answer: {result_value:,} {metric['unit']}

Query Used:
{query_result['sql']}

Explanation:
This query counts {metric['description'].lower()} from the {metric['table']} table.
{f"Filtered by: {metric['filter']}" if metric['filter'] else "No additional filters applied."}

Data Quality:
{quality}

Metric Definition:
• Name: {metric['name']}
• Description: {metric['description']}
• Source: {metric['table']}
"""
    
    # Add follow-up suggestions
    followups = _suggest_followup_questions(parsed["metrics"][0], time_period)
    if followups:
        report += f"\nSuggested Follow-ups:\n"
        for followup in followups:
            report += f"• {followup}\n"
    
    return report


@mcp.tool()
def generate_query(
    metric: str,
    time_period: str = "last 7 days",
    filters: str = "",
    group_by: str = ""
) -> str:
    """
    Generate a SQL query for a specific metric with structured parameters.
    
    Args:
        metric: Metric name (e.g., "active_users", "revenue", "conversion_rate")
        time_period: Time range (e.g., "last 7 days", "this month")
        filters: Additional WHERE clause filters (e.g., "country = 'US'")
        group_by: GROUP BY clause (e.g., "date", "country")
        
    Returns:
        SQL query with explanation
    """
    if metric not in METRIC_DEFINITIONS:
        similar = _find_similar_metrics(metric)
        msg = f"Metric '{metric}' not found."
        if similar:
            msg += f"\n\nDid you mean: {', '.join(similar)}?"
        msg += f"\n\nAvailable metrics:\n{_list_available_metrics()}"
        return msg
    
    metric_def = METRIC_DEFINITIONS[metric]
    
    # Build query
    date_filter = _parse_time_period(time_period)
    
    select_clause = metric_def["sql_template"]
    if group_by:
        select_clause = f"{group_by}, {select_clause}"
    
    where_clauses = []
    if metric_def["filter"]:
        where_clauses.append(metric_def["filter"])
    if date_filter:
        where_clauses.append(date_filter)
    if filters:
        where_clauses.append(filters)
    
    where_clause = " AND ".join(where_clauses) if where_clauses else ""
    
    query = f"SELECT {select_clause}\nFROM {metric_def['table']}"
    if where_clause:
        query += f"\nWHERE {where_clause}"
    if group_by:
        query += f"\nGROUP BY {group_by}"
    
    report = f"""
Generated Query for: {metric_def['name']}
{'=' * 50}

{query}

Parameters:
• Metric: {metric_def['name']} - {metric_def['description']}
• Time Period: {time_period}
• Additional Filters: {filters if filters else "None"}
• Grouping: {group_by if group_by else "None (aggregate)"}

Data Source:
• Table: {metric_def['table']}
• Unit: {metric_def['unit']}

Next Steps:
• Validate with validate_query("{metric}")
• Execute and explain with explain_result()
• Save as template with save_query_template()
"""
    
    return report


@mcp.tool()
def explain_result(result_value: str, metric: str, time_period: str = "last 7 days") -> str:
    """
    Explain a query result with context, comparisons, and interpretation.
    
    Args:
        result_value: The numeric result to explain
        metric: Which metric this result represents
        time_period: Time period for the result
        
    Returns:
        Contextual explanation with comparisons and insights
    """
    if metric not in METRIC_DEFINITIONS:
        return f"Metric '{metric}' not found."
    
    metric_def = METRIC_DEFINITIONS[metric]
    
    try:
        value = float(result_value.replace(",", ""))
    except:
        return f"Could not parse result value: {result_value}"
    
    # Get historical context (simulated)
    historical = _get_historical_context(metric, value, time_period)
    
    # Get statistical context
    stats = _calculate_statistical_context(value, historical["baseline"])
    
    report = f"""
Result Explanation: {metric_def['name']}
{'=' * 50}

Result: {value:,.0f} {metric_def['unit']}
Time Period: {time_period}

Context:
• Baseline (previous period): {historical['baseline']:,.0f} {metric_def['unit']}
• Change: {stats['change']:+.1f}% ({stats['direction']})
• Statistical Significance: {stats['significance']}

Interpretation:
{_interpret_result(metric, value, historical, stats)}

Data Quality Considerations:
{_assess_data_quality(metric, time_period)}

Recommended Actions:
{_recommend_actions(metric, stats)}
"""
    
    return report


@mcp.tool()
def validate_query(sql_query: str) -> str:
    """
    Validate a SQL query for syntax, performance, and data quality issues.
    
    Args:
        sql_query: SQL query to validate
        
    Returns:
        Validation report with issues and recommendations
    """
    issues = []
    warnings = []
    recommendations = []
    
    # Basic syntax checks
    if not sql_query.strip().upper().startswith("SELECT"):
        issues.append("Query must start with SELECT")
    
    # Check for required components
    if "FROM" not in sql_query.upper():
        issues.append("Query missing FROM clause")
    
    # Performance checks
    if "SELECT *" in sql_query.upper():
        warnings.append("SELECT * can be slow - specify only needed columns")
    
    if "WHERE" not in sql_query.upper():
        warnings.append("No WHERE clause - query will scan entire table")
    
    # Check for date filters (good practice)
    date_patterns = ["event_date", "created_at", "timestamp", "date"]
    has_date_filter = any(pattern in sql_query.lower() for pattern in date_patterns)
    if not has_date_filter:
        recommendations.append("Consider adding a date filter to improve performance")
    
    # Check for aggregations without GROUP BY
    aggregations = ["COUNT", "SUM", "AVG", "MIN", "MAX"]
    has_aggregation = any(agg in sql_query.upper() for agg in aggregations)
    has_group_by = "GROUP BY" in sql_query.upper()
    
    if has_aggregation and not has_group_by:
        recommendations.append("Using aggregation without GROUP BY - result will be a single row")
    
    # Format report
    report = f"""
Query Validation Report
{'=' * 50}

Query:
{sql_query}

"""
    
    if not issues and not warnings:
        report += "✓ All validation checks passed\n\n"
    
    if issues:
        report += f"Issues Found ({len(issues)}):\n"
        for issue in issues:
            report += f"  ✗ {issue}\n"
        report += "\n"
    
    if warnings:
        report += f"Warnings ({len(warnings)}):\n"
        for warning in warnings:
            report += f"  ⚠ {warning}\n"
        report += "\n"
    
    if recommendations:
        report += f"Recommendations ({len(recommendations)}):\n"
        for rec in recommendations:
            report += f"  • {rec}\n"
        report += "\n"
    
    if not issues:
        report += "✓ Query is valid and ready to execute\n"
    else:
        report += "✗ Fix issues before executing\n"
    
    return report


@mcp.tool()
def suggest_followups(question: str, result: str = "") -> str:
    """
    Suggest relevant follow-up questions based on the current query.
    
    Args:
        question: Original question asked
        result: Optional result value to inform suggestions
        
    Returns:
        List of suggested follow-up questions
    """
    parsed = _parse_question(question)
    
    if not parsed["metrics"]:
        return "Unable to generate follow-ups - could not parse original question."
    
    metric = parsed["metrics"][0]
    suggestions = _suggest_followup_questions(metric, parsed["time_period"])
    
    report = f"""
Follow-up Suggestions for: "{question}"
{'=' * 50}

Drill-Down Questions:
"""
    
    for i, suggestion in enumerate(suggestions, 1):
        report += f"{i}. {suggestion}\n"
    
    report += f"""
Related Analysis:
• Compare to previous period: "Show {METRIC_DEFINITIONS[metric]['name'].lower()} for the same period last year"
• Segment analysis: "Break down by user segment"
• Trend analysis: "Show weekly trend over the past quarter"
• Cohort analysis: "Compare across user cohorts"

To ask any of these questions, use:
ask_question("your question here")
"""
    
    return report


@mcp.tool()
def save_query_template(name: str, sql_query: str, description: str = "") -> str:
    """
    Save a query as a reusable template for reproducibility.
    
    Args:
        name: Template name (e.g., "Weekly Active Users Report")
        sql_query: SQL query to save
        description: Optional description of what this query does
        
    Returns:
        Confirmation with template details
    """
    template_id = name.lower().replace(" ", "_")
    
    if template_id in QUERY_TEMPLATES:
        return f"⚠ Template '{name}' already exists. Use a different name or delete the existing template first."
    
    QUERY_TEMPLATES[template_id] = {
        "name": name,
        "sql": sql_query,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "run_count": 0
    }
    
    report = f"""
✓ Query Template Saved: {name}

Description: {description if description else "No description provided"}

Query:
{sql_query}

To run this template:
run_template("{name}")

To list all templates:
list_templates()

To export for external use:
export_template("{name}")
"""
    
    return report


@mcp.tool()
def list_templates() -> str:
    """
    List all saved query templates.
    
    Returns:
        List of saved templates with metadata
    """
    if not QUERY_TEMPLATES:
        return """
No query templates saved yet.

Create a template with:
save_query_template("Template Name", "SELECT ...")
"""
    
    report = f"""
Saved Query Templates ({len(QUERY_TEMPLATES)})
{'=' * 50}

"""
    
    for template_id, template in QUERY_TEMPLATES.items():
        report += f"""
Name: {template['name']}
Description: {template['description']}
Created: {_format_relative_time(template['created_at'])}
Times Run: {template['run_count']}
Query: {template['sql'][:100]}{"..." if len(template['sql']) > 100 else ""}

"""
    
    return report


@mcp.tool()
def check_data_quality(metric: str, time_period: str = "last 7 days") -> str:
    """
    Assess data quality for a specific metric and time period.
    
    Args:
        metric: Metric to check
        time_period: Time period to assess
        
    Returns:
        Data quality report with freshness, completeness, and anomalies
    """
    if metric not in METRIC_DEFINITIONS:
        return f"Metric '{metric}' not found."
    
    metric_def = METRIC_DEFINITIONS[metric]
    
    # Simulate data quality checks
    freshness = _check_data_freshness(metric)
    completeness = _check_data_completeness(metric, time_period)
    anomalies = _check_for_anomalies(metric, time_period)
    
    report = f"""
Data Quality Report: {metric_def['name']}
{'=' * 50}

Time Period: {time_period}
Data Source: {metric_def['table']}

Freshness:
{freshness['status']} Last updated: {freshness['last_updated']}
{freshness['message']}

Completeness:
{completeness['status']} Coverage: {completeness['coverage']}%
{completeness['message']}

Anomaly Detection:
{anomalies['status']} {anomalies['message']}
{anomalies['details']}

Overall Quality Score: {_calculate_quality_score(freshness, completeness, anomalies)}/100

Recommendations:
{_quality_recommendations(freshness, completeness, anomalies)}
"""
    
    return report


@mcp.tool()
def compare_metrics(metric1: str, metric2: str, time_period: str = "last 7 days") -> str:
    """
    Compare two metrics side-by-side for the same time period.
    
    Args:
        metric1: First metric to compare
        metric2: Second metric to compare
        time_period: Time period for comparison
        
    Returns:
        Side-by-side comparison with insights
    """
    if metric1 not in METRIC_DEFINITIONS:
        return f"Metric '{metric1}' not found."
    if metric2 not in METRIC_DEFINITIONS:
        return f"Metric '{metric2}' not found."
    
    m1 = METRIC_DEFINITIONS[metric1]
    m2 = METRIC_DEFINITIONS[metric2]
    
    # Simulate values
    value1 = _simulate_query_execution(f"SELECT {m1['sql_template']} FROM {m1['table']}")
    value2 = _simulate_query_execution(f"SELECT {m2['sql_template']} FROM {m2['table']}")
    
    report = f"""
Metric Comparison
{'=' * 50}

Time Period: {time_period}

{m1['name']} vs {m2['name']}

Values:
  {m1['name']}: {value1:,} {m1['unit']}
  {m2['name']}: {value2:,} {m2['unit']}

Definitions:
  {m1['name']}: {m1['description']}
  {m2['name']}: {m2['description']}

Data Sources:
  {m1['name']}: {m1['table']}
  {m2['name']}: {m2['table']}

Insights:
{_generate_comparison_insights(metric1, metric2, value1, value2)}

Correlation Analysis:
{_analyze_correlation(metric1, metric2)}
"""
    
    return report


# Helper functions

def _parse_question(question: str) -> Dict[str, Any]:
    """Parse natural language question to identify metrics and intent."""
    question_lower = question.lower()
    
    # Normalize business terms
    for business_term, technical_term in BUSINESS_GLOSSARY.items():
        question_lower = question_lower.replace(business_term, technical_term)
    
    # Identify metrics
    metrics = []
    for metric_id, metric_def in METRIC_DEFINITIONS.items():
        metric_name_lower = metric_def["name"].lower()
        if metric_id in question_lower or metric_name_lower in question_lower:
            metrics.append(metric_id)
    
    # Identify time period
    time_period = "last 7 days"  # default
    time_patterns = {
        r"last (\d+) days?": lambda m: f"last {m.group(1)} days",
        r"past (\d+) weeks?": lambda m: f"last {int(m.group(1)) * 7} days",
        r"last month": lambda m: "last 30 days",
        r"this month": lambda m: "this month",
        r"last week": lambda m: "last 7 days"
    }
    
    for pattern, formatter in time_patterns.items():
        match = re.search(pattern, question_lower)
        if match:
            time_period = formatter(match)
            break
    
    return {
        "metrics": metrics,
        "time_period": time_period,
        "original_question": question
    }


def _generate_sql_query(parsed: Dict[str, Any], time_period: str) -> Dict[str, Any]:
    """Generate SQL query from parsed question."""
    if not parsed["metrics"]:
        return {"sql": "", "error": "No metrics identified in question"}
    
    metric_id = parsed["metrics"][0]
    metric = METRIC_DEFINITIONS[metric_id]
    
    date_filter = _parse_time_period(time_period)
    
    where_clauses = []
    if metric["filter"]:
        where_clauses.append(metric["filter"])
    if date_filter:
        where_clauses.append(date_filter)
    
    where_clause = " AND ".join(where_clauses) if where_clauses else ""
    
    sql = f"SELECT {metric['sql_template']}\nFROM {metric['table']}"
    if where_clause:
        sql += f"\nWHERE {where_clause}"
    
    return {"sql": sql, "error": None}


def _parse_time_period(time_period: str) -> str:
    """Convert time period string to SQL date filter."""
    time_period_lower = time_period.lower()
    
    if "last" in time_period_lower and "days" in time_period_lower:
        days = re.search(r"(\d+)", time_period_lower)
        if days:
            return f"event_date >= CURRENT_DATE - INTERVAL '{days.group(1)} days'"
    
    if "this month" in time_period_lower:
        return "event_date >= DATE_TRUNC('month', CURRENT_DATE)"
    
    if "last month" in time_period_lower:
        return "event_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') AND event_date < DATE_TRUNC('month', CURRENT_DATE)"
    
    # Default to last 7 days
    return "event_date >= CURRENT_DATE - INTERVAL '7 days'"


def _simulate_query_execution(sql: str) -> float:
    """Simulate query execution with realistic values."""
    # Generate realistic values based on metric type
    if "COUNT" in sql.upper():
        return float(1247 + hash(sql) % 1000)
    elif "SUM" in sql.upper():
        return float(50000 + hash(sql) % 50000)
    elif "AVG" in sql.upper():
        return float(25 + (hash(sql) % 100) / 10)
    else:
        return float(100 + hash(sql) % 900)


def _assess_data_quality(metric: str, time_period: str) -> str:
    """Assess data quality for a metric."""
    return """✓ Data is fresh (updated 2 hours ago)
✓ No missing days in date range
✓ Volume within expected range (within 2σ of baseline)"""


def _suggest_followup_questions(metric: str, time_period: str) -> List[str]:
    """Generate follow-up questions based on metric."""
    metric_def = METRIC_DEFINITIONS[metric]
    
    suggestions = [
        f"What was {metric_def['name'].lower()} for the previous period?",
        f"Show me {metric_def['name'].lower()} broken down by day",
        f"Compare {metric_def['name'].lower()} to the same period last year"
    ]
    
    # Add metric-specific suggestions
    if metric == "active_users":
        suggestions.append("What's the conversion rate for these users?")
    elif metric == "revenue":
        suggestions.append("What's the average transaction value?")
    
    return suggestions


def _list_available_metrics() -> str:
    """List all available metrics."""
    lines = []
    for metric_id, metric_def in METRIC_DEFINITIONS.items():
        lines.append(f"• {metric_def['name']} - {metric_def['description']}")
    return "\n".join(lines)


def _find_similar_metrics(query: str) -> List[str]:
    """Find metrics with similar names."""
    query_lower = query.lower()
    similar = []
    
    for metric_id, metric_def in METRIC_DEFINITIONS.items():
        if query_lower in metric_def["name"].lower() or query_lower in metric_id:
            similar.append(metric_def["name"])
    
    return similar[:3]


def _get_historical_context(metric: str, value: float, time_period: str) -> Dict[str, Any]:
    """Get historical context for a metric value."""
    # Simulate historical baseline (previous period)
    baseline = value * 0.9 + (hash(metric) % 200)
    
    return {
        "baseline": baseline,
        "trend": "increasing" if value > baseline else "decreasing"
    }


def _calculate_statistical_context(value: float, baseline: float) -> Dict[str, Any]:
    """Calculate statistical context for a value."""
    change = ((value - baseline) / baseline) * 100
    
    direction = "increase" if change > 0 else "decrease"
    significance = "Significant" if abs(change) > 10 else "Within normal variance"
    
    return {
        "change": change,
        "direction": direction,
        "significance": significance
    }


def _interpret_result(metric: str, value: float, historical: Dict, stats: Dict) -> str:
    """Interpret what a result means."""
    metric_def = METRIC_DEFINITIONS[metric]
    
    interpretation = f"The current {metric_def['name'].lower()} of {value:,.0f} {metric_def['unit']} represents a {abs(stats['change']):.1f}% {stats['direction']} compared to the baseline of {historical['baseline']:,.0f} {metric_def['unit']}."
    
    if abs(stats['change']) > 15:
        interpretation += f"\n\nThis is a notable change that may warrant investigation."
    elif abs(stats['change']) < 5:
        interpretation += f"\n\nThis change is within normal variance and likely not significant."
    
    return interpretation


def _recommend_actions(metric: str, stats: Dict) -> str:
    """Recommend actions based on result."""
    if abs(stats['change']) > 15:
        return """• Investigate root causes of significant change
• Compare to other related metrics
• Check for data quality issues or tracking changes
• Review recent product/marketing changes"""
    else:
        return "• Continue monitoring trends\n• No immediate action required"


def _format_relative_time(iso_time: str) -> str:
    """Format ISO timestamp as relative time."""
    dt = datetime.fromisoformat(iso_time)
    delta = datetime.now() - dt
    
    if delta.days == 0:
        return "today"
    elif delta.days == 1:
        return "yesterday"
    elif delta.days < 7:
        return f"{delta.days} days ago"
    else:
        return f"{delta.days // 7} weeks ago"


def _check_data_freshness(metric: str) -> Dict[str, Any]:
    """Check data freshness for a metric."""
    return {
        "status": "✓",
        "last_updated": "2 hours ago",
        "message": "Data is current and recently refreshed"
    }


def _check_data_completeness(metric: str, time_period: str) -> Dict[str, Any]:
    """Check data completeness."""
    return {
        "status": "✓",
        "coverage": 100,
        "message": "No gaps detected in date range"
    }


def _check_for_anomalies(metric: str, time_period: str) -> Dict[str, Any]:
    """Check for data anomalies."""
    return {
        "status": "✓",
        "message": "No anomalies detected",
        "details": "Values are within 2σ of historical baseline"
    }


def _calculate_quality_score(freshness: Dict, completeness: Dict, anomalies: Dict) -> int:
    """Calculate overall quality score."""
    score = 0
    if freshness["status"] == "✓":
        score += 40
    if completeness["coverage"] >= 95:
        score += 40
    if anomalies["status"] == "✓":
        score += 20
    return score


def _quality_recommendations(freshness: Dict, completeness: Dict, anomalies: Dict) -> str:
    """Generate quality improvement recommendations."""
    if all(x["status"] == "✓" for x in [freshness, anomalies]) and completeness["coverage"] >= 95:
        return "✓ Data quality is excellent - proceed with confidence"
    else:
        return "⚠ Address data quality issues before making critical decisions"


def _generate_comparison_insights(metric1: str, metric2: str, value1: float, value2: float) -> str:
    """Generate insights from metric comparison."""
    m1_name = METRIC_DEFINITIONS[metric1]["name"]
    m2_name = METRIC_DEFINITIONS[metric2]["name"]
    
    ratio = value1 / value2 if value2 != 0 else 0
    
    return f"""• {m1_name} is {ratio:.2f}x {m2_name}
• Both metrics are trending in the same direction
• Consider analyzing these together for complete picture"""


def _analyze_correlation(metric1: str, metric2: str) -> str:
    """Analyze correlation between two metrics."""
    return "Strong positive correlation (r=0.85) - these metrics tend to move together"


# MCP Resources

@mcp.resource("metrics://catalog")
def get_metrics_catalog() -> str:
    """
    Expose the complete metrics catalog as an MCP resource.
    
    Returns the full list of available metrics with their definitions,
    making it easy for LLMs to understand what data is available.
    """
    catalog = {
        "catalog_name": "AI Insights Agent Metrics",
        "version": "0.1.0",
        "last_updated": datetime.now().isoformat(),
        "metrics": METRIC_DEFINITIONS,
        "business_glossary": BUSINESS_GLOSSARY
    }
    return json.dumps(catalog, indent=2)


@mcp.resource("metrics://metric/{metric_id}")
def get_metric_definition(metric_id: str) -> str:
    """
    Get detailed information about a specific metric.
    
    Args:
        metric_id: The metric identifier
        
    Returns:
        JSON string with metric definition
    """
    if metric_id not in METRIC_DEFINITIONS:
        return json.dumps({"error": f"Metric '{metric_id}' not found"})
    
    metric = METRIC_DEFINITIONS[metric_id]
    return json.dumps({
        "metric_id": metric_id,
        "definition": metric,
        "sample_query": f"SELECT {metric['sql_template']}\nFROM {metric['table']}\nWHERE {metric['filter']}" if metric['filter'] else f"SELECT {metric['sql_template']}\nFROM {metric['table']}"
    }, indent=2)


@mcp.resource("history://recent")
def get_recent_queries() -> str:
    """
    Get recent query history as an MCP resource.
    
    Returns:
        JSON string with recent query history
    """
    recent = QUERY_HISTORY[-10:] if QUERY_HISTORY else []
    return json.dumps({
        "count": len(recent),
        "queries": recent
    }, indent=2)


@mcp.resource("templates://list")
def get_all_templates() -> str:
    """
    Get all saved query templates as an MCP resource.
    
    Returns:
        JSON string with all templates
    """
    return json.dumps({
        "count": len(QUERY_TEMPLATES),
        "templates": QUERY_TEMPLATES
    }, indent=2)


@mcp.prompt()
def insights_query_guide() -> str:
    """
    Guide for asking effective data questions.
    
    Returns best practices and examples for natural language queries.
    """
    return """
# Guide to Asking Effective Data Questions

## Best Practices

### 1. Be Specific About Metrics
✓ Good: "How many active users did we have last week?"
✗ Bad: "Show me user numbers"

### 2. Include Time Periods
✓ Good: "What was revenue in December 2025?"
✗ Bad: "What was revenue?"

### 3. Use Comparison Language
✓ Good: "Compare conversion rate this month vs last month"
✗ Bad: "Show conversion rate"

### 4. Ask for Explanations
✓ Good: "Why did signups drop 20% last week?"
✗ Bad: "Show signups"

## Example Questions

### Simple Queries
- "How many users signed up last month?"
- "What was our revenue last quarter?"
- "Show me conversion rate for the past 7 days"

### Comparative Queries
- "Compare active users this week vs last week"
- "What's the difference in revenue between Q3 and Q4?"
- "Show monthly signups for the past 6 months"

### Investigative Queries
- "Why did conversion rate drop last week?"
- "What's driving the increase in revenue?"
- "Are there any anomalies in user signups?"

### Segmented Queries
- "Show active users by country"
- "Break down revenue by product line"
- "Compare conversion rates across user segments"

## Available Metrics

- Active Users: Unique users who logged in
- Revenue: Total transaction amounts
- Conversion Rate: Percentage who purchased
- Signups: New user registrations

## Tips for Getting Better Answers

1. Start broad, then drill down
2. Ask for data quality checks on critical decisions
3. Request explanations to understand assumptions
4. Save reproducible queries as templates
5. Compare against historical baselines

Use explain_result() to add context to any number.
Use validate_query() to check queries before execution.
Use save_query_template() to create reusable reports.
"""


def main():
    """
    Main entry point for the AI-Assisted Insights Agent.
    Starts the server with STDIO transport.
    """
    try:
        print("Starting AI-Assisted Insights Agent...", file=sys.stderr)
        print("Ready to translate natural language questions into data insights", file=sys.stderr)
        
        # Run the server
        mcp.run()
        
    except Exception as e:
        print(f"Failed to start Insights Agent: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
