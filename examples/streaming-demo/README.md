# Streaming Services 2025 Demo

Test the AI-Assisted Insights Agent with realistic 2025 streaming services data.

## Dataset Overview

This demo includes sample data for major streaming platforms in 2025:
- Netflix
- Disney+
- Max (formerly HBO Max)
- Apple TV+
- Paramount+
- Peacock

**Metrics Available:**
- Total Subscribers
- New Subscribers
- Monthly Recurring Revenue (MRR)
- Average Revenue Per User (ARPU)
- Churn Rate
- Engagement Rate
- Average Watch Time
- Content Completion Rate
- Customer Lifetime Value (LTV)
- Platform Market Share
- Premium Plan Adoption

## Quick Start

### 1. Use the Streaming Configuration

```bash
# Copy the streaming config
cp config_streaming.yaml config.yaml

# Or specify it when running
python -m insights_agent.cli --config config_streaming.yaml
```

### 2. Start the CLI

```bash
python -m insights_agent.cli
```

### 3. Try These Questions

**Subscriber Metrics:**
```
insights> ask How many total subscribers do we have?
insights> ask What's our new subscriber count for last month?
insights> ask Compare total subscribers across platforms
```

**Revenue Analysis:**
```
insights> ask What's our monthly recurring revenue?
insights> ask Show me average revenue per user
insights> ask What's the premium plan adoption rate?
```

**Engagement Metrics:**
```
insights> ask What's our user engagement rate?
insights> ask Show me average watch time per user
insights> ask What's the content completion rate?
```

**Churn Analysis:**
```
insights> ask What's our churn rate?
insights> ask What's the customer lifetime value?
insights> ask Compare churn rate to last quarter
```

**Comparative Analysis:**
```
insights> compare total_subscribers monthly_revenue "last 90 days"
insights> compare engagement_rate churn_rate "this year"
insights> compare average_watch_time content_completion_rate "last month"
```

## Example Queries

### Business Questions

**"How healthy is our streaming business?"**
```
insights> ask What's our total subscriber count?
insights> ask What's the churn rate?
insights> ask Show me engagement rate
insights> check data quality for total_subscribers
```

**"Which platform is performing best?"**
```
insights> generate platform_market_share "last 90 days" "" "platform"
insights> compare total_subscribers monthly_revenue "this quarter"
```

**"Are users watching our content?"**
```
insights> ask What's the average watch time?
insights> ask What's the content completion rate?
insights> ask Show me engagement rate for last month
```

**"How much revenue are we generating?"**
```
insights> ask What's our monthly recurring revenue?
insights> ask What's the ARPU?
insights> ask Show me premium adoption rate
```

**"Are we retaining customers?"**
```
insights> ask What's the churn rate?
insights> ask What's the customer lifetime value?
insights> compare churn_rate engagement_rate "this year"
```

## Data Generation (Optional)

If you want more realistic data, you can generate it:

```python
# Run this Python script to generate larger dataset
python examples/streaming-demo/generate_data.py
```

This will create:
- 10,000 subscriber records
- 50,000 viewing activity records
- Monthly revenue data
- Churn events
- Content library

## Metrics Definitions

### Total Subscribers
**What it measures:** Count of active subscribers across all platforms
**Business value:** Core growth metric
**Query:** `COUNT(DISTINCT user_id) WHERE status = 'active'`

### Churn Rate
**What it measures:** Percentage of subscribers who cancelled
**Business value:** Retention health indicator
**Query:** `COUNT(churned) / COUNT(total) * 100`

### Engagement Rate
**What it measures:** Percentage of subscribers actively watching content
**Business value:** Product stickiness indicator
**Query:** `COUNT(active_viewers) / COUNT(subscribers) * 100`

### ARPU (Average Revenue Per User)
**What it measures:** Average monthly revenue per subscriber
**Business value:** Monetization effectiveness
**Query:** `AVG(monthly_revenue)`

### Content Completion Rate
**What it measures:** Percentage of started content that users finish
**Business value:** Content quality indicator
**Query:** `COUNT(completed) / COUNT(started) * 100`

## Sample Analysis Workflow

```
# 1. Check overall health
insights> ask How many total subscribers do we have?
insights> ask What's our churn rate?

# 2. Assess data quality
insights> quality total_subscribers "last 30 days"
insights> quality churn_rate "last 30 days"

# 3. Analyze revenue
insights> ask What's our monthly recurring revenue?
insights> ask What's the ARPU?

# 4. Deep dive into engagement
insights> ask What's the engagement rate?
insights> ask Show me average watch time
insights> ask What's the content completion rate?

# 5. Compare key metrics
insights> compare engagement_rate churn_rate "last 90 days"
insights> compare total_subscribers monthly_revenue "this year"

# 6. Save useful queries
insights> save_template "Monthly Metrics" "SELECT COUNT(*) FROM subscriptions" "Monthly subscriber count"
insights> templates
```

## Use with Claude Desktop

Configure Claude Desktop to use the streaming config:

**Windows:**
```json
{
  "mcpServers": {
    "insights-agent-streaming": {
      "command": "python",
      "args": ["-m", "insights_agent.server"],
      "cwd": "C:\\path\\to\\ai-assisted-insights-agent",
      "env": {
        "CONFIG_PATH": "config_streaming.yaml"
      }
    }
  }
}
```

**Then ask Claude:**
```
"What are our key streaming metrics for 2025?"
"How is our churn rate compared to engagement?"
"Show me the revenue analysis for Q4"
"Which platform has the most subscribers?"
```

## Real-World Questions to Try

1. **Product Manager:** "Is our engagement declining?"
2. **Executive:** "What's driving our revenue growth?"
3. **Analyst:** "Which user segments are churning most?"
4. **Marketing:** "What's our acquisition efficiency?"
5. **Finance:** "What's our LTV:CAC ratio trending?"

## Tips for Testing

- Start with simple questions to understand the data
- Use `metrics` command to see all available metrics
- Use `quality` command before important decisions
- Save frequently used queries as templates
- Export history for reporting: `history` command

## Limitations (Demo Data)

This is simulated data for demonstration:
- 20 sample subscriber records
- Aggregated metrics are simulated
- Real production would connect to actual database
- Data quality checks return simulated results

For production use, connect to your real data warehouse!
