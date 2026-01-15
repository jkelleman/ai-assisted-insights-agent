# Usage Examples and Scenarios

This guide demonstrates real-world use cases for the AI-Assisted Insights Agent.

## Scenario 1: Product Manager - Quick Status Check

**Context:** Monday morning standup, need current metrics fast.

```
Question: "How many active users did we have last week?"

Response:
Answer: 12,470 users

Query Used:
SELECT COUNT(DISTINCT user_id)
FROM analytics.user_events
WHERE event_type = 'login'
  AND event_date >= CURRENT_DATE - INTERVAL '7 days'

Data Quality:
✓ Data is fresh (updated 2 hours ago)
✓ No missing days in date range
✓ Volume within expected range

Suggested Follow-ups:
• What was active users for the previous period?
• Show me active users broken down by day
• Compare to the same period last year
```

**Outcome:** Got answer in seconds, with full transparency on calculation and data quality.

---

## Scenario 2: Executive - Investigating Performance Change

**Context:** Revenue decreased 15% - need to understand why.

```
Question: "Why did revenue drop 15% last week?"

Step 1: Get the numbers
ask_question("What was revenue last week?")

Step 2: Add context
explain_result("208250", "revenue", "last week")

Response:
Result: 208,250 dollars
Context:
• Baseline (previous week): 245,000 dollars
• Change: -15.0% (decrease)
• Statistical Significance: Significant change

Interpretation:
This is a notable change that may warrant investigation.

Recommended Actions:
• Investigate root causes of significant change
• Compare to other related metrics
• Check for data quality issues
• Review recent product/marketing changes

Step 3: Drill down
ask_question("How many users signed up last week?")
compare_metrics("revenue", "signups", "last week")
```

**Outcome:** Root cause identified (signup drop), with reproducible queries for ongoing monitoring.

---

## Scenario 3: Data Analyst - Building Recurring Report

**Context:** Need to create a weekly report that can be easily reproduced.

```
Step 1: Generate and test query
generate_query("active_users", "last 7 days", "", "date")

Response:
SELECT date, COUNT(DISTINCT user_id)
FROM analytics.user_events
WHERE event_type = 'login'
  AND event_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY date

Step 2: Validate query
validate_query("SELECT date, COUNT(DISTINCT user_id) FROM analytics.user_events WHERE event_type = 'login' AND event_date >= CURRENT_DATE - INTERVAL '7 days' GROUP BY date")

Response:
✓ All validation checks passed
✓ Query is valid and ready to execute

Step 3: Save as template
save_query_template(
    "Weekly Active Users Report",
    "SELECT date, COUNT(DISTINCT user_id) FROM analytics.user_events WHERE event_type = 'login' AND event_date >= CURRENT_DATE - INTERVAL '7 days' GROUP BY date",
    "Daily breakdown of active users for the past week"
)

Response:
✓ Query Template Saved: Weekly Active Users Report
To run this template: run_template("Weekly Active Users Report")
```

**Outcome:** Reproducible weekly report that anyone can run, with built-in validation.

---

## Scenario 4: Stakeholder - Self-Service Insights

**Context:** Marketing manager needs conversion metrics for campaign planning.

```
Question: "What's our conversion rate for the past month?"

Response:
Answer: 2.3 percent

Query Used:
SELECT COUNT(DISTINCT CASE WHEN purchased = true THEN user_id END) * 100.0 / 
       COUNT(DISTINCT user_id)
FROM analytics.user_sessions
WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'

Explanation:
This query calculates percentage of visitors who completed a purchase 
from the analytics.user_sessions table.

Suggested Follow-ups:
• What was conversion rate for the previous period?
• Show me conversion rate broken down by day
• Compare to same period last year

Follow-up: "Compare to the previous month"
compare_metrics("conversion_rate", "conversion_rate", "last month")
```

**Outcome:** Self-service access without bothering analysts, with full transparency on methodology.

---

## Scenario 5: Data Quality Check Before Decision

**Context:** Making a major decision based on metric - need confidence in data quality.

```
Question: "What's our customer lifetime value?"

Step 1: Get the answer
ask_question("What's our customer lifetime value this quarter?")

Step 2: Check data quality thoroughly
check_data_quality("revenue", "this quarter")

Response:
Data Quality Report: Total Revenue
Time Period: this quarter

Freshness:
✓ Last updated: 2 hours ago
Data is current and recently refreshed

Completeness:
✓ Coverage: 100%
No gaps detected in date range

Anomaly Detection:
✓ No anomalies detected
Values are within 2σ of historical baseline

Overall Quality Score: 100/100

Recommendations:
✓ Data quality is excellent - proceed with confidence
```

**Outcome:** High confidence in decision, with documented data quality assessment.

---

## Scenario 6: Learning Available Metrics

**Context:** New team member needs to understand what metrics are available.

```
Action: Use the insights_query_guide prompt

Response:
# Guide to Asking Effective Data Questions

Available Metrics:
• Active Users - Unique users who logged in at least once
• Total Revenue - Sum of all completed transactions
• Conversion Rate - Percentage of visitors who purchased
• New Signups - Count of new user registrations

Example Questions:
- "How many users signed up last month?"
- "What was our revenue last quarter?"
- "Show me conversion rate for the past 7 days"
...
```

**Outcome:** Self-service discovery of available metrics and how to query them.

---

## Key Benefits Demonstrated

### Explainability
- Every answer shows the exact SQL query used
- Data quality indicators surface limitations
- Assumptions are made explicit

### Reproducibility
- Queries can be saved as templates
- Same question yields same query structure
- Version-controlled metric definitions ensure consistency

### Accessibility
- Non-technical stakeholders can self-serve
- Natural language eliminates SQL learning curve
- Suggestions guide users to relevant follow-ups

### Trust
- Transparent calculation methodology
- Data quality checks before critical decisions
- Statistical context (baselines, trends, significance)

---

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/jkelleman/ai-assisted-insights-agent.git
cd ai-assisted-insights-agent

# Install dependencies
uv pip install -e .

# Configure in Claude Desktop
{
  "mcpServers": {
    "ai-insights": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/ai-assisted-insights-agent",
        "run",
        "insights_agent/server.py"
      ]
    }
  }
}

# Restart Claude Desktop
```

---

## Best Practices

1. **Start with Data Quality** - Check freshness and completeness for critical decisions
2. **Save Reproducible Queries** - Use templates for recurring reports
3. **Compare Against Baselines** - Always provide historical context
4. **Validate Before Executing** - Use validate_query() on complex queries
5. **Document Assumptions** - Use explain_result() to surface limitations
