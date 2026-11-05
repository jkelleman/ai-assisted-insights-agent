"""Shared types for data-source connectors."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol

from ..periods import DateRange


class ConnectorError(RuntimeError):
    """A data source could not be reached or returned an error. The message is safe to show users."""


@dataclass
class QueryResult:
    value: Optional[float]
    query: str                      # the exact SQL, DAX, or API request that ran
    query_language: str             # "sql", "dax", or "adobe-analytics-api"
    source: str                     # human-readable source label
    elapsed_ms: float = 0.0
    rows: List[Dict[str, Any]] = field(default_factory=list)


class Connector(Protocol):
    """A data source the agent can answer metric questions from."""

    label: str

    def run_metric(self, metric_id: str, metric: dict, period: DateRange) -> QueryResult:
        ...

    def health_check(self) -> str:
        ...
