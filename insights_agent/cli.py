#!/usr/bin/env python3
"""
Interactive CLI for the AI-Assisted Insights Agent.

Provides a command-line interface for testing and interacting with the agent
without requiring an MCP client.
"""
import sys
import cmd
import json
from typing import Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from insights_agent.server import (
    ask_question,
    generate_query,
    validate_query,
    explain_result,
    suggest_followups,
    save_query_template,
    list_templates,
    check_data_quality,
    compare_metrics,
    METRIC_DEFINITIONS,
    QUERY_HISTORY
)


class InsightsAgentCLI(cmd.Cmd):
    """Interactive command-line interface for the Insights Agent."""
    
    intro = """
╔════════════════════════════════════════════════════════════════╗
║      AI-Assisted Insights Agent - Interactive CLI             ║
║                                                                ║
║  Ask data questions in natural language and get explainable   ║
║  answers with SQL queries and data quality context.           ║
╚════════════════════════════════════════════════════════════════╝

Type 'help' or '?' for available commands.
Type 'examples' to see usage examples.
Type 'quit' or 'exit' to exit.
"""
    
    prompt = "insights> "
    
    def __init__(self):
        super().__init__()
        self.last_result = None
        self.last_metric = None
        self.last_time_period = "last 7 days"
    
    # Question Commands
    
    def do_ask(self, arg):
        """
        Ask a data question in natural language.
        
        Usage: ask <question>
        Example: ask How many active users did we have last week?
        """
        if not arg:
            print("❌ Please provide a question.")
            print("Example: ask How many active users last week?")
            return
        
        result = ask_question(arg, self.last_time_period)
        print(result)
        
        # Extract result value for explain command
        if "Answer:" in result:
            try:
                answer_line = [line for line in result.split('\n') if line.startswith('Answer:')][0]
                self.last_result = answer_line.split()[1].replace(',', '')
            except:
                pass
    
    def do_question(self, arg):
        """Alias for 'ask' command."""
        self.do_ask(arg)
    
    def do_q(self, arg):
        """Shortcut for 'ask' command."""
        self.do_ask(arg)
    
    # Query Generation Commands
    
    def do_generate(self, arg):
        """
        Generate a SQL query for a specific metric.
        
        Usage: generate <metric> [time_period] [filters] [group_by]
        Example: generate active_users "last 30 days"
        Example: generate revenue "this month" "country='US'" date
        """
        parts = arg.split(maxsplit=3)
        if not parts:
            print("❌ Please provide a metric name.")
            print("Available metrics:", ", ".join(METRIC_DEFINITIONS.keys()))
            return
        
        metric = parts[0]
        time_period = parts[1].strip('"') if len(parts) > 1 else self.last_time_period
        filters = parts[2].strip('"') if len(parts) > 2 else ""
        group_by = parts[3].strip('"') if len(parts) > 3 else ""
        
        result = generate_query(metric, time_period, filters, group_by)
        print(result)
    
    def do_validate(self, arg):
        """
        Validate a SQL query.
        
        Usage: validate <sql_query>
        Example: validate SELECT COUNT(*) FROM users WHERE date >= '2025-01-01'
        """
        if not arg:
            print("❌ Please provide a SQL query to validate.")
            return
        
        result = validate_query(arg)
        print(result)
    
    # Analysis Commands
    
    def do_explain(self, arg):
        """
        Explain a query result with context.
        
        Usage: explain <result_value> <metric> [time_period]
        Example: explain 1500 active_users "last 7 days"
        """
        parts = arg.split(maxsplit=2)
        if len(parts) < 2:
            if self.last_result and self.last_metric:
                result = explain_result(self.last_result, self.last_metric, self.last_time_period)
            else:
                print("❌ Usage: explain <result_value> <metric> [time_period]")
                return
        else:
            result_value = parts[0]
            metric = parts[1]
            time_period = parts[2].strip('"') if len(parts) > 2 else self.last_time_period
            result = explain_result(result_value, metric, time_period)
        
        print(result)
    
    def do_compare(self, arg):
        """
        Compare two metrics side-by-side.
        
        Usage: compare <metric1> <metric2> [time_period]
        Example: compare active_users revenue "last 30 days"
        """
        parts = arg.split(maxsplit=2)
        if len(parts) < 2:
            print("❌ Usage: compare <metric1> <metric2> [time_period]")
            return
        
        metric1 = parts[0]
        metric2 = parts[1]
        time_period = parts[2].strip('"') if len(parts) > 2 else self.last_time_period
        
        result = compare_metrics(metric1, metric2, time_period)
        print(result)
    
    def do_quality(self, arg):
        """
        Check data quality for a metric.
        
        Usage: quality <metric> [time_period]
        Example: quality active_users "last 7 days"
        """
        parts = arg.split(maxsplit=1)
        if not parts:
            print("❌ Please provide a metric name.")
            return
        
        metric = parts[0]
        time_period = parts[1].strip('"') if len(parts) > 1 else self.last_time_period
        
        result = check_data_quality(metric, time_period)
        print(result)
    
    def do_followups(self, arg):
        """
        Suggest follow-up questions.
        
        Usage: followups <question>
        Example: followups How many active users last week?
        """
        if not arg:
            print("❌ Please provide a question.")
            return
        
        result = suggest_followups(arg)
        print(result)
    
    # Template Commands
    
    def do_save_template(self, arg):
        """
        Save a query as a reusable template.
        
        Usage: save_template "<name>" "<sql_query>" "<description>"
        Example: save_template "Weekly Users" "SELECT COUNT(*) FROM users" "Weekly active users"
        """
        # Parse quoted arguments
        import shlex
        try:
            parts = shlex.split(arg)
        except ValueError as e:
            print(f"❌ Error parsing arguments: {e}")
            return
        
        if len(parts) < 2:
            print("❌ Usage: save_template \"<name>\" \"<sql_query>\" \"<description>\"")
            return
        
        name = parts[0]
        sql_query = parts[1]
        description = parts[2] if len(parts) > 2 else ""
        
        result = save_query_template(name, sql_query, description)
        print(result)
    
    def do_templates(self, arg):
        """
        List all saved query templates.
        
        Usage: templates
        """
        result = list_templates()
        print(result)
    
    # Utility Commands
    
    def do_metrics(self, arg):
        """
        List all available metrics.
        
        Usage: metrics
        """
        print("\n📊 Available Metrics:\n" + "=" * 60)
        for metric_id, metric in METRIC_DEFINITIONS.items():
            print(f"\n{metric['name']} ({metric_id})")
            print(f"  Description: {metric['description']}")
            print(f"  Unit: {metric['unit']}")
            print(f"  Table: {metric['table']}")
    
    def do_history(self, arg):
        """
        Show query history.
        
        Usage: history [limit]
        Example: history 5
        """
        limit = int(arg) if arg and arg.isdigit() else 10
        
        if not QUERY_HISTORY:
            print("No queries in history.")
            return
        
        print(f"\n📜 Query History (last {limit}):\n" + "=" * 60)
        for i, entry in enumerate(QUERY_HISTORY[-limit:], 1):
            print(f"\n{i}. Question: {entry['question']}")
            print(f"   Time Period: {entry['time_period']}")
            print(f"   Result: {entry['result']}")
            print(f"   Timestamp: {entry['timestamp']}")
    
    def do_set_period(self, arg):
        """
        Set default time period for queries.
        
        Usage: set_period <time_period>
        Example: set_period "last 30 days"
        Example: set_period "this month"
        """
        if not arg:
            print(f"Current time period: {self.last_time_period}")
            return
        
        self.last_time_period = arg.strip('"')
        print(f"✓ Default time period set to: {self.last_time_period}")
    
    def do_examples(self, arg):
        """Show usage examples."""
        print("""
📖 Usage Examples:
════════════════════════════════════════════════════════════════

1. Ask a simple question:
   insights> ask How many active users did we have last week?

2. Generate a query for a specific metric:
   insights> generate active_users "last 30 days"

3. Generate a query with filters:
   insights> generate revenue "this month" "country='US'" date

4. Validate a SQL query:
   insights> validate SELECT COUNT(*) FROM users WHERE date >= '2025-01-01'

5. Explain a result:
   insights> explain 1500 active_users "last 7 days"

6. Compare two metrics:
   insights> compare active_users revenue "last month"

7. Check data quality:
   insights> quality active_users "last 7 days"

8. Save a query template:
   insights> save_template "Weekly Report" "SELECT COUNT(*) FROM users" "Description"

9. List all templates:
   insights> templates

10. View available metrics:
    insights> metrics

11. View query history:
    insights> history

12. Set default time period:
    insights> set_period "last 30 days"
""")
    
    def do_help(self, arg):
        """Show help for commands."""
        if not arg:
            print("""
Available Commands:
══════════════════════════════════════════════════════════════

Questions & Queries:
  ask, question, q    - Ask a data question in natural language
  generate           - Generate a SQL query for a metric
  validate           - Validate a SQL query
  
Analysis:
  explain            - Explain a result with context
  compare            - Compare two metrics
  quality            - Check data quality
  followups          - Suggest follow-up questions
  
Templates:
  save_template      - Save a query as a template
  templates          - List all saved templates
  
Utilities:
  metrics            - List all available metrics
  history            - Show query history
  set_period         - Set default time period
  examples           - Show usage examples
  help               - Show this help message
  quit, exit         - Exit the CLI

Type 'help <command>' for detailed help on a specific command.
""")
        else:
            super().do_help(arg)
    
    def do_exit(self, arg):
        """Exit the CLI."""
        print("\n👋 Thank you for using AI-Assisted Insights Agent!")
        return True
    
    def do_quit(self, arg):
        """Exit the CLI."""
        return self.do_exit(arg)
    
    def do_EOF(self, arg):
        """Handle Ctrl+D to exit."""
        print()
        return self.do_exit(arg)
    
    def emptyline(self):
        """Do nothing on empty line."""
        pass
    
    def default(self, line):
        """Handle unknown commands."""
        print(f"❌ Unknown command: {line}")
        print("Type 'help' for available commands.")


def main():
    """Main entry point for the CLI."""
    try:
        InsightsAgentCLI().cmdloop()
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using AI-Assisted Insights Agent!")
        sys.exit(0)


if __name__ == "__main__":
    main()
