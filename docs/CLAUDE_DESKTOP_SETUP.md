# Connect AI-Assisted Insights Agent to Claude Desktop

Complete guide to integrate your insights agent with Claude Desktop via MCP.

---

## Prerequisites

Before starting, ensure you have:

- ✅ Claude Desktop installed ([Download here](https://claude.ai/download))
- ✅ Python 3.10+ installed
- ✅ AI-Assisted Insights Agent repository cloned/downloaded
- ✅ Agent dependencies installed (`pip install -e .`)

---

## Step 1: Verify Agent Installation

First, test that the agent works:

```bash
# Navigate to your project directory
cd /path/to/ai-assisted-insights-agent

# Test the server starts
python -m insights_agent.server
```

You should see:
```
Starting AI-Assisted Insights Agent...
Ready to translate natural language questions into data insights
```

Press `Ctrl+C` to stop the server.

**If you see errors:**
- Check Python version: `python --version` (needs 3.10+)
- Install dependencies: `pip install -e .`
- Check for typos in file paths

---

## Step 2: Locate Claude Desktop Config File

Find your Claude Desktop configuration file location:

### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Full path usually:**
```
C:\Users\YourUsername\AppData\Roaming\Claude\claude_desktop_config.json
```

**To open quickly:**
1. Press `Win + R`
2. Type: `%APPDATA%\Claude`
3. Look for `claude_desktop_config.json`

### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**To open in Finder:**
1. Open Finder
2. Press `Cmd + Shift + G`
3. Paste: `~/Library/Application Support/Claude`
4. Look for `claude_desktop_config.json`

### Linux
```
~/.config/Claude/claude_desktop_config.json
```

**If file doesn't exist:** Create it in the location above.

---

## Step 3: Configure MCP Server

Edit `claude_desktop_config.json` with your preferred text editor.

### Option A: Basic Configuration (Recommended)

```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python",
      "args": [
        "-m",
        "insights_agent.server"
      ],
      "cwd": "C:\\Users\\YourUsername\\ai-assisted-insights-agent"
    }
  }
}
```

**Important:** Replace `C:\\Users\\YourUsername\\ai-assisted-insights-agent` with your actual path.

### Option B: Streaming Services Configuration

To use the streaming dataset by default:

```json
{
  "mcpServers": {
    "insights-agent-streaming": {
      "command": "python",
      "args": [
        "-m",
        "insights_agent.server"
      ],
      "cwd": "C:\\Users\\YourUsername\\ai-assisted-insights-agent",
      "env": {
        "CONFIG_PATH": "config_streaming.yaml"
      }
    }
  }
}
```

### Option C: Multiple Configurations

Run both regular and streaming versions:

```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python",
      "args": ["-m", "insights_agent.server"],
      "cwd": "C:\\Users\\YourUsername\\ai-assisted-insights-agent"
    },
    "insights-agent-streaming": {
      "command": "python",
      "args": ["-m", "insights_agent.server"],
      "cwd": "C:\\Users\\YourUsername\\ai-assisted-insights-agent",
      "env": {
        "CONFIG_PATH": "config_streaming.yaml"
      }
    }
  }
}
```

---

## Step 4: Platform-Specific Path Formats

### Windows Paths

**Use double backslashes:**
```json
"cwd": "C:\\Users\\jenkelleman\\ai-assisted-insights-agent"
```

**Or forward slashes:**
```json
"cwd": "C:/Users/jenkelleman/ai-assisted-insights-agent"
```

### macOS/Linux Paths

**Use forward slashes:**
```json
"cwd": "/Users/jenkelleman/ai-assisted-insights-agent"
```

**With home directory shortcut:**
```json
"cwd": "~/ai-assisted-insights-agent"
```

---

## Step 5: Complete Configuration Example

Here's a full working configuration for **Windows**:

```json
{
  "mcpServers": {
    "insights-agent-streaming": {
      "command": "python",
      "args": [
        "-m",
        "insights_agent.server"
      ],
      "cwd": "C:\\Users\\jenkelleman\\ai-assisted-insights-agent",
      "env": {
        "CONFIG_PATH": "config_streaming.yaml",
        "PYTHONPATH": "C:\\Users\\jenkelleman\\ai-assisted-insights-agent"
      }
    }
  }
}
```

**For macOS:**

```json
{
  "mcpServers": {
    "insights-agent-streaming": {
      "command": "python3",
      "args": [
        "-m",
        "insights_agent.server"
      ],
      "cwd": "/Users/jenkelleman/ai-assisted-insights-agent",
      "env": {
        "CONFIG_PATH": "config_streaming.yaml",
        "PYTHONPATH": "/Users/jenkelleman/ai-assisted-insights-agent"
      }
    }
  }
}
```

---

## Step 6: Restart Claude Desktop

1. **Completely quit Claude Desktop** (don't just close the window)
   - Windows: Right-click system tray icon → Quit
   - macOS: Cmd+Q
   - Or use Task Manager/Activity Monitor to force quit

2. **Reopen Claude Desktop**

3. **Wait 5-10 seconds** for MCP servers to initialize

---

## Step 7: Verify Connection

Start a new conversation in Claude and check:

### Method 1: Look for the Tool Icon

In the chat interface, you should see a small **tools icon** (🔧) indicating MCP tools are available.

### Method 2: Ask Claude Directly

```
You: What MCP tools do you have available?
```

Claude should list the insights agent tools:
- ask_question
- generate_query
- validate_query
- explain_result
- suggest_followups
- save_query_template
- list_templates
- check_data_quality
- compare_metrics

### Method 3: Check Resources

```
You: Can you show me the metrics catalog?
```

Claude should be able to access `metrics://catalog` resource.

---

## Step 8: Test with Questions

Try these questions to test functionality:

### Basic Question
```
You: Can you use the insights agent to check how many total subscribers we have?
```

**Expected:** Claude calls `ask_question` tool and returns the answer with SQL.

### Generate Query
```
You: Generate a SQL query for monthly revenue for the last 30 days.
```

**Expected:** Claude calls `generate_query` tool.

### Compare Metrics
```
You: Compare engagement rate and churn rate for the streaming service.
```

**Expected:** Claude calls `compare_metrics` tool.

### Check Data Quality
```
You: Check the data quality for our subscriber metrics.
```

**Expected:** Claude calls `check_data_quality` tool.

---

## Troubleshooting

### Issue 1: Tools Not Showing Up

**Symptoms:** Claude doesn't mention or use the insights agent tools.

**Solutions:**
1. ✅ Verify config file location is correct
2. ✅ Check JSON syntax (use [JSONLint](https://jsonlint.com/))
3. ✅ Ensure no trailing commas in JSON
4. ✅ Completely quit and restart Claude Desktop
5. ✅ Check Claude Desktop logs

**View Logs:**
- Windows: `%APPDATA%\Claude\logs`
- macOS: `~/Library/Logs/Claude`
- Linux: `~/.config/Claude/logs`

### Issue 2: Python Not Found

**Error in logs:** `Python was not found`

**Solutions:**
1. Install Python 3.10+ from [python.org](https://python.org)
2. Or use full Python path:
   ```json
   "command": "C:\\Python310\\python.exe"
   ```
3. Or use `python3` instead of `python`:
   ```json
   "command": "python3"
   ```

### Issue 3: Module Not Found

**Error in logs:** `ModuleNotFoundError: No module named 'insights_agent'`

**Solutions:**
1. Install the package:
   ```bash
   cd /path/to/ai-assisted-insights-agent
   pip install -e .
   ```
2. Set PYTHONPATH in config:
   ```json
   "env": {
     "PYTHONPATH": "C:\\path\\to\\ai-assisted-insights-agent"
   }
   ```

### Issue 4: Config File Not Loading

**Error in logs:** `Config file not found`

**Solutions:**
1. Check `config_streaming.yaml` exists in project root
2. Use absolute path:
   ```json
   "env": {
     "CONFIG_PATH": "C:\\full\\path\\to\\config_streaming.yaml"
   }
   ```
3. Or remove CONFIG_PATH to use defaults

### Issue 5: Permission Denied

**Error in logs:** `Permission denied`

**Solutions:**
1. Run Claude Desktop as administrator (Windows)
2. Check file permissions:
   ```bash
   chmod +x insights_agent/server.py
   ```
3. Move project to non-protected folder

---

## Advanced Configuration

### Use Virtual Environment

If using a Python virtual environment:

```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "C:\\path\\to\\venv\\Scripts\\python.exe",
      "args": ["-m", "insights_agent.server"],
      "cwd": "C:\\path\\to\\ai-assisted-insights-agent"
    }
  }
}
```

### Debug Mode

Enable verbose logging:

```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python",
      "args": ["-m", "insights_agent.server"],
      "cwd": "C:\\path\\to\\ai-assisted-insights-agent",
      "env": {
        "DEBUG": "true",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### Custom Port

If you need a specific port:

```json
{
  "mcpServers": {
    "insights-agent": {
      "command": "python",
      "args": ["-m", "insights_agent.server", "--port", "3000"],
      "cwd": "C:\\path\\to\\ai-assisted-insights-agent"
    }
  }
}
```

---

## Usage Examples in Claude

Once connected, you can have natural conversations:

### Example 1: Quick Metrics Check

```
You: What are our key streaming metrics for this month?

Claude: I'll check the streaming service metrics for you.
[Calls ask_question tool multiple times]

Here's what I found:
- Total Subscribers: 1,450 active users
- Monthly Recurring Revenue: $215,300
- Churn Rate: 15.2%
- Engagement Rate: 68.5%
- ARPU: $148.48

The business looks healthy with strong engagement offsetting the churn rate.
```

### Example 2: Deep Dive Analysis

```
You: I'm concerned about our churn rate. Can you investigate?

Claude: Let me analyze the churn rate for you.
[Calls check_data_quality on churn_rate]
[Calls explain_result with the churn data]
[Calls compare_metrics for churn_rate vs engagement_rate]

The data quality is good, and I found something interesting:
- Current churn: 15.2% (within industry norms)
- Strong negative correlation with engagement (-0.72)
- Users who watch more content are much less likely to churn

Recommendation: Focus on engagement initiatives to reduce churn.
```

### Example 3: Building Reports

```
You: I need SQL queries for a weekly executive dashboard showing subscribers, revenue, and churn.

Claude: I'll generate those queries for you.
[Calls generate_query for each metric]

Here are your dashboard queries:

1. Weekly Subscribers:
SELECT COUNT(DISTINCT user_id)...

2. Weekly Revenue:
SELECT SUM(amount)...

3. Weekly Churn Rate:
SELECT COUNT(DISTINCT user_id) * 100.0...

Would you like me to save these as templates for future use?
```

### Example 4: Data Quality Monitoring

```
You: Before my board meeting, can you verify our data is reliable?

Claude: I'll check data quality across all key metrics.
[Calls check_data_quality on multiple metrics]

Data Quality Report:
✅ Subscribers: Fresh (2 hrs ago), Complete, No anomalies - Score: 100/100
✅ Revenue: Fresh (2 hrs ago), Complete, No anomalies - Score: 100/100
✅ Churn: Fresh (2 hrs ago), Complete, No anomalies - Score: 100/100

All metrics are excellent quality. You're good to go for your meeting!
```

---

## Best Practices

### 1. Start Conversations Explicitly

❌ **Don't:**
```
You: What's the churn rate?
```
(Claude might not know to use the tool)

✅ **Do:**
```
You: Use the insights agent to check our churn rate.
You: Can you query the streaming metrics for churn rate?
```

### 2. Be Specific About Time Periods

✅ **Good:**
```
You: What were total subscribers last month?
You: Compare Q3 and Q4 revenue.
```

### 3. Ask for Explanations

✅ **Good:**
```
You: The churn rate is 15.2% - what does that mean in context?
You: Explain this revenue number and whether we should be concerned.
```

### 4. Leverage Follow-ups

✅ **Good:**
```
You: What's our engagement rate?
Claude: [Returns 68.5%]
You: What are good follow-up questions to explore this further?
```

### 5. Check Data Quality for Critical Decisions

✅ **Always:**
```
You: Before we present to the board, verify all our metrics are reliable.
```

---

## Testing Checklist

After setup, verify these work:

- [ ] Claude recognizes insights agent tools
- [ ] `ask_question` returns results with SQL
- [ ] `generate_query` creates valid SQL
- [ ] `validate_query` checks SQL syntax
- [ ] `explain_result` adds context
- [ ] `compare_metrics` shows relationships
- [ ] `check_data_quality` runs successfully
- [ ] Resources (`metrics://catalog`) are accessible
- [ ] Streaming metrics work (if using streaming config)
- [ ] Claude can have multi-turn conversations about data

---

## Next Steps

Once connected successfully:

1. **Explore the streaming dataset** - Ask questions about 2025 streaming services
2. **Build analysis workflows** - Use Claude to guide your analysis
3. **Create custom metrics** - Add your own metrics to config.yaml
4. **Save useful queries** - Build a template library
5. **Connect real data** - Replace simulated data with your warehouse

---

## Getting Help

**Issues with Claude Desktop:**
- [Claude Desktop Documentation](https://claude.ai/docs)
- [MCP Documentation](https://modelcontextprotocol.io)

**Issues with the Agent:**
- Check logs in `~/.config/Claude/logs` (or Windows equivalent)
- Test server directly: `python -m insights_agent.server`
- Verify installation: `pip list | grep mcp`
- Review [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)

**Common Log Files:**
- `%APPDATA%\Claude\logs\mcp-server-insights-agent.log` (Windows)
- `~/Library/Logs/Claude/mcp-server-insights-agent.log` (macOS)

---

## Success!

You should now be able to:

✅ Ask Claude natural language questions about your streaming data  
✅ Generate SQL queries for dashboards  
✅ Check data quality before presentations  
✅ Compare metrics to find insights  
✅ Build reproducible analysis workflows  
✅ Save queries as reusable templates  

**Ready to analyze streaming services data through conversation with Claude!** 🎉

---

*Last updated: January 3, 2026*
