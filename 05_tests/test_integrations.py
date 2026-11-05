"""Tests for config, connectors, telemetry, and the SQL layer.

API connectors (Power BI, Adobe Analytics, Datadog) are tested against fake
HTTP sessions that check the exact requests sent. SQL tests run end to end
against the bundled SQLite demo warehouse.
"""

import importlib
import sqlite3
import textwrap
from datetime import date

import pytest

from insights_agent.connectors import ConnectorError
from insights_agent.models import AppConfig, load_config
from insights_agent.periods import DateRange, period_to_range

ACTIVE_USERS = {
    "name": "Active Users",
    "description": "Unique users who logged in",
    "sql_template": "COUNT(DISTINCT user_id)",
    "table": "analytics.user_events",
    "filter": "event_type = 'login'",
    "unit": "users",
    "date_column": "event_date",
}


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload
        self.text = text

    def json(self):
        return self._payload


class FakeSession:
    """Records POSTs and replies with queued responses."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, json=None, data=None, headers=None, timeout=None):
        self.calls.append({"url": url, "json": json, "data": data, "headers": headers or {}})
        return self.responses.pop(0)


# ---------------------------------------------------------------- periods

class TestPeriods:
    today = date(2026, 11, 4)

    def test_last_n_days_includes_today(self):
        r = period_to_range("last 7 days", self.today)
        assert r == DateRange(date(2026, 10, 29), date(2026, 11, 5))
        assert r.days == 7

    def test_last_month_is_the_previous_calendar_month(self):
        assert period_to_range("last month", self.today) == DateRange(date(2026, 10, 1), date(2026, 11, 1))

    def test_this_month(self):
        assert period_to_range("this month", self.today) == DateRange(date(2026, 11, 1), date(2026, 11, 5))

    def test_unknown_period_defaults_to_last_7_days(self):
        assert period_to_range("someday", self.today).days == 7


# ---------------------------------------------------------------- config

class TestConfig:
    def test_demo_config_loads_and_resolves_paths(self, monkeypatch):
        monkeypatch.delenv("INSIGHTS_CONFIG", raising=False)
        cfg = load_config("06_configs/config.demo.yaml")
        assert cfg.data_source.type == "sqlite"
        from pathlib import Path
        assert Path(cfg.data_source.path).parts[-2:] == ("03_data", "demo_analytics.db")
        assert set(cfg.metrics) == {"active_users", "revenue", "conversion_rate", "signups"}

    def test_no_config_means_none(self, monkeypatch):
        monkeypatch.delenv("INSIGHTS_CONFIG", raising=False)
        assert load_config() is None

    def test_unknown_source_type_is_rejected(self):
        with pytest.raises(Exception):
            AppConfig.model_validate({"data_source": {"type": "excel"}})

    def test_env_vars_expand(self, tmp_path, monkeypatch):
        monkeypatch.setenv("WAREHOUSE_URL", "postgresql://example/db")
        p = tmp_path / "c.yaml"
        p.write_text(textwrap.dedent("""
            data_source:
              type: sqlalchemy
              url: ${WAREHOUSE_URL}
              dialect: postgres
        """))
        assert load_config(str(p)).data_source.url == "postgresql://example/db"

    def test_every_source_type_validates(self):
        examples = [
            {"type": "fabric", "server": "x.datawarehouse.fabric.microsoft.com", "database": "db"},
            {"type": "databricks", "server_hostname": "adb.net", "http_path": "/sql/1.0/warehouses/x", "schema": "s"},
            {"type": "powerbi", "dataset_id": "abc"},
            {"type": "adobe_analytics", "global_company_id": "co", "report_suite_id": "rs"},
        ]
        for src in examples:
            assert AppConfig.model_validate({"data_source": src}).data_source.type == src["type"]


# ---------------------------------------------------------------- demo warehouse

def test_demo_warehouse_is_reproducible(tmp_path):
    from insights_agent import demo
    a = demo.build(tmp_path / "a.db", days=14, today=date(2026, 11, 4))
    b = demo.build(tmp_path / "b.db", days=14, today=date(2026, 11, 4))
    q = "SELECT COUNT(*), MIN(event_date), MAX(event_date) FROM user_events"
    ra, rb = (sqlite3.connect(p).execute(q).fetchone() for p in (a, b))
    assert ra == rb
    assert ra[1] == "2026-10-22" and ra[2] == "2026-11-04"


# ---------------------------------------------------------------- Power BI

class TestPowerBI:
    def test_dax_query_with_named_measure(self):
        from insights_agent.connectors.powerbi import build_dax_query
        metric = dict(ACTIVE_USERS, dax_measure="Active Users")
        dax = build_dax_query(metric, DateRange(date(2026, 10, 29), date(2026, 11, 5)), "'Date'[Date]")
        assert dax == ('EVALUATE ROW("Value", CALCULATE([Active Users], '
                       "DATESBETWEEN('Date'[Date], DATE(2026, 10, 29), DATE(2026, 11, 5) - 1)))")

    def test_execute_queries_request_and_parsing(self):
        from insights_agent.connectors.powerbi import PowerBIConnector
        session = FakeSession(FakeResponse(200, {"results": [{"tables": [{"rows": [{"[Value]": 1234}]}]}]}))
        conn = PowerBIConnector("ds1", "ws1", "'Date'[Date]", token_provider=lambda: "tok", session=session)
        result = conn.run_metric("active_users", dict(ACTIVE_USERS, dax_measure="Active Users"),
                                 DateRange(date(2026, 10, 29), date(2026, 11, 5)))
        call = session.calls[0]
        assert call["url"] == "https://api.powerbi.com/v1.0/myorg/groups/ws1/datasets/ds1/executeQueries"
        assert call["headers"]["Authorization"] == "Bearer tok"
        assert call["json"]["queries"][0]["query"].startswith("EVALUATE ROW")
        assert result.value == 1234 and result.query_language == "dax"

    def test_error_status_raises_connector_error(self):
        from insights_agent.connectors.powerbi import PowerBIConnector
        conn = PowerBIConnector("ds1", None, "'Date'[Date]", token_provider=lambda: "t",
                                session=FakeSession(FakeResponse(401, text="Unauthorized")))
        with pytest.raises(ConnectorError, match="401"):
            conn.execute_dax('EVALUATE ROW("ok", 1)')


# ---------------------------------------------------------------- Adobe Analytics

class TestAdobeAnalytics:
    def make(self, *responses):
        from insights_agent.connectors.adobe_analytics import AdobeAnalyticsConnector
        session = FakeSession(*responses)
        return AdobeAnalyticsConnector("acmeco", "acmersid", "cid", "secret", session=session), session

    def test_signs_in_then_requests_a_report(self):
        conn, session = self.make(
            FakeResponse(200, {"access_token": "abc", "expires_in": 86399}),
            FakeResponse(200, {"summaryData": {"totals": [5821]},
                               "rows": [{"value": "Oct 29, 2026", "data": [800]}]}),
        )
        metric = dict(ACTIVE_USERS, adobe_metric="metrics/visitors")
        result = conn.run_metric("active_users", metric, DateRange(date(2026, 10, 29), date(2026, 11, 5)))

        token_call, report_call = session.calls
        assert token_call["url"] == "https://ims-na1.adobelogin.com/ims/token/v3"
        assert token_call["data"]["grant_type"] == "client_credentials"
        assert report_call["url"] == "https://analytics.adobe.io/api/acmeco/reports"
        assert report_call["headers"]["x-api-key"] == "cid"
        assert report_call["headers"]["x-proxy-global-company-id"] == "acmeco"
        body = report_call["json"]
        assert body["rsid"] == "acmersid"
        assert body["metricContainer"]["metrics"][0]["id"] == "metrics/visitors"
        assert body["globalFilters"][0]["dateRange"] == "2026-10-29T00:00:00.000/2026-11-05T00:00:00.000"
        assert result.value == 5821

    def test_token_is_reused(self):
        report = {"summaryData": {"totals": [1]}, "rows": []}
        conn, session = self.make(FakeResponse(200, {"access_token": "abc", "expires_in": 3600}),
                                  FakeResponse(200, report), FakeResponse(200, report))
        metric = dict(ACTIVE_USERS, adobe_metric="metrics/visits")
        period = DateRange(date(2026, 10, 29), date(2026, 11, 5))
        conn.run_metric("a", metric, period)
        conn.run_metric("a", metric, period)
        assert len(session.calls) == 3   # one sign-in, two reports

    def test_metric_without_adobe_id_is_explained(self):
        conn, _ = self.make()
        with pytest.raises(ConnectorError, match="adobe_metric"):
            conn.run_metric("a", ACTIVE_USERS, DateRange(date(2026, 10, 29), date(2026, 11, 5)))


# ---------------------------------------------------------------- Datadog

class TestDatadog:
    def test_sends_duration_and_success_count(self):
        from insights_agent.telemetry import DatadogTelemetry
        session = FakeSession(FakeResponse(202, {}))
        DatadogTelemetry("key", "datadoghq.eu", "svc", session=session).record_query("revenue", "Fabric", 41.5, ok=True)
        call = session.calls[0]
        assert call["url"] == "https://api.datadoghq.eu/api/v2/series"
        assert call["headers"]["DD-API-KEY"] == "key"
        names = [s["metric"] for s in call["json"]["series"]]
        assert names == ["insights_agent.query.duration_ms", "insights_agent.query.success"]
        assert "metric:revenue" in call["json"]["series"][0]["tags"]

    def test_failures_never_raise(self):
        import requests
        from insights_agent.telemetry import DatadogTelemetry

        class Broken:
            def post(self, *a, **k):
                raise requests.ConnectionError("down")

        DatadogTelemetry("key", session=Broken()).record_query("m", "s", 1.0, ok=False)

    def test_disabled_without_api_key(self, monkeypatch):
        from insights_agent.models import Telemetry as TelemetryCfg
        from insights_agent.telemetry import from_config
        monkeypatch.delenv("DD_API_KEY", raising=False)
        cfg = TelemetryCfg.model_validate({"datadog": {"enabled": True}})
        assert from_config(cfg).enabled is False


# ---------------------------------------------------------------- SQL layer (SQLGlot)

class TestSQL:
    @pytest.fixture(autouse=True)
    def _need_sqlglot(self):
        pytest.importorskip("sqlglot")

    def test_metric_sql_targets_each_dialect(self):
        from insights_agent.sql import build_metric_sql
        period = DateRange(date(2026, 10, 29), date(2026, 11, 5))
        for dialect in ("fabric", "databricks", "snowflake", "sqlite"):
            sql = build_metric_sql(ACTIVE_USERS, period, dialect)
            assert "(DISTINCT user_id)" in sql   # T-SQL uses COUNT_BIG; others use COUNT
            assert "'2026-10-29'" in sql and "'2026-11-05'" in sql

    def test_read_only_guard(self):
        from insights_agent.sql import UnsafeQueryError, ensure_read_only
        ensure_read_only("SELECT 1")
        for bad in ("DELETE FROM t", "DROP TABLE t", "SELECT 1; DROP TABLE t", "INSERT INTO t SELECT 1"):
            with pytest.raises(UnsafeQueryError):
                ensure_read_only(bad)

    def test_fabric_uses_count_big(self):
        from insights_agent.sql import build_metric_sql
        sql = build_metric_sql(ACTIVE_USERS, DateRange(date(2026, 10, 29), date(2026, 11, 5)), "fabric")
        assert "COUNT_BIG(DISTINCT user_id)" in sql

    def test_transpile_to_fabric(self):
        from insights_agent.sql import transpile
        out = transpile("SELECT name FROM users LIMIT 5", "fabric", pretty=False)
        assert "TOP 5" in out

    def test_metric_to_dax(self):
        from insights_agent.sql import metric_to_dax
        assert metric_to_dax(ACTIVE_USERS) == \
            "CALCULATE(DISTINCTCOUNT('user_events'[user_id]), 'user_events'[event_type] = \"login\")"
        revenue = {"table": "analytics.transactions", "sql_template": "SUM(amount)", "filter": ""}
        assert metric_to_dax(revenue) == "SUM('transactions'[amount])"
        assert metric_to_dax({"table": "t", "sql_template": "AVG(a) * 100.0", "filter": ""}) is None


# ---------------------------------------------------------------- end to end on the demo warehouse

class TestEndToEnd:
    @pytest.fixture
    def demo_runtime(self, tmp_path, monkeypatch):
        pytest.importorskip("sqlglot")
        pytest.importorskip("sqlalchemy")
        from insights_agent import demo, runtime, server

        db = demo.build(tmp_path / "demo.db", days=30)
        cfg = tmp_path / "config.yaml"
        cfg.write_text(open("06_configs/config.demo.yaml").read()
                       .replace("../03_data/demo_analytics.db", str(db)))
        monkeypatch.setenv("INSIGHTS_CONFIG", str(cfg))
        saved = (dict(server.METRIC_DEFINITIONS), dict(server.BUSINESS_GLOSSARY))
        rt = runtime.get_runtime(server.METRIC_DEFINITIONS, server.BUSINESS_GLOSSARY, reload=True)
        yield server, rt, db
        server.METRIC_DEFINITIONS.clear(); server.METRIC_DEFINITIONS.update(saved[0])
        server.BUSINESS_GLOSSARY.clear(); server.BUSINESS_GLOSSARY.update(saved[1])
        monkeypatch.delenv("INSIGHTS_CONFIG")
        runtime.get_runtime(reload=True)

    def test_answer_matches_the_database(self, demo_runtime):
        server, rt, db = demo_runtime
        from insights_agent.periods import period_to_range
        period = period_to_range("last 7 days")
        expected = sqlite3.connect(db).execute(
            "SELECT COUNT(DISTINCT user_id) FROM user_events WHERE event_type = 'login' "
            "AND event_date >= ? AND event_date < ?", (period.start.isoformat(), period.end.isoformat())
        ).fetchone()[0]
        out = server.ask_question("How many active users did we have last week?")
        assert f"Answer: {expected:,} users" in out
        assert "Source: SQLite" in out
        assert "simulated" not in out.lower().split("data quality")[0]

    def test_run_query_rejects_writes(self, demo_runtime):
        server, _, _ = demo_runtime
        assert "Query not run" in server.run_query("DELETE FROM analytics.user_events")
        assert "row(s)" in server.run_query("SELECT COUNT(*) AS n FROM analytics.signups")

    def test_compare_computes_real_correlation(self, demo_runtime):
        server, _, _ = demo_runtime
        out = server.compare_metrics("active_users", "signups", "last 30 days")
        assert "correlation (r = " in out or "Correlation undefined" in out

    def test_list_data_sources_reports_connection(self, demo_runtime):
        server, _, _ = demo_runtime
        out = server.list_data_sources()
        assert "Active: SQLite" in out and "Connected to SQLite" in out
