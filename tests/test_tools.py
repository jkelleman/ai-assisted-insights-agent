"""
Integration tests for MCP tools.
"""
import pytest
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
    QUERY_TEMPLATES,
    QUERY_HISTORY
)


class TestAskQuestionTool:
    """Tests for ask_question tool."""
    
    def test_ask_valid_question(self):
        """Test asking a valid question."""
        result = ask_question("How many active users last week?", "last 7 days")
        assert "Answer:" in result
        assert "Query Used:" in result
        assert "Explanation:" in result
        assert "Data Quality:" in result
    
    def test_ask_invalid_question(self):
        """Test asking an invalid question."""
        result = ask_question("What is the meaning of life?", "last 7 days")
        assert "Unable to parse question" in result
        assert "Suggestions:" in result
    
    def test_ask_question_with_time_period(self):
        """Test asking question with custom time period."""
        result = ask_question("How many signups?", "last 30 days")
        assert "Time Period: last 30 days" in result


class TestGenerateQueryTool:
    """Tests for generate_query tool."""
    
    def test_generate_valid_metric(self):
        """Test generating query for valid metric."""
        result = generate_query("active_users", "last 7 days")
        assert "Generated Query" in result
        assert "SELECT" in result
        assert "FROM" in result
    
    def test_generate_invalid_metric(self):
        """Test generating query for invalid metric."""
        result = generate_query("invalid_metric", "last 7 days")
        assert "not found" in result
    
    def test_generate_with_filters(self):
        """Test generating query with filters."""
        result = generate_query("active_users", "last 7 days", "country = 'US'")
        assert "country = 'US'" in result
    
    def test_generate_with_group_by(self):
        """Test generating query with GROUP BY."""
        result = generate_query("active_users", "last 7 days", "", "date")
        assert "GROUP BY" in result


class TestValidateQueryTool:
    """Tests for validate_query tool."""
    
    def test_validate_valid_query(self):
        """Test validating a valid query."""
        sql = "SELECT COUNT(*) FROM users WHERE date >= '2025-01-01'"
        result = validate_query(sql)
        assert "validation checks passed" in result or "valid and ready" in result
    
    def test_validate_invalid_query(self):
        """Test validating an invalid query."""
        sql = "INVALID SQL STATEMENT"
        result = validate_query(sql)
        assert "Issues Found" in result or "must start with SELECT" in result
    
    def test_validate_select_star(self):
        """Test validation warning for SELECT *."""
        sql = "SELECT * FROM users"
        result = validate_query(sql)
        assert "Warnings" in result or "SELECT *" in result


class TestExplainResultTool:
    """Tests for explain_result tool."""
    
    def test_explain_valid_result(self):
        """Test explaining a valid result."""
        result = explain_result("1500", "active_users", "last 7 days")
        assert "Result Explanation" in result
        assert "Context:" in result
        assert "Interpretation:" in result
    
    def test_explain_invalid_metric(self):
        """Test explaining result for invalid metric."""
        result = explain_result("1500", "invalid_metric", "last 7 days")
        assert "not found" in result
    
    def test_explain_invalid_value(self):
        """Test explaining invalid result value."""
        result = explain_result("not_a_number", "active_users", "last 7 days")
        assert "Could not parse" in result


class TestSuggestFollowupsTool:
    """Tests for suggest_followups tool."""
    
    def test_suggest_valid_question(self):
        """Test suggesting follow-ups for valid question."""
        result = suggest_followups("How many active users last week?")
        assert "Follow-up Suggestions" in result
        assert "Drill-Down Questions:" in result
    
    def test_suggest_invalid_question(self):
        """Test suggesting follow-ups for invalid question."""
        result = suggest_followups("Invalid question")
        assert "Unable to generate follow-ups" in result


class TestQueryTemplateTool:
    """Tests for query template tools."""
    
    def setup_method(self):
        """Clear templates before each test."""
        QUERY_TEMPLATES.clear()
    
    def test_save_template(self):
        """Test saving a query template."""
        result = save_query_template(
            "Test Template",
            "SELECT * FROM users",
            "Test description"
        )
        assert "Query Template Saved" in result
        assert "test_template" in QUERY_TEMPLATES
    
    def test_save_duplicate_template(self):
        """Test saving duplicate template."""
        save_query_template("Test", "SELECT 1", "Test")
        result = save_query_template("Test", "SELECT 2", "Duplicate")
        assert "already exists" in result
    
    def test_list_empty_templates(self):
        """Test listing when no templates exist."""
        result = list_templates()
        assert "No query templates" in result
    
    def test_list_templates(self):
        """Test listing saved templates."""
        save_query_template("Template 1", "SELECT 1", "First")
        save_query_template("Template 2", "SELECT 2", "Second")
        result = list_templates()
        assert "Template 1" in result
        assert "Template 2" in result


class TestDataQualityTool:
    """Tests for data quality checking."""
    
    def test_check_valid_metric(self):
        """Test checking data quality for valid metric."""
        result = check_data_quality("active_users", "last 7 days")
        assert "Data Quality Report" in result
        assert "Freshness:" in result
        assert "Completeness:" in result
        assert "Anomaly Detection:" in result
    
    def test_check_invalid_metric(self):
        """Test checking data quality for invalid metric."""
        result = check_data_quality("invalid_metric", "last 7 days")
        assert "not found" in result


class TestCompareMetricsTool:
    """Tests for metric comparison."""
    
    def test_compare_valid_metrics(self):
        """Test comparing two valid metrics."""
        result = compare_metrics("active_users", "revenue", "last 7 days")
        assert "Metric Comparison" in result
        assert "Active Users" in result
        assert "Total Revenue" in result
    
    def test_compare_invalid_first_metric(self):
        """Test comparing with invalid first metric."""
        result = compare_metrics("invalid", "revenue", "last 7 days")
        assert "not found" in result
    
    def test_compare_invalid_second_metric(self):
        """Test comparing with invalid second metric."""
        result = compare_metrics("active_users", "invalid", "last 7 days")
        assert "not found" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
