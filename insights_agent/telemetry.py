"""Query telemetry sent to Datadog through the Metrics API (v2 series endpoint).

Reports, per query: duration, a success count, and an error count, tagged with
the metric, source, and service. Telemetry never blocks or breaks an answer:
failures are logged and ignored.

Docs: https://docs.datadoghq.com/api/latest/metrics/#submit-metrics
"""

from __future__ import annotations

import logging
import os
import time
from typing import List, Optional

import requests

log = logging.getLogger(__name__)

GAUGE, COUNT = 3, 1   # Datadog v2 metric intake types


class Telemetry:
    """No-op by default. DatadogTelemetry subclasses it when enabled."""

    enabled = False

    def record_query(self, metric_id: str, source: str, elapsed_ms: float, ok: bool) -> None:
        return None


class DatadogTelemetry(Telemetry):
    enabled = True

    def __init__(self, api_key: str, site: str = "datadoghq.com", service: str = "insights-agent",
                 session: Optional[requests.Session] = None):
        self.api_key = api_key
        self.url = f"https://api.{site}/api/v2/series"
        self.service = service
        self.session = session or requests.Session()

    def series(self, metric_id: str, source: str, elapsed_ms: float, ok: bool, now: Optional[int] = None) -> List[dict]:
        now = now or int(time.time())
        tags = [f"service:{self.service}", f"metric:{metric_id}", f"source:{source}"]
        name = "insights_agent.query.success" if ok else "insights_agent.query.error"
        return [
            {"metric": "insights_agent.query.duration_ms", "type": GAUGE,
             "points": [{"timestamp": now, "value": round(elapsed_ms, 2)}], "tags": tags},
            {"metric": name, "type": COUNT, "interval": 10,
             "points": [{"timestamp": now, "value": 1}], "tags": tags},
        ]

    def record_query(self, metric_id: str, source: str, elapsed_ms: float, ok: bool) -> None:
        try:
            resp = self.session.post(self.url, json={"series": self.series(metric_id, source, elapsed_ms, ok)},
                                     headers={"DD-API-KEY": self.api_key, "Content-Type": "application/json"},
                                     timeout=3)
            if resp.status_code >= 300:
                log.warning("Datadog rejected telemetry: %s %s", resp.status_code, resp.text[:200])
        except requests.RequestException as e:
            log.warning("Couldn't send telemetry to Datadog: %s", e)


def from_config(cfg) -> Telemetry:
    """Build telemetry from the config's telemetry.datadog section."""
    if cfg is None or not cfg.datadog.enabled:
        return Telemetry()
    key = os.environ.get(cfg.datadog.api_key_env)
    if not key:
        log.warning("Datadog telemetry is enabled but %s isn't set; telemetry is off", cfg.datadog.api_key_env)
        return Telemetry()
    return DatadogTelemetry(key, cfg.datadog.site, cfg.datadog.service)
