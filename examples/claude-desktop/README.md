# Claude Desktop Integration

Integrate the AI-Assisted Insights Agent with Claude Desktop via MCP.

## Setup

1. Install the agent:
```bash
cd /path/to/ai-assisted-insights-agent
pip install -e .
```

2. Configure Claude Desktop to use the agent:

### Windows

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python",
      "args": [
        "-m",
        "insights_agent.server"
      ],
      "cwd": "C:\\path\\to\\ai-assisted-insights-agent"
    }
  }
}
```

### macOS

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python3",
      "args": [
        "-m",
        "insights_agent.server"
      ],
      "cwd": "/path/to/ai-assisted-insights-agent"
    }
  }
}
```

### Linux

Edit `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python3",
      "args": [
        "-m",
        "insights_agent.server"
      ],
      "cwd": "/path/to/ai-assisted-insights-agent"
    }
  }
}
```

## Usage

1. Restart Claude Desktop
2. Start a new conversation
3. Ask data questions naturally:

```
You: Can you check how many active users we had last week?

Claude: I'll use the insights agent to check that for you.
[Uses ask_question tool]

The data shows you had 12,470 active users last week. The query was:
SELECT COUNT(DISTINCT user_id)
FROM analytics.user_events
WHERE event_type = 'login'
  AND event_date >= CURRENT_DATE - INTERVAL '7 days'

Data quality is excellent - the data is fresh and complete.
```

## Example Conversations

### Revenue Analysis
```
You: What was our revenue last month and how does it compare to the previous month?

Claude: [Uses compare_metrics tool and explain_result]
```

### Data Quality Check
```
You: Before I make a decision, can you check the data quality for our conversion rate metric?

Claude: [Uses check_data_quality tool]
```

### Query Generation
```
You: I need a SQL query for active users grouped by day for the last 30 days.

Claude: [Uses generate_query tool]
```

## Tips

- Ask follow-up questions naturally
- Request explanations for any numbers
- Have Claude validate queries before using them
- Ask about data quality for important decisions
