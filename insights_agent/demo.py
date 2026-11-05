"""Build a small local demo warehouse so the agent can run real queries without credentials.

    python -m insights_agent.demo
    INSIGHTS_CONFIG=06_configs/config.demo.yaml python -m insights_agent.cli

Creates 03_data/demo_analytics.db with 90 days of synthetic product analytics,
ending today: user_events, transactions, user_sessions, and signups. The data
is generated from a fixed seed, so it's the same every time you build it.
"""

from __future__ import annotations

import argparse
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "03_data" / "demo_analytics.db"

SCHEMA = """
CREATE TABLE user_events (user_id INTEGER, event_type TEXT, event_date TEXT);
CREATE TABLE transactions (user_id INTEGER, amount REAL, status TEXT, event_date TEXT);
CREATE TABLE user_sessions (user_id INTEGER, purchased INTEGER, event_date TEXT);
CREATE TABLE signups (user_id INTEGER, event_date TEXT);
CREATE INDEX idx_events_date ON user_events (event_date);
CREATE INDEX idx_tx_date ON transactions (event_date);
CREATE INDEX idx_sessions_date ON user_sessions (event_date);
CREATE INDEX idx_signups_date ON signups (event_date);
"""


def build(path: Path = DEFAULT_PATH, days: int = 90, users: int = 4000, seed: int = 7,
          today: date | None = None) -> Path:
    """Create (or replace) the demo database and return its path."""
    rng = random.Random(seed)
    today = today or date.today()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()

    events, tx, sessions, signups = [], [], [], []
    next_user = users
    for offset in range(days, 0, -1):
        day = today - timedelta(days=offset - 1)
        d = day.isoformat()
        weekend = day.weekday() >= 5
        daily_active = int(rng.gauss(620 if weekend else 780, 40))
        for uid in rng.sample(range(next_user), min(daily_active, next_user)):
            events.append((uid, "login", d))
            if rng.random() < 0.35:
                events.append((uid, "view_report", d))
            purchased = rng.random() < 0.031
            sessions.append((uid, int(purchased), d))
            if purchased:
                status = "completed" if rng.random() < 0.94 else "refunded"
                tx.append((uid, round(rng.uniform(12, 140), 2), status, d))
        for _ in range(int(rng.gauss(55, 9))):
            signups.append((next_user, d))
            next_user += 1

    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA)
        conn.executemany("INSERT INTO user_events VALUES (?, ?, ?)", events)
        conn.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?)", tx)
        conn.executemany("INSERT INTO user_sessions VALUES (?, ?, ?)", sessions)
        conn.executemany("INSERT INTO signups VALUES (?, ?)", signups)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the local demo warehouse.")
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--days", type=int, default=90)
    args = parser.parse_args()
    out = build(args.path, args.days)
    print(f"Built demo warehouse: {out}")
    print("Try it: INSIGHTS_CONFIG=06_configs/config.demo.yaml python -m insights_agent.cli")


if __name__ == "__main__":
    main()
