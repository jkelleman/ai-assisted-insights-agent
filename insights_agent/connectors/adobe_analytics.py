"""Adobe Analytics report suites, queried through the Analytics 2.0 Reports API
with OAuth Server-to-Server credentials from the Adobe Developer Console.

Docs: https://developer.adobe.com/analytics-apis/docs/2.0/guides/endpoints/reports/
"""

from __future__ import annotations

import os
import time
from typing import Optional

import requests

from ..periods import DateRange
from .base import ConnectorError, QueryResult

IMS_TOKEN_URL = "https://ims-na1.adobelogin.com/ims/token/v3"
ANALYTICS_API = "https://analytics.adobe.io/api"
IMS_SCOPES = "openid,AdobeID,additional_info.projectedProductContext"


class AdobeAnalyticsConnector:
    def __init__(self, global_company_id: str, report_suite_id: str,
                 client_id: str, client_secret: str,
                 session: Optional[requests.Session] = None):
        self.global_company_id = global_company_id
        self.report_suite_id = report_suite_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = session or requests.Session()
        self.label = f"Adobe Analytics ({report_suite_id})"
        self._token: Optional[str] = None
        self._token_expires = 0.0

    @classmethod
    def from_env(cls, global_company_id: str, report_suite_id: str,
                 client_id_env: str, client_secret_env: str) -> "AdobeAnalyticsConnector":
        client_id, secret = os.environ.get(client_id_env), os.environ.get(client_secret_env)
        if not client_id or not secret:
            raise ConnectorError(f"Set {client_id_env} and {client_secret_env} from your Adobe Developer Console project")
        return cls(global_company_id, report_suite_id, client_id, secret)

    def _access_token(self) -> str:
        if self._token and time.time() < self._token_expires - 60:
            return self._token
        resp = self.session.post(IMS_TOKEN_URL, timeout=30, data={
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": IMS_SCOPES,
        })
        if resp.status_code != 200:
            raise ConnectorError(f"Adobe sign-in failed ({resp.status_code}). Check the client ID and secret.")
        payload = resp.json()
        self._token = payload["access_token"]
        self._token_expires = time.time() + float(payload.get("expires_in", 3600))
        return self._token

    def report_request(self, adobe_metric: str, period: DateRange) -> dict:
        date_range = f"{period.start.isoformat()}T00:00:00.000/{period.end.isoformat()}T00:00:00.000"
        return {
            "rsid": self.report_suite_id,
            "globalFilters": [{"type": "dateRange", "dateRange": date_range}],
            "metricContainer": {"metrics": [{"columnId": "0", "id": adobe_metric}]},
            "dimension": "variables/daterangeday",
            "settings": {"limit": 400, "page": 0},
        }

    def run_metric(self, metric_id: str, metric: dict, period: DateRange) -> QueryResult:
        adobe_metric = metric.get("adobe_metric")
        if not adobe_metric:
            raise ConnectorError(f"{metric['name']} has no adobe_metric (for example metrics/visits) in the config")
        body = self.report_request(adobe_metric, period)
        start = time.perf_counter()
        resp = self.session.post(f"{ANALYTICS_API}/{self.global_company_id}/reports", json=body, timeout=60, headers={
            "Authorization": f"Bearer {self._access_token()}",
            "x-api-key": self.client_id,
            "x-proxy-global-company-id": self.global_company_id,
            "Accept": "application/json",
        })
        elapsed = (time.perf_counter() - start) * 1000
        if resp.status_code != 200:
            raise ConnectorError(f"Adobe Analytics returned {resp.status_code}: {resp.text[:300]}")
        data = resp.json()
        try:
            total = data["summaryData"]["totals"][0]
        except (KeyError, IndexError) as e:
            raise ConnectorError("Adobe Analytics returned an unexpected response shape") from e
        rows = [{"day": r.get("value"), "value": (r.get("data") or [None])[0]} for r in data.get("rows", [])]
        summary = f"POST /reports  rsid={self.report_suite_id}  metric={adobe_metric}  dateRange={body['globalFilters'][0]['dateRange']}"
        return QueryResult(value=float(total), query=summary, query_language="adobe-analytics-api",
                           source=self.label, elapsed_ms=elapsed, rows=rows)

    def health_check(self) -> str:
        self._access_token()
        return f"Signed in to Adobe Analytics for {self.global_company_id}"
