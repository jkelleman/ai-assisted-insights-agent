"""Typed configuration for the insights agent, validated with Pydantic.

A config file declares the metric catalog, the business glossary, one data
source, and optional telemetry. Set INSIGHTS_CONFIG to its path to use it:

    INSIGHTS_CONFIG=06_configs/config.demo.yaml python -m insights_agent.server

Without a config file, the agent keeps its built-in catalog and simulates
query results.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Dict, Literal, Optional, Union

import yaml
from pydantic import BaseModel, ConfigDict, Field

CONFIG_ENV_VAR = "INSIGHTS_CONFIG"


class MetricDefinition(BaseModel):
    """One trusted metric. SQL sources use sql_template, table, and filter.
    API sources use the source-specific fields (dax_measure, adobe_metric)."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    sql_template: str
    table: str
    filter: str = ""
    unit: str = ""
    date_column: str = "event_date"
    # Power BI: name of an existing measure in the semantic model, e.g. "Active Users".
    dax_measure: Optional[str] = None
    # Adobe Analytics: metric id in the report suite, e.g. "metrics/visits".
    adobe_metric: Optional[str] = None


class SQLiteSource(BaseModel):
    """A local SQLite file. Each entry in `attach` is mounted as a schema, so
    tables like analytics.user_events resolve without changing the catalog."""

    type: Literal["sqlite"]
    path: str
    attach: Dict[str, str] = Field(default_factory=dict)


class SQLAlchemySource(BaseModel):
    """Any database with a SQLAlchemy dialect: PostgreSQL, MySQL, Snowflake, and others.
    `url` may reference environment variables, e.g. ${WAREHOUSE_URL}."""

    type: Literal["sqlalchemy"]
    url: str
    dialect: str = Field(description="SQLGlot dialect to generate, e.g. postgres, mysql, snowflake")


class FabricSource(BaseModel):
    """A Microsoft Fabric Warehouse or Lakehouse SQL analytics endpoint, over TDS
    with Microsoft Entra ID authentication."""

    type: Literal["fabric"]
    server: str = Field(description="SQL connection string host, e.g. xxxx.datawarehouse.fabric.microsoft.com")
    database: str
    odbc_driver: str = "ODBC Driver 18 for SQL Server"


class DatabricksSource(BaseModel):
    """A Databricks SQL warehouse."""

    type: Literal["databricks"]
    server_hostname: str
    http_path: str
    access_token_env: str = "DATABRICKS_TOKEN"
    catalog: Optional[str] = None
    schema_: Optional[str] = Field(default=None, alias="schema")


class PowerBISource(BaseModel):
    """A Power BI semantic model, queried with DAX through the executeQueries REST API."""

    type: Literal["powerbi"]
    dataset_id: str
    workspace_id: Optional[str] = None
    date_column: str = Field(default="'Date'[Date]", description="DAX date column for time filters")


class AdobeAnalyticsSource(BaseModel):
    """An Adobe Analytics report suite, queried through the Analytics 2.0 Reports API."""

    type: Literal["adobe_analytics"]
    global_company_id: str
    report_suite_id: str
    client_id_env: str = "ADOBE_CLIENT_ID"
    client_secret_env: str = "ADOBE_CLIENT_SECRET"


DataSource = Annotated[
    Union[SQLiteSource, SQLAlchemySource, FabricSource, DatabricksSource, PowerBISource, AdobeAnalyticsSource],
    Field(discriminator="type"),
]


class DatadogTelemetry(BaseModel):
    """Send query timing and error counts to Datadog. The API key comes from DD_API_KEY."""

    enabled: bool = False
    site: str = "datadoghq.com"
    service: str = "insights-agent"
    api_key_env: str = "DD_API_KEY"


class Telemetry(BaseModel):
    datadog: DatadogTelemetry = Field(default_factory=DatadogTelemetry)


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    metrics: Dict[str, MetricDefinition] = Field(default_factory=dict)
    business_glossary: Dict[str, str] = Field(default_factory=dict)
    data_source: Optional[DataSource] = None
    telemetry: Telemetry = Field(default_factory=Telemetry)


def _expand_env(value):
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_env(v) for v in value]
    return value


def load_config(path: Optional[str] = None) -> Optional[AppConfig]:
    """Load and validate a config file. Returns None when no config is set.

    Relative paths inside the file (like a SQLite path) resolve against the
    file's own folder, so the config works from any working directory.
    """
    path = path or os.environ.get(CONFIG_ENV_VAR)
    if not path:
        return None
    config_path = Path(path).expanduser().resolve()
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    config = AppConfig.model_validate(_expand_env(raw))

    source = config.data_source
    if isinstance(source, SQLiteSource):
        source.path = str(_resolve(config_path.parent, source.path))
        source.attach = {k: str(_resolve(config_path.parent, v)) for k, v in source.attach.items()}
    return config


def _resolve(base: Path, value: str) -> Path:
    p = Path(value).expanduser()
    return p if p.is_absolute() else (base / p).resolve()
