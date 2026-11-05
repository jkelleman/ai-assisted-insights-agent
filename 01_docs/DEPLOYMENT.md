#  Deployment Guide

##  Production Ready

All 43 tests passing, MCP server runs successfully.

## Quick Deploy to Claude Desktop

### 1. Add to Claude Desktop Config

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ai-insights-agent": {
      "command": "python",
      "args": [
        "-m",
        "insights_agent.server"
      ],
      "cwd": "/path/to/ai-assisted-insights-agent",
      "env": {
        "CONFIG_PATH": "config.yaml"
      }
    }
  }
}
```

### 2. Restart Claude Desktop

### 3. Test

Ask Claude: "What metrics are available?" or "Show me active users for last week"

## 9 Available MCP Tools

1. **ask_question()** - Natural language  SQL + results + insights
2. **generate_query()** - Create SQL from metric descriptions  
3. **validate_query()** - Check SQL syntax and performance
4. **explain_result()** - Interpret query output with context
5. **compare_metrics()** - Side-by-side metric comparison
6. **check_data_quality()** - Freshness and completeness checks
7. **list_available_metrics()** - Browse all configured metrics
8. **search_metrics()** - Find metrics by keyword
9. **get_metric_definition()** - Detailed metric specifications

## Configuration

Edit `config.yaml` to customize:
- Data sources (SQLite, PostgreSQL, MySQL, BigQuery, etc.)
- Business glossary (map terms like "revenue" to tables)
- Metric definitions
- Quality thresholds

## Testing

```bash
# Run all tests
pytest tests/ -v

# Test specific functionality
pytest tests/test_tools.py -v
pytest tests/test_server.py -v
```

## Status:  READY FOR PRODUCTION
