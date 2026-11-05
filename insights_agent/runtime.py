"""Connects the MCP tools to a configured data source and telemetry.

Loaded once, on first use. With no INSIGHTS_CONFIG set, there is no data source
and the tools fall back to simulated values, labeled as simulated.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Dict, Optional

from . import telemetry as telemetry_mod
from .connectors import Connector, ConnectorError, QueryResult, build_connector
from .models import AppConfig, load_config
from .periods import period_to_range

log = logging.getLogger(__name__)


@dataclass
class Runtime:
    config: Optional[AppConfig]
    connector: Optional[Connector]
    telemetry: telemetry_mod.Telemetry
    error: Optional[str] = None      # why the configured source isn't available, if it isn't

    @property
    def source_label(self) -> str:
        if self.connector:
            return self.connector.label
        return "simulated (no data source configured)"

    def run_metric(self, metric_id: str, metric: dict, time_period: str) -> QueryResult:
        """Run one metric on the configured source and record telemetry."""
        if not self.connector:
            raise ConnectorError(self.error or "No data source configured")
        start = time.perf_counter()
        try:
            result = self.connector.run_metric(metric_id, metric, period_to_range(time_period))
        except Exception:
            self.telemetry.record_query(metric_id, self.connector.label, (time.perf_counter() - start) * 1000, ok=False)
            raise
        self.telemetry.record_query(metric_id, self.connector.label, result.elapsed_ms, ok=True)
        return result


_runtime: Optional[Runtime] = None


def get_runtime(metric_definitions: Optional[Dict] = None, glossary: Optional[Dict] = None,
                reload: bool = False) -> Runtime:
    """Load config once. Metrics and glossary entries from the config are merged into
    the dictionaries passed in, so the MCP tools see the configured catalog."""
    global _runtime
    if _runtime is not None and not reload:
        return _runtime

    try:
        config = load_config()
    except Exception as e:
        log.error("Couldn't load config: %s", e)
        _runtime = Runtime(None, None, telemetry_mod.Telemetry(), error=f"Config error: {e}")
        return _runtime

    if config is None:
        _runtime = Runtime(None, None, telemetry_mod.Telemetry())
        return _runtime

    if metric_definitions is not None and config.metrics:
        metric_definitions.clear()
        metric_definitions.update({k: v.model_dump() for k, v in config.metrics.items()})
    if glossary is not None and config.business_glossary:
        glossary.clear()
        glossary.update(config.business_glossary)

    connector, error = None, None
    if config.data_source is not None:
        try:
            connector = build_connector(config.data_source)
        except ConnectorError as e:
            error = str(e)
            log.error("Data source unavailable: %s", e)
    _runtime = Runtime(config, connector, telemetry_mod.from_config(config.telemetry), error=error)
    return _runtime
