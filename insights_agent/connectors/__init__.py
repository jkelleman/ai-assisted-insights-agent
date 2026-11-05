"""Data-source connectors. Each one answers metric questions from a real system."""

from __future__ import annotations

from .base import Connector, ConnectorError, QueryResult

SUPPORTED_SOURCES = {
    "sqlite": "Local SQLite file (used by the bundled demo warehouse)",
    "sqlalchemy": "Any SQLAlchemy URL: PostgreSQL, MySQL, Snowflake, and more",
    "fabric": "Microsoft Fabric Warehouse or Lakehouse SQL analytics endpoint",
    "databricks": "Databricks SQL warehouse",
    "powerbi": "Power BI semantic model, queried with DAX",
    "adobe_analytics": "Adobe Analytics report suite, via the 2.0 Reports API",
}


def build_connector(source) -> Connector:
    """Create the connector for a validated data_source config. Imports are lazy,
    so optional drivers are only needed for the source you use."""
    kind = source.type
    if kind == "sqlite":
        from .sql_sources import sqlite_connector
        return sqlite_connector(source.path, source.attach)
    if kind == "sqlalchemy":
        from .sql_sources import url_connector
        return url_connector(source.url, source.dialect)
    if kind == "fabric":
        from .sql_sources import fabric_connector
        return fabric_connector(source.server, source.database, source.odbc_driver)
    if kind == "databricks":
        from .sql_sources import databricks_connector
        return databricks_connector(source.server_hostname, source.http_path, source.access_token_env,
                                    source.catalog, source.schema_)
    if kind == "powerbi":
        from .powerbi import PowerBIConnector
        return PowerBIConnector(source.dataset_id, source.workspace_id, source.date_column)
    if kind == "adobe_analytics":
        from .adobe_analytics import AdobeAnalyticsConnector
        return AdobeAnalyticsConnector.from_env(source.global_company_id, source.report_suite_id,
                                                source.client_id_env, source.client_secret_env)
    raise ConnectorError(f"Unsupported data source type: {kind}")


__all__ = ["Connector", "ConnectorError", "QueryResult", "SUPPORTED_SOURCES", "build_connector"]
