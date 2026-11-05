<p align="center"><img src="assets/banner.png" alt="Every answer shows its work: an MCP agent that turns plain-language data questions into SQL from trusted metric definitions. An example card shows the question 'How many active users did we have last week?', the generated SQL, and the metric and filter used." width="100%"></p>

# AI-Assisted Insights Agent

<p>
  <a href="https://github.com/jkelleman/ai-assisted-insights-agent/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/jkelleman/ai-assisted-insights-agent/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-0F1B2D?logo=python&logoColor=white">
  <a href="https://modelcontextprotocol.io/"><img alt="MCP SDK 1.x" src="https://img.shields.io/badge/MCP%20SDK-1.x-0F8B7E"></a>
  <img alt="9 MCP tools" src="https://img.shields.io/badge/MCP%20tools-9-0F8B7E">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-0F1B2D"></a>
</p>

**An MCP agent that turns plain-language data questions into SQL from trusted metric definitions, and shows its work on every answer.**

Ask "How many active users did we have last week?" and the agent answers with the number, the exact SQL it ran, the metric definition behind it, the filters it assumed, and the questions worth asking next. It's built for stakeholders who need answers without writing SQL, and for analysts who need to trust those answers.

> [!NOTE]
> **Status: reference implementation.** Question parsing, SQL generation, query validation, templates, and history work today. Query execution and data-quality checks are **simulated**, and every answer says so. Connecting a real warehouse is next on the [roadmap](#roadmap).

## Contents

- [The problem](#the-problem)
- [What an answer looks like](#what-an-answer-looks-like)
- [MCP tools and resources](#mcp-tools-and-resources)
- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [Design principles](#design-principles)
- [Project layout](#project-layout)
- [Roadmap](#roadmap)
- [About](#about)

## The problem

| Who | What goes wrong today |
|---|---|
| **Stakeholders** | They ask "why did revenue drop?" and wait days. When the answer arrives, they can't check how it was calculated. |
| **Analysts** | They rewrite the same queries for routine questions and become the bottleneck. |
| **Everyone** | "Active customers" means different things to different teams, so two dashboards disagree. |

This agent maps business language to one set of trusted metric definitions, then shows the work behind every number, so an answer can be checked instead of taken on faith.

## What an answer looks like

This is real output from `ask_question`. The number comes from the simulated execution layer.

```text
Question: How many active users did we have last week?
Time Period: last 7 days

Answer: 1,896 users
Note: Values are simulated until a data source is connected.

Query Used:
SELECT COUNT(DISTINCT user_id)
FROM analytics.user_events
WHERE event_type = 'login' AND event_date >= CURRENT_DATE - INTERVAL '7 days'

Explanation:
Metric logic: Unique users who logged in at least once in the time period, from the analytics.user_events table.
Filtered by: event_type = 'login'

Data Quality: (simulated checks)
✓ Data is fresh (updated 2 hours ago)
✓ No missing days in date range
✓ Volume within expected range (within 2σ of baseline)

Metric Definition:
• Name: Active Users
• Description: Unique users who logged in at least once in the time period
• Source: analytics.user_events

Suggested Follow-ups:
• What was active users for the previous period?
• Show me active users broken down by day
• Compare active users to the same period last year
• What's the conversion rate for these users?
```

If a question doesn't match a known metric, the agent doesn't guess. It lists the metrics it knows and suggests how to rephrase.

## MCP tools and resources

| Tool | What it does |
|---|---|
| `ask_question` | Answers a plain-language question with the SQL, metric definition, and follow-ups |
| `generate_query` | Builds SQL for a named metric, time period, filters, and grouping |
| `validate_query` | Checks SQL for structural and performance problems before it runs |
| `explain_result` | Puts a number in context against a baseline and flags notable changes |
| `suggest_followups` | Suggests drill-down and related questions |
| `check_data_quality` | Scores freshness, completeness, and anomalies *(simulated)* |
| `compare_metrics` | Compares two metrics side by side with their definitions |
| `save_query_template` | Saves a query so it can be rerun later |
| `list_templates` | Lists saved templates |

**Resources:** `metrics://catalog`, `metrics://metric/{id}`, `history://recent`, `templates://list`
**Prompt:** `insights_query_guide`, a short guide to asking good data questions

Full reference: [01_docs/API.md](01_docs/API.md)

## Quick start

**Requirements:** Python 3.10+

```bash
git clone https://github.com/jkelleman/ai-assisted-insights-agent.git
cd ai-assisted-insights-agent
pip install -e .
pytest            # 43 tests
```

### Use it in Claude Desktop

Add the server to `claude_desktop_config.json`. On macOS it's in `~/Library/Application Support/Claude/`, and on Windows it's in `%APPDATA%\Claude\`.

```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python",
      "args": ["-m", "insights_agent.server"],
      "cwd": "/path/to/ai-assisted-insights-agent"
    }
  }
}
```

Restart Claude Desktop and ask a data question. Step-by-step setup: [01_docs/CLAUDE_DESKTOP_SETUP.md](01_docs/CLAUDE_DESKTOP_SETUP.md)

### Or use the interactive CLI

```text
python -m insights_agent.cli

insights> ask How many active users did we have last week?
insights> generate revenue "last 30 days"
insights> compare active_users revenue "last month"
insights> help
```

CLI reference: [01_docs/CLI_REFERENCE.md](01_docs/CLI_REFERENCE.md)

## How it works

```mermaid
flowchart LR
    Q["Plain-language question"] --> G["Normalize terms<br/>with the business glossary"]
    G --> M["Match a metric<br/>in the catalog"]
    M --> S["Build SQL from the<br/>metric's template, filter,<br/>and time period"]
    S --> E["Execute<br/><i>(simulated today)</i>"]
    E --> A["Answer with SQL, definition,<br/>assumptions, and follow-ups"]
    S --> H[("History and<br/>templates")]
```

1. **Normalize.** The business glossary maps everyday words to metric terms. For example, "customers" becomes "users" and "sales" becomes "revenue."
2. **Match.** The question is matched against the metric catalog: active users, revenue, conversion rate, and signups.
3. **Generate.** SQL comes from the metric's own template and filter, never improvised, so the same question always gets the same logic.
4. **Explain.** Every answer carries the query, the definition, the filters it assumed, and suggested next questions.

Design detail: [01_docs/ARCHITECTURE.md](01_docs/ARCHITECTURE.md)

## Design principles

1. **No number without its query.** Showing how a result was calculated is what makes it trustworthy.
2. **Definitions over improvisation.** SQL comes from approved metric definitions, so two people asking the same question get the same answer.
3. **Don't guess.** When a question doesn't match a metric, the agent says so and offers options.
4. **Progressive disclosure.** The answer comes first, then the detail for anyone who wants to check it.
5. **Honest about limits.** Simulated values and checks are labeled as simulated, every time.

## Project layout

```text
insights_agent/   MCP server, CLI, config loader, and SQLite query history
05_tests/         43 tests covering parsing, SQL generation, validation, and every tool
01_docs/          API, architecture, CLI, Claude Desktop setup, data connections, demo walkthrough
02_examples/      Python client, Claude Desktop, Jupyter, and streaming-data examples
03_data/          Sample data for demos
06_configs/       Example configurations
```

## Roadmap

- [ ] Load metric definitions and the glossary from `config.yaml` instead of the built-in catalog
- [ ] Run generated SQL against a real database, starting with SQLite and the bundled sample data
- [ ] Replace simulated data-quality checks with real freshness and completeness queries
- [ ] Parse and validate SQL with a real parser instead of pattern checks
- [ ] Add LLM-based question parsing for phrasings the rule-based matcher misses

Planned connection setup: [01_docs/CONNECTING_TO_DATA.md](01_docs/CONNECTING_TO_DATA.md)

## About

Built by **Jen Kelleman**, a content designer for AI and data experiences. I design how AI systems explain themselves, so people can see why an answer is right before they act on it.

- [LinkedIn](https://linkedin.com/in/jenniferkelleman) · [Portfolio](https://aiwithjen.com) · [AI Content Design Handbook](https://jkelleman.github.io/ai-content-design-handbook/)

**Related projects**
- [Semantic Metrics Modeling Assistant](https://github.com/jkelleman/semantic-metrics-modeling-assistant): an MCP agent for metric governance and trust
- [Airbnb LLM-as-a-Judge Listing Evals](https://github.com/jkelleman/airbnb-llm-as-a-judge-listing-evals): calibrated virtual judges for AI listing highlights
- [AI Content Design Handbook](https://github.com/jkelleman/ai-content-design-handbook): a guide to UX writing for AI systems

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
