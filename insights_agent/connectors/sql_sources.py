"""SQL data sources through SQLAlchemy: SQLite, any SQLAlchemy URL,
Microsoft Fabric, and Databricks.

Each source generates metric SQL with SQLGlot in its own dialect, checks that
the query is read-only, and runs it.
"""

from __future__ import annotations

import os
import struct
import time
from typing import Any, Dict, Optional
from urllib.parse import quote_plus

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine

from .. import sql as sqltools
from ..periods import DateRange
from .base import ConnectorError, QueryResult


class SQLAlchemyConnector:
    """Runs generated metric SQL on any SQLAlchemy engine."""

    def __init__(self, engine: Engine, dialect: str, label: str):
        self.engine = engine
        self.dialect = sqltools.resolve_dialect(dialect)
        self.label = label

    def build_sql(self, metric: dict, period: DateRange, group_by: str = "") -> str:
        return sqltools.build_metric_sql(metric, period, self.dialect, group_by)

    def run_metric(self, metric_id: str, metric: dict, period: DateRange) -> QueryResult:
        query = self.build_sql(metric, period)
        rows = self.run_sql(query)
        value = None
        if rows:
            first = next(iter(rows[0].values()))
            value = float(first) if first is not None else None
        return QueryResult(value=value, query=query, query_language="sql", source=self.label,
                           elapsed_ms=self._last_elapsed_ms, rows=rows)

    def run_sql(self, query: str, max_rows: int = 1000) -> list:
        sqltools.ensure_read_only(query, self.dialect)
        start = time.perf_counter()
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                columns = list(result.keys())
                rows = [dict(zip(columns, row)) for row in result.fetchmany(max_rows)]
        except Exception as e:  # driver errors vary by database
            raise ConnectorError(f"{self.label} query failed: {e.__class__.__name__}: {e}") from e
        finally:
            self._last_elapsed_ms = (time.perf_counter() - start) * 1000
        return rows

    def health_check(self) -> str:
        self.run_sql("SELECT 1 AS ok")
        return f"Connected to {self.label}"

    _last_elapsed_ms = 0.0


def sqlite_connector(path: str, attach: Dict[str, str]) -> SQLAlchemyConnector:
    engine = create_engine(f"sqlite:///{path}")

    @event.listens_for(engine, "connect")
    def _attach_schemas(dbapi_conn, _record):
        for schema, file_path in attach.items():
            dbapi_conn.execute(f"ATTACH DATABASE ? AS {schema}", (file_path,))

    return SQLAlchemyConnector(engine, "sqlite", label=f"SQLite ({os.path.basename(path)})")


def url_connector(url: str, dialect: str) -> SQLAlchemyConnector:
    engine = create_engine(url, pool_pre_ping=True)
    return SQLAlchemyConnector(engine, dialect, label=f"{engine.dialect.name} database")


# Microsoft Fabric ---------------------------------------------------------

SQL_COPT_SS_ACCESS_TOKEN = 1256          # pyodbc connection attribute for an Entra access token
FABRIC_TOKEN_SCOPE = "https://database.windows.net/.default"


def fabric_connector(server: str, database: str, odbc_driver: str,
                     credential: Optional[Any] = None) -> SQLAlchemyConnector:
    """Connect to a Fabric Warehouse or SQL analytics endpoint with Microsoft Entra ID.

    Uses DefaultAzureCredential, so `az login`, a managed identity, or service
    principal environment variables all work. A fresh token is fetched for
    each new connection.
    """
    try:
        import pyodbc  # noqa: F401  (driver must be installed)
    except ImportError as e:
        raise ConnectorError("Fabric needs pyodbc and the Microsoft ODBC driver. "
                             "Install with: pip install 'ai-insights-agent[fabric]'") from e
    if credential is None:
        try:
            from azure.identity import DefaultAzureCredential
        except ImportError as e:
            raise ConnectorError("Fabric needs azure-identity. "
                                 "Install with: pip install 'ai-insights-agent[fabric]'") from e
        credential = DefaultAzureCredential()

    odbc = f"Driver={{{odbc_driver}}};Server={server},1433;Database={database};Encrypt=yes;TrustServerCertificate=no"
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc)}", pool_pre_ping=True)

    @event.listens_for(engine, "do_connect")
    def _provide_token(_dialect, _conn_rec, _cargs, cparams):
        token = credential.get_token(FABRIC_TOKEN_SCOPE).token.encode("utf-16-le")
        cparams["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: struct.pack(f"<I{len(token)}s", len(token), token)}

    return SQLAlchemyConnector(engine, "tsql", label=f"Microsoft Fabric ({database})")


# Databricks ----------------------------------------------------------------

def databricks_connector(server_hostname: str, http_path: str, access_token_env: str,
                         catalog: Optional[str] = None, schema: Optional[str] = None) -> SQLAlchemyConnector:
    """Connect to a Databricks SQL warehouse with a personal access token."""
    token = os.environ.get(access_token_env)
    if not token:
        raise ConnectorError(f"Set {access_token_env} to a Databricks access token")
    try:
        import databricks.sqlalchemy  # noqa: F401  (registers the databricks:// dialect)
    except ImportError as e:
        raise ConnectorError("Databricks needs databricks-sqlalchemy. "
                             "Install with: pip install 'ai-insights-agent[databricks]'") from e
    params = f"http_path={quote_plus(http_path)}"
    if catalog:
        params += f"&catalog={quote_plus(catalog)}"
    if schema:
        params += f"&schema={quote_plus(schema)}"
    engine = create_engine(f"databricks://token:{quote_plus(token)}@{server_hostname}?{params}")
    return SQLAlchemyConnector(engine, "databricks", label=f"Databricks ({server_hostname})")
