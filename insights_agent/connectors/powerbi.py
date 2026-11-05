"""Power BI semantic models, queried with DAX through the executeQueries REST API.

Docs: https://learn.microsoft.com/rest/api/power-bi/datasets/execute-queries
"""

from __future__ import annotations

import time
from typing import Any, Callable, Optional

import requests

from ..periods import DateRange
from .base import ConnectorError, QueryResult

POWERBI_SCOPE = "https://analysis.windows.net/powerbi/api/.default"
API_ROOT = "https://api.powerbi.com/v1.0/myorg"


def dax_for_metric(metric: dict) -> Optional[str]:
    """The DAX expression for a metric: an existing model measure if named, else a translation of its SQL."""
    if metric.get("dax_measure"):
        return f"[{metric['dax_measure']}]"
    from .. import sql as sqltools  # imported here so DAX-only setups don't need SQLGlot loaded
    return sqltools.metric_to_dax(metric)


def build_dax_query(metric: dict, period: DateRange, date_column: str) -> str:
    """A DAX query that returns the metric's value for the date range as one row."""
    expression = dax_for_metric(metric)
    if expression is None:
        raise ConnectorError(f"Can't translate {metric['name']} to DAX. Set dax_measure in the config.")
    start, end = period.start, period.end
    date_filter = (f"DATESBETWEEN({date_column}, DATE({start.year}, {start.month}, {start.day}), "
                   f"DATE({end.year}, {end.month}, {end.day}) - 1)")
    return f'EVALUATE ROW("Value", CALCULATE({expression}, {date_filter}))'


class PowerBIConnector:
    def __init__(self, dataset_id: str, workspace_id: Optional[str], date_column: str,
                 token_provider: Optional[Callable[[], str]] = None,
                 session: Optional[requests.Session] = None):
        self.dataset_id = dataset_id
        self.workspace_id = workspace_id
        self.date_column = date_column
        self.session = session or requests.Session()
        self._token_provider = token_provider or _azure_token_provider(POWERBI_SCOPE)
        self.label = "Power BI semantic model"

    @property
    def url(self) -> str:
        base = f"{API_ROOT}/groups/{self.workspace_id}" if self.workspace_id else API_ROOT
        return f"{base}/datasets/{self.dataset_id}/executeQueries"

    def execute_dax(self, dax: str) -> list:
        body = {"queries": [{"query": dax}], "serializerSettings": {"includeNulls": True}}
        resp = self.session.post(self.url, json=body, timeout=60,
                                 headers={"Authorization": f"Bearer {self._token_provider()}"})
        if resp.status_code != 200:
            raise ConnectorError(f"Power BI returned {resp.status_code}: {resp.text[:300]}")
        try:
            return resp.json()["results"][0]["tables"][0]["rows"]
        except (KeyError, IndexError, ValueError) as e:
            raise ConnectorError("Power BI returned an unexpected response shape") from e

    def run_metric(self, metric_id: str, metric: dict, period: DateRange) -> QueryResult:
        dax = build_dax_query(metric, period, self.date_column)
        start = time.perf_counter()
        rows = self.execute_dax(dax)
        elapsed = (time.perf_counter() - start) * 1000
        value = None
        if rows:
            raw = rows[0].get("[Value]")
            value = float(raw) if raw is not None else None
        return QueryResult(value=value, query=dax, query_language="dax", source=self.label,
                           elapsed_ms=elapsed, rows=rows)

    def health_check(self) -> str:
        self.execute_dax('EVALUATE ROW("ok", 1)')
        return f"Connected to {self.label} {self.dataset_id}"


def _azure_token_provider(scope: str) -> Callable[[], str]:
    def provider() -> str:
        try:
            from azure.identity import DefaultAzureCredential
        except ImportError as e:
            raise ConnectorError("Power BI needs azure-identity. "
                                 "Install with: pip install 'ai-insights-agent[powerbi]'") from e
        return DefaultAzureCredential().get_token(scope).token
    return provider
