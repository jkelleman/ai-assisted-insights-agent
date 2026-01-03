"""
Tests for server.py tools and functionality.
"""
import pytest
from insights_agent.server import (
    _parse_question,
    _generate_sql_query,
    _parse_time_period,
    _simulate_query_execution,
    _find_similar_metrics,
    _list_available_metrics,
    METRIC_DEFINITIONS,
    BUSINESS_GLOSSARY
)


class TestQuestionParsing:
    """Tests for natural language question parsing."""
    
    def test_parse_simple_question(self):
        """Test parsing a simple question."""
        result = _parse_question("How many active users last week?")
        assert "active_users" in result["metrics"]
        assert result["time_period"] == "last 7 days"
    
    def test_parse_question_with_business_term(self):
        """Test parsing with business terminology."""
        result = _parse_question("How many customers did we have?")
        assert result["original_question"] == "How many customers did we have?"
        # Should map "customers" to "users"
    
    def test_parse_question_multiple_metrics(self):
        """Test parsing question mentioning multiple metrics."""
        result = _parse_question("Compare active users and revenue")
        assert len(result["metrics"]) >= 1
    
    def test_parse_question_no_metrics(self):
        """Test parsing question with no identifiable metrics."""
        result = _parse_question("What happened yesterday?")
        assert len(result["metrics"]) == 0


class TestTimePersiodParsing:
    """Tests for time period parsing."""
    
    def test_parse_last_n_days(self):
        """Test parsing 'last N days' format."""
        result = _parse_time_period("last 7 days")
        assert "INTERVAL '7 days'" in result
        assert "event_date >=" in result
    
    def test_parse_this_month(self):
        """Test parsing 'this month'."""
        result = _parse_time_period("this month")
        assert "DATE_TRUNC('month'" in result
    
    def test_parse_last_month(self):
        """Test parsing 'last month'."""
        result = _parse_time_period("last month")
        assert "DATE_TRUNC('month'" in result
    
    def test_parse_default_period(self):
        """Test default time period."""
        result = _parse_time_period("invalid period")
        assert "INTERVAL '7 days'" in result


class TestSQLGeneration:
    """Tests for SQL query generation."""
    
    def test_generate_basic_query(self):
        """Test generating a basic query."""
        parsed = {
            "metrics": ["active_users"],
            "time_period": "last 7 days",
            "original_question": "How many active users?"
        }
        result = _generate_sql_query(parsed, "last 7 days")
        assert result["error"] is None
        assert "SELECT" in result["sql"]
        assert "FROM analytics.user_events" in result["sql"]
    
    def test_generate_query_no_metrics(self):
        """Test generating query with no metrics."""
        parsed = {
            "metrics": [],
            "time_period": "last 7 days",
            "original_question": "Invalid question"
        }
        result = _generate_sql_query(parsed, "last 7 days")
        assert result["error"] is not None
    
    def test_generate_query_with_filter(self):
        """Test generating query with metric filter."""
        parsed = {
            "metrics": ["active_users"],
            "time_period": "last 7 days",
            "original_question": "Test"
        }
        result = _generate_sql_query(parsed, "last 7 days")
        assert "event_type = 'login'" in result["sql"]


class TestMetricDiscovery:
    """Tests for metric discovery and search."""
    
    def test_list_available_metrics(self):
        """Test listing all metrics."""
        result = _list_available_metrics()
        assert "Active Users" in result
        assert "Total Revenue" in result
    
    def test_find_similar_metrics_exact(self):
        """Test finding similar metrics with exact match."""
        result = _find_similar_metrics("active")
        assert len(result) > 0
        assert "Active Users" in result
    
    def test_find_similar_metrics_no_match(self):
        """Test finding similar metrics with no match."""
        result = _find_similar_metrics("xyz123invalid")
        assert len(result) == 0


class TestQueryExecution:
    """Tests for query execution simulation."""
    
    def test_simulate_count_query(self):
        """Test simulating a COUNT query."""
        sql = "SELECT COUNT(*) FROM table"
        result = _simulate_query_execution(sql)
        assert isinstance(result, float)
        assert result > 0
    
    def test_simulate_sum_query(self):
        """Test simulating a SUM query."""
        sql = "SELECT SUM(amount) FROM transactions"
        result = _simulate_query_execution(sql)
        assert isinstance(result, float)
        assert result > 0
    
    def test_simulate_avg_query(self):
        """Test simulating an AVG query."""
        sql = "SELECT AVG(value) FROM table"
        result = _simulate_query_execution(sql)
        assert isinstance(result, float)
        assert result > 0


class TestDataStructures:
    """Tests for data structures and configurations."""
    
    def test_metric_definitions_structure(self):
        """Test metric definitions have required fields."""
        for metric_id, metric in METRIC_DEFINITIONS.items():
            assert "name" in metric
            assert "description" in metric
            assert "sql_template" in metric
            assert "table" in metric
            assert "filter" in metric
            assert "unit" in metric
    
    def test_business_glossary_structure(self):
        """Test business glossary structure."""
        assert isinstance(BUSINESS_GLOSSARY, dict)
        assert len(BUSINESS_GLOSSARY) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
