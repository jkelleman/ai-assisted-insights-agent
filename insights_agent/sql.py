"""SQL handling with SQLGlot: build metric queries, translate them between
dialects, enforce read-only access, and convert simple metrics to DAX.

Metric definitions are written once in PostgreSQL-style SQL (the "source
dialect"). SQLGlot translates them for whichever warehouse runs the query.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError

from .periods import DateRange

SOURCE_DIALECT = "postgres"

# Friendly names people use, mapped to SQLGlot dialect names.
DIALECT_ALIASES = {
    "fabric": "tsql",
    "sqlserver": "tsql",
    "azure sql": "tsql",
    "synapse": "tsql",
    "databricks": "databricks",
    "spark": "spark",
    "snowflake": "snowflake",
    "bigquery": "bigquery",
    "postgres": "postgres",
    "postgresql": "postgres",
    "mysql": "mysql",
    "sqlite": "sqlite",
    "duckdb": "duckdb",
    "redshift": "redshift",
}

# Statement types that change data or schema. Looked up by name because a few
# were renamed across SQLGlot versions (for example AlterTable became Alter).
WRITE_NODES = tuple(
    getattr(exp, name)
    for name in ("Insert", "Update", "Delete", "Merge", "Create", "Drop",
                 "Alter", "AlterTable", "Command", "TruncateTable", "Grant")
    if hasattr(exp, name)
)


class UnsafeQueryError(ValueError):
    """Raised when SQL would modify data or isn't a single read-only query."""


def resolve_dialect(name: str) -> str:
    return DIALECT_ALIASES.get(name.strip().lower(), name.strip().lower())


def build_metric_sql(metric: dict, period: DateRange, dialect: str, group_by: str = "") -> str:
    """Build the SQL for one metric over a date range, in the target dialect."""
    date_col = metric.get("date_column") or "event_date"
    conditions = []
    if metric.get("filter"):
        conditions.append(f"({metric['filter']})")
    conditions.append(f"{date_col} >= '{period.start.isoformat()}'")
    conditions.append(f"{date_col} < '{period.end.isoformat()}'")

    select = metric["sql_template"]
    if group_by:
        select = f"{group_by}, {select} AS value"
    sql = f"SELECT {select} FROM {metric['table']} WHERE {' AND '.join(conditions)}"
    if group_by:
        sql += f" GROUP BY {group_by} ORDER BY {group_by}"
    return transpile(sql, resolve_dialect(dialect))


def transpile(sql: str, write: str, read: str = SOURCE_DIALECT, pretty: bool = True) -> str:
    """Translate one SQL statement from one dialect to another."""
    out = sqlglot.transpile(sql, read=resolve_dialect(read), write=resolve_dialect(write), pretty=pretty)
    if len(out) != 1:
        raise ValueError(f"Expected one SQL statement, found {len(out)}")
    return out[0]


def ensure_read_only(sql: str, dialect: str = SOURCE_DIALECT) -> exp.Expression:
    """Parse SQL and reject anything other than a single SELECT. Returns the parsed tree."""
    try:
        statements = [s for s in sqlglot.parse(sql, read=resolve_dialect(dialect)) if s is not None]
    except ParseError as e:
        raise UnsafeQueryError(f"SQL could not be parsed: {e}") from e
    if len(statements) != 1:
        raise UnsafeQueryError("Only a single statement is allowed")
    tree = statements[0]
    if not isinstance(tree, (exp.Select, exp.Union, exp.Subquery)) and not tree.find(exp.Select):
        raise UnsafeQueryError("Only SELECT queries are allowed")
    if any(tree.find(node) for node in WRITE_NODES):
        raise UnsafeQueryError("Queries that change data are not allowed")
    return tree


@dataclass
class SQLAnalysis:
    parse_error: Optional[str] = None
    is_read_only: bool = True
    tables: List[str] = field(default_factory=list)


def analyze(sql: str, dialect: str = SOURCE_DIALECT) -> SQLAnalysis:
    """Parse SQL for validation: syntax errors, write operations, and tables used."""
    result = SQLAnalysis()
    try:
        tree = sqlglot.parse_one(sql, read=resolve_dialect(dialect) or None)
    except ParseError as e:
        result.parse_error = str(e).splitlines()[0]
        result.is_read_only = False
        return result
    result.is_read_only = not any(tree.find(node) for node in WRITE_NODES)
    result.tables = sorted({".".join(p for p in (t.db, t.name) if p) for t in tree.find_all(exp.Table)})
    return result


# ---------------------------------------------------------------------------
# SQL metric -> DAX measure (for Power BI)
# ---------------------------------------------------------------------------

def metric_to_dax(metric: dict) -> Optional[str]:
    """Convert a simple SQL metric into a DAX measure expression.

    Handles COUNT(*), COUNT(col), COUNT(DISTINCT col), SUM, AVG, MIN, and MAX,
    with filters made of `column = literal` conditions joined by AND.
    Returns None for anything more complex; set `dax_measure` in config instead.
    """
    table = metric["table"].split(".")[-1]
    try:
        agg = sqlglot.parse_one(metric["sql_template"], read=SOURCE_DIALECT)
    except ParseError:
        return None

    def col(c: exp.Column) -> str:
        return f"'{table}'[{c.name}]"

    if isinstance(agg, exp.Count):
        arg = agg.this
        if isinstance(arg, exp.Star):
            base = f"COUNTROWS('{table}')"
        elif isinstance(arg, exp.Distinct) and len(arg.expressions) == 1 and isinstance(arg.expressions[0], exp.Column):
            base = f"DISTINCTCOUNT({col(arg.expressions[0])})"
        elif isinstance(arg, exp.Column):
            base = f"COUNT({col(arg)})"
        else:
            return None
    elif isinstance(agg, (exp.Sum, exp.Avg, exp.Min, exp.Max)) and isinstance(agg.this, exp.Column):
        fn = {exp.Sum: "SUM", exp.Avg: "AVERAGE", exp.Min: "MIN", exp.Max: "MAX"}[type(agg)]
        base = f"{fn}({col(agg.this)})"
    else:
        return None

    flt = (metric.get("filter") or "").strip()
    if not flt:
        return base
    try:
        cond = sqlglot.parse_one(flt, read=SOURCE_DIALECT)
    except ParseError:
        return None

    parts: List[str] = []
    for c in _flatten_and(cond):
        if not (isinstance(c, exp.EQ) and isinstance(c.this, exp.Column)):
            return None
        value = c.expression
        if isinstance(value, exp.Literal):
            literal = f'"{value.this}"' if value.is_string else value.this
        elif isinstance(value, exp.Boolean):
            literal = "TRUE()" if value.this else "FALSE()"
        else:
            return None
        parts.append(f"{col(c.this)} = {literal}")
    return f"CALCULATE({base}, {', '.join(parts)})"


def _flatten_and(node: exp.Expression) -> List[exp.Expression]:
    if isinstance(node, exp.Paren):
        return _flatten_and(node.this)
    if isinstance(node, exp.And):
        return _flatten_and(node.this) + _flatten_and(node.expression)
    return [node]
