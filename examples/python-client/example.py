"""
Python client example for AI-Assisted Insights Agent.

This example shows how to use the agent directly in a Python application.
"""
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from insights_agent.server import (
    ask_question,
    generate_query,
    validate_query,
    explain_result,
    compare_metrics,
    check_data_quality
)


def example_simple_question():
    """Example: Ask a simple question."""
    print("=" * 70)
    print("Example 1: Simple Question")
    print("=" * 70)
    
    result = ask_question("How many active users did we have last week?")
    print(result)


def example_generate_and_validate():
    """Example: Generate and validate a query."""
    print("\n" + "=" * 70)
    print("Example 2: Generate and Validate Query")
    print("=" * 70)
    
    # Generate query
    query_result = generate_query("revenue", "last 30 days", "country = 'US'", "date")
    print(query_result)
    
    # Extract SQL from result (in practice, you'd parse this properly)
    print("\n--- Validating Query ---\n")
    validation = validate_query(
        "SELECT date, SUM(amount) FROM analytics.transactions "
        "WHERE status = 'completed' AND country = 'US' "
        "AND event_date >= CURRENT_DATE - INTERVAL '30 days' "
        "GROUP BY date"
    )
    print(validation)


def example_explain_result():
    """Example: Explain a result with context."""
    print("\n" + "=" * 70)
    print("Example 3: Explain Result")
    print("=" * 70)
    
    result = explain_result("1500", "active_users", "last 7 days")
    print(result)


def example_compare_metrics():
    """Example: Compare two metrics."""
    print("\n" + "=" * 70)
    print("Example 4: Compare Metrics")
    print("=" * 70)
    
    result = compare_metrics("active_users", "revenue", "last 30 days")
    print(result)


def example_check_quality():
    """Example: Check data quality."""
    print("\n" + "=" * 70)
    print("Example 5: Check Data Quality")
    print("=" * 70)
    
    result = check_data_quality("conversion_rate", "last 7 days")
    print(result)


def example_workflow():
    """Example: Complete analysis workflow."""
    print("\n" + "=" * 70)
    print("Example 6: Complete Workflow")
    print("=" * 70)
    
    # 1. Ask initial question
    print("Step 1: Initial Question")
    print("-" * 40)
    result = ask_question("What was our revenue last week?")
    print(result)
    
    # 2. Check data quality
    print("\n\nStep 2: Check Data Quality")
    print("-" * 40)
    quality = check_data_quality("revenue", "last 7 days")
    print(quality)
    
    # 3. Compare with related metric
    print("\n\nStep 3: Compare with Related Metric")
    print("-" * 40)
    comparison = compare_metrics("revenue", "signups", "last 7 days")
    print(comparison)
    
    # 4. Generate reusable query
    print("\n\nStep 4: Generate Reusable Query")
    print("-" * 40)
    query = generate_query("revenue", "last 7 days", "", "date")
    print(query)


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "AI-Assisted Insights Agent - Python Examples" + " " * 14 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Run examples
    example_simple_question()
    example_generate_and_validate()
    example_explain_result()
    example_compare_metrics()
    example_check_quality()
    example_workflow()
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
