"""
Pytest configuration and fixtures for tests.
"""
import pytest
from typing import Dict, Any


@pytest.fixture
def sample_metric():
    """Sample metric definition for testing."""
    return {
        "name": "Test Metric",
        "description": "A test metric for unit tests",
        "sql_template": "COUNT(DISTINCT user_id)",
        "table": "test_table",
        "filter": "status = 'active'",
        "unit": "users"
    }


@pytest.fixture
def sample_question():
    """Sample natural language question."""
    return "How many active users did we have last week?"


@pytest.fixture
def sample_sql_query():
    """Sample SQL query."""
    return """SELECT COUNT(DISTINCT user_id)
FROM analytics.user_events
WHERE event_type = 'login'
  AND event_date >= CURRENT_DATE - INTERVAL '7 days'"""


@pytest.fixture
def mock_metric_definitions():
    """Mock metric definitions for testing."""
    return {
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
        }
    }
