"""Turn time-period phrases into concrete date ranges.

Executed queries use literal dates instead of dialect-specific interval math,
so the same metric SQL runs unchanged on SQLite, Fabric, Databricks, and others.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass(frozen=True)
class DateRange:
    start: date          # inclusive
    end: date            # exclusive

    @property
    def days(self) -> int:
        return (self.end - self.start).days


def period_to_range(time_period: str, today: Optional[date] = None) -> DateRange:
    """Resolve "last 7 days", "this month", or "last month". Defaults to the last 7 days."""
    today = today or date.today()
    tomorrow = today + timedelta(days=1)
    text = time_period.lower().strip()

    match = re.search(r"(\d+)\s*days?", text)
    if "last" in text and match:
        return DateRange(tomorrow - timedelta(days=int(match.group(1))), tomorrow)

    match = re.search(r"(\d+)\s*weeks?", text)
    if ("last" in text or "past" in text) and match:
        return DateRange(tomorrow - timedelta(days=7 * int(match.group(1))), tomorrow)

    if "this month" in text:
        return DateRange(today.replace(day=1), tomorrow)

    if "last month" in text:
        first_this_month = today.replace(day=1)
        first_last_month = (first_this_month - timedelta(days=1)).replace(day=1)
        return DateRange(first_last_month, first_this_month)

    if "last week" in text:
        return DateRange(tomorrow - timedelta(days=7), tomorrow)

    return DateRange(tomorrow - timedelta(days=7), tomorrow)
