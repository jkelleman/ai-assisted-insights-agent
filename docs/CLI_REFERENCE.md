# CLI Commands Reference Guide

Complete guide to using the AI-Assisted Insights Agent Interactive CLI.

---

## Starting the CLI

```bash
# Basic start
python -m insights_agent.cli

# With custom config
python -m insights_agent.cli --config config_streaming.yaml
```

---

## Core Commands

### 📊 ASKING QUESTIONS

#### `ask` (or `question`, `q`)
Ask data questions in natural language.

**Syntax:**
```
ask <your question>
```

**Examples:**
```
insights> ask How many subscribers do we have?
insights> ask What's our churn rate last month?
insights> ask Show me revenue for Q4
insights> q What's the engagement rate?  (shortcut)
```

**What You'll Get:**
- ✅ Direct answer with the number
- ✅ The SQL query that generated it
- ✅ Explanation of how it was calculated
- ✅ Data quality assessment
- ✅ Suggested follow-up questions

**Tips:**
- Be specific about time periods
- Use metric names from the catalog
- Ask one question at a time
- Natural language works best

---

### 🔧 QUERY GENERATION

#### `generate`
Generate SQL for specific metrics with structured parameters.

**Syntax:**
```
generate <metric> [time_period] [filters] [group_by]
```

**Examples:**
```
insights> generate total_subscribers
insights> generate revenue "last 30 days"
insights> generate active_users "this month" "country='USA'" 
insights> generate platform_market_share "last 90 days" "" "platform"
```

**Parameters:**
- `metric` - Required. Use `metrics` command to see all available
- `time_period` - Optional. Defaults to "last 7 days"
  - Examples: "last 7 days", "this month", "last quarter"
- `filters` - Optional. Additional WHERE clause conditions in quotes
  - Example: "country='USA'" or "platform='Netflix'"
- `group_by` - Optional. Column to group results by
  - Example: "platform", "date", "country"

**What You'll Get:**
- ✅ Complete SQL query
- ✅ Parameter breakdown
- ✅ Data source information
- ✅ Next steps suggestions

**Use Cases:**
- Building dashboard queries
- Creating reports
- Learning SQL patterns
- Debugging query issues

---

### ✅ QUERY VALIDATION

#### `validate`
Check SQL queries for errors and performance issues.

**Syntax:**
```
validate <sql_query>
```

**Examples:**
```
insights> validate SELECT COUNT(*) FROM users WHERE date >= '2025-01-01'
insights> validate SELECT * FROM subscriptions
```

**What Gets Checked:**
- ✅ Syntax errors (missing SELECT, FROM, etc.)
- ✅ Performance issues (SELECT *, no WHERE clause)
- ✅ Best practices (date filters, aggregations)
- ✅ Query structure

**Validation Levels:**
- ❌ **Issues** - Must fix (syntax errors)
- ⚠️ **Warnings** - Should fix (performance problems)
- 💡 **Recommendations** - Nice to have (optimizations)

---

### 📈 RESULT EXPLANATION

#### `explain`
Add context and interpretation to query results.

**Syntax:**
```
explain <result_value> <metric> [time_period]
```

**Examples:**
```
insights> explain 1500 total_subscribers "last 7 days"
insights> explain 15.2 churn_rate "last month"
insights> explain 208250 monthly_revenue "last quarter"
```

**What You'll Get:**
- ✅ Result in context
- ✅ Comparison to previous period
- ✅ Percentage change and direction
- ✅ Statistical significance
- ✅ Interpretation (what it means)
- ✅ Recommended actions

**When to Use:**
- Understanding surprising numbers
- Presenting to stakeholders
- Making data-driven decisions
- Investigating trends

---

### 🔄 METRIC COMPARISON

#### `compare`
Compare two metrics side-by-side.

**Syntax:**
```
compare <metric1> <metric2> [time_period]
```

**Examples:**
```
insights> compare total_subscribers monthly_revenue "last 30 days"
insights> compare engagement_rate churn_rate "this year"
insights> compare new_subscribers premium_adoption_rate "Q4"
```

**What You'll Get:**
- ✅ Both values side-by-side
- ✅ Metric definitions
- ✅ Data sources
- ✅ Relationship insights
- ✅ Correlation analysis

**Best Metric Pairs:**
- Engagement + Churn (inverse relationship)
- Subscribers + Revenue (growth alignment)
- New Signups + Churn (net growth)
- Watch Time + Completion Rate (content quality)

---

### 🎯 DATA QUALITY

#### `quality` (or `check`)
Assess data quality for a metric.

**Syntax:**
```
quality <metric> [time_period]
```

**Examples:**
```
insights> quality total_subscribers "last 7 days"
insights> quality monthly_revenue "this month"
insights> quality churn_rate "last quarter"
```

**What Gets Checked:**
- ✅ **Freshness** - When data was last updated
- ✅ **Completeness** - Any missing dates/gaps
- ✅ **Anomalies** - Unusual spikes or drops
- ✅ **Quality Score** - Overall rating (0-100)

**Quality Indicators:**
- ✓ Green - Good quality, proceed with confidence
- ⚠️ Yellow - Some issues, review before using
- ✗ Red - Significant problems, investigate first

**When to Use:**
- Before important presentations
- Monthly data health checks
- After pipeline changes
- When numbers look unusual

---

### 💾 QUERY TEMPLATES

#### `save_template`
Save queries for reuse.

**Syntax:**
```
save_template "<name>" "<sql_query>" "<description>"
```

**Examples:**
```
insights> save_template "Weekly Users" "SELECT COUNT(*) FROM users" "Weekly active users"
insights> save_template "Monthly Revenue" "SELECT SUM(amount) FROM revenue" "MRR report"
```

**Best Practices:**
- Use descriptive names
- Include purpose in description
- Save frequently-run queries
- Version control templates

---

#### `templates`
List all saved templates.

**Syntax:**
```
templates
```

**Example:**
```
insights> templates

Saved Query Templates (3)
==================================================

Name: Weekly Active Users
Description: Weekly subscriber count
Created: today
Times Run: 0
```

---

### 🔍 FOLLOW-UP SUGGESTIONS

#### `followups`
Get intelligent follow-up question suggestions.

**Syntax:**
```
followups <question>
```

**Examples:**
```
insights> followups How many active users last week?
insights> followups What's our revenue?
```

**What You'll Get:**
- ✅ Drill-down questions
- ✅ Related analysis ideas
- ✅ Comparative queries
- ✅ Trend analysis suggestions

---

## Utility Commands

### 📋 METRICS CATALOG

#### `metrics`
List all available metrics.

**Syntax:**
```
metrics
```

**Output:**
```
📊 Available Metrics:
============================================================

Total Subscribers (total_subscribers)
  Description: Total number of active subscribers
  Unit: subscribers
  Table: analytics.subscriptions

Monthly Recurring Revenue (monthly_revenue)
  Description: Total monthly recurring revenue
  Unit: dollars
  Table: analytics.revenue

[... continues for all 11 metrics ...]
```

**When to Use:**
- Starting a new analysis
- Learning what data is available
- Finding the right metric name
- Understanding metric definitions

---

### 📜 HISTORY

#### `history`
View recent query history.

**Syntax:**
```
history [limit]
```

**Examples:**
```
insights> history          # Shows last 10 queries
insights> history 5        # Shows last 5 queries
insights> history 20       # Shows last 20 queries
```

**What You'll See:**
- Question asked
- Time period used
- Result value
- Timestamp

**Use Cases:**
- Review previous analyses
- Track your work
- Find queries to save as templates
- Audit trail

---

### ⏱️ SET TIME PERIOD

#### `set_period`
Set default time period for all queries.

**Syntax:**
```
set_period <time_period>
```

**Examples:**
```
insights> set_period "last 30 days"
insights> set_period "this month"
insights> set_period "Q4 2025"
```

**Time Period Formats:**
- "last N days" - e.g., "last 7 days", "last 90 days"
- "last N weeks" - e.g., "last 2 weeks"
- "this month" - Current calendar month
- "last month" - Previous calendar month
- "this year" - Current year
- "Q1", "Q2", "Q3", "Q4" - Quarters

**Tip:** Set this once at session start to avoid repeating it

---

### 📖 EXAMPLES

#### `examples`
Show usage examples.

**Syntax:**
```
examples
```

Shows a comprehensive list of example commands for every feature.

---

### ❓ HELP

#### `help`
Show all commands or get help on a specific command.

**Syntax:**
```
help              # Show all commands
help <command>    # Help for specific command
```

**Examples:**
```
insights> help
insights> help ask
insights> help generate
```

---

### 🚪 EXIT

#### `exit` (or `quit`)
Exit the CLI.

**Syntax:**
```
exit
quit
```

**Keyboard Shortcut:** Ctrl+D (Unix) or Ctrl+Z (Windows)

---

## Common Workflows

### 🔍 Workflow 1: Exploratory Analysis

```
1. insights> metrics                        # See what's available
2. insights> ask How many subscribers?      # Get baseline
3. insights> quality total_subscribers      # Check data quality
4. insights> followups [your question]      # Get ideas
5. insights> compare [metric1] [metric2]    # Deep dive
```

### 📊 Workflow 2: Building a Report

```
1. insights> set_period "last 30 days"      # Set timeframe
2. insights> generate total_subscribers     # Get queries
3. insights> generate monthly_revenue
4. insights> validate [your SQL]            # Check queries
5. insights> save_template "Monthly Report" # Save for reuse
```

### 🐛 Workflow 3: Investigating an Issue

```
1. insights> ask What's our churn rate?     # Get the number
2. insights> explain [result] churn_rate    # Understand it
3. insights> compare churn engagement       # Find correlations
4. insights> quality churn_rate             # Check data issues
5. insights> followups Why is churn high?   # Next steps
```

### 📈 Workflow 4: Monthly Business Review

```
1. insights> ask How many total subscribers?
2. insights> ask What's our MRR?
3. insights> ask What's the churn rate?
4. insights> compare subscribers revenue
5. insights> templates                      # Run saved reports
```

---

## Tips & Tricks

### 💡 Pro Tips

1. **Use shortcuts**
   - `q` instead of `ask`
   - Tab completion for commands
   - Up arrow for command history

2. **Chain your analysis**
   - Start broad, then drill down
   - Use followups to guide exploration
   - Save good queries as templates

3. **Check data quality first**
   - Always run `quality` for critical decisions
   - Check after pipeline changes
   - Include in monthly reviews

4. **Leverage templates**
   - Save weekly/monthly reports
   - Build a template library
   - Share templates with team

5. **Use time periods effectively**
   - Set default period at session start
   - Compare periods: "this month" vs "last month"
   - Use quarters for trend analysis

### ⚠️ Common Mistakes to Avoid

1. ❌ **Don't skip data quality checks**
   - Always validate before big presentations
   
2. ❌ **Don't use vague questions**
   - Bad: "show me users"
   - Good: "How many active users last week?"

3. ❌ **Don't forget quotes in filters**
   - Bad: `generate revenue last 30 days country=USA`
   - Good: `generate revenue "last 30 days" "country='USA'"`

4. ❌ **Don't run SELECT * queries**
   - Validate will warn you about performance

5. ❌ **Don't ignore warnings**
   - Validation warnings prevent future problems

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Up Arrow | Previous command |
| Down Arrow | Next command |
| Tab | Command completion |
| Ctrl+C | Cancel current input |
| Ctrl+D | Exit (Unix/Mac) |
| Ctrl+Z | Exit (Windows) |

---

## Error Messages & Solutions

### "Metric not found"
**Problem:** Typed wrong metric name  
**Solution:** Run `metrics` to see available options

### "Unable to parse question"
**Problem:** Question too vague or no recognizable metrics  
**Solution:** Use metric names from catalog, be more specific

### "Query validation failed"
**Problem:** SQL syntax error  
**Solution:** Check the validation output, fix issues listed

### "Could not parse result value"
**Problem:** Invalid number format in explain command  
**Solution:** Use just the number, no commas or units

---

## Getting Started Checklist

- [ ] Start CLI: `python -m insights_agent.cli`
- [ ] View available metrics: `metrics`
- [ ] Set time period: `set_period "last 30 days"`
- [ ] Ask first question: `ask How many subscribers?`
- [ ] Check data quality: `quality total_subscribers`
- [ ] Compare two metrics: `compare [metric1] [metric2]`
- [ ] Save a template: `save_template "name" "query" "desc"`
- [ ] View history: `history`
- [ ] Read examples: `examples`

---

## Next Steps

Once comfortable with CLI:
1. **Connect to Claude Desktop** - Use agent via conversation
2. **Build Python scripts** - Automate analysis
3. **Create dashboards** - Export queries to BI tools
4. **Schedule reports** - Use templates for recurring analysis

---

**Need more help?** Type `help <command>` in the CLI for command-specific details!
