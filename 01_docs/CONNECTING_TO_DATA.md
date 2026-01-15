# Connecting to Your Real Data

Complete guide to connecting the AI-Assisted Insights Agent to your actual data sources.

---

## Overview

By default, the agent uses **simulated data** for demonstrations. To connect to your real data, you'll need to:

1. Choose your data source type
2. Install the required database driver
3. Configure your connection details
4. Update your metrics to match your schema
5. Test the connection

**Estimated time:** 15-30 minutes depending on your data source

---

## Table of Contents

- [Option 1: SQL Server / Azure SQL Database](#option-1-sql-server--azure-sql-database)
- [Option 2: PostgreSQL](#option-2-postgresql)
- [Option 3: MySQL / MariaDB](#option-3-mysql--mariadb)
- [Option 4: Snowflake](#option-4-snowflake)
- [Option 5: Google BigQuery](#option-5-google-bigquery)
- [Option 6: Databricks](#option-6-databricks)
- [Option 7: Excel / CSV Files](#option-7-excel--csv-files)
- [Option 8: Local SQLite Database](#option-8-local-sqlite-database)
- [Option 9: Azure Synapse Analytics](#option-9-azure-synapse-analytics)
- [Option 10: Microsoft Fabric](#option-10-microsoft-fabric)
- [Troubleshooting](#troubleshooting)

---

## Option 1: SQL Server / Azure SQL Database

Perfect for Microsoft environments, Azure SQL Database, or on-premises SQL Server.

### Step 1: Install Database Driver

```powershell
pip install pyodbc
```

### Step 2: Get Your Connection Details

**For Azure SQL Database:**
- Server: `your-server.database.windows.net`
- Database: `your-database`
- Username: `your-username`
- Password: `your-password`

**For Local SQL Server:**
- Server: `localhost` or `YOUR-COMPUTER-NAME`
- Database: `your-database`
- Authentication: Windows or SQL Server

### Step 3: Create Connection Configuration

Edit `config.yaml` and update the data sources section:

```yaml
data_sources:
  primary:
    type: sqlserver
    connection:
      server: your-server.database.windows.net
      database: your-database
      username: ${SQLSERVER_USER}  # From environment variable
      password: ${SQLSERVER_PASSWORD}  # From environment variable
      driver: "ODBC Driver 18 for SQL Server"
      encrypt: true
      trust_server_certificate: false
```

### Step 4: Set Environment Variables

**Windows PowerShell:**
```powershell
$env:SQLSERVER_USER = "your-username"
$env:SQLSERVER_PASSWORD = "your-password"
```

**Or create a `.env` file:**
```
SQLSERVER_USER=your-username
SQLSERVER_PASSWORD=your-password
```

### Step 5: Update Your Metrics

Edit the `metrics` section in `config.yaml` to match your actual tables:

```yaml
metrics:
  total_customers:
    name: Total Customers
    description: Total number of active customers
    sql_template: COUNT(DISTINCT customer_id)
    table: dbo.Customers
    filter: status = 'active'
    unit: customers
```

### Step 6: Test Connection

```python
import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=your-server.database.windows.net;"
    "DATABASE=your-database;"
    "UID=your-username;"
    "PWD=your-password;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute("SELECT TOP 5 * FROM INFORMATION_SCHEMA.TABLES")
for row in cursor:
    print(row)
conn.close()
```

---

## Option 2: PostgreSQL

Great for open-source projects, Heroku, or AWS RDS PostgreSQL.

### Step 1: Install Database Driver

```powershell
pip install psycopg2-binary
```

### Step 2: Get Your Connection Details

- Host: `your-host.postgres.database.azure.com` or `localhost`
- Port: `5432` (default)
- Database: `your-database`
- Username: `your-username`
- Password: `your-password`

### Step 3: Create Connection Configuration

Edit `config.yaml`:

```yaml
data_sources:
  primary:
    type: postgresql
    connection:
      host: your-host.postgres.database.azure.com
      port: 5432
      database: your-database
      username: ${POSTGRES_USER}
      password: ${POSTGRES_PASSWORD}
      sslmode: require
```

### Step 4: Set Environment Variables

```powershell
$env:POSTGRES_USER = "your-username"
$env:POSTGRES_PASSWORD = "your-password"
```

### Step 5: Update Metrics for PostgreSQL Schema

```yaml
metrics:
  total_users:
    name: Total Users
    description: Active user count
    sql_template: COUNT(DISTINCT user_id)
    table: public.users
    filter: status = 'active'
    unit: users
```

### Step 6: Test Connection

```python
import psycopg2

conn = psycopg2.connect(
    host="your-host.postgres.database.azure.com",
    port=5432,
    database="your-database",
    user="your-username",
    password="your-password",
    sslmode="require"
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
conn.close()
```

---

## Option 3: MySQL / MariaDB

Popular for web applications, WordPress, and LAMP stacks.

### Step 1: Install Database Driver

```powershell
pip install mysql-connector-python
```

### Step 2: Get Your Connection Details

- Host: `your-host.mysql.database.azure.com` or `localhost`
- Port: `3306` (default)
- Database: `your-database`
- Username: `your-username`
- Password: `your-password`

### Step 3: Create Connection Configuration

Edit `config.yaml`:

```yaml
data_sources:
  primary:
    type: mysql
    connection:
      host: your-host.mysql.database.azure.com
      port: 3306
      database: your-database
      username: ${MYSQL_USER}
      password: ${MYSQL_PASSWORD}
      ssl_ca: /path/to/ca-cert.pem  # For Azure MySQL
```

### Step 4: Set Environment Variables

```powershell
$env:MYSQL_USER = "your-username"
$env:MYSQL_PASSWORD = "your-password"
```

### Step 5: Update Metrics

```yaml
metrics:
  total_orders:
    name: Total Orders
    description: Count of all orders
    sql_template: COUNT(DISTINCT order_id)
    table: orders
    filter: status = 'completed'
    unit: orders
```

### Step 6: Test Connection

```python
import mysql.connector

conn = mysql.connector.connect(
    host="your-host.mysql.database.azure.com",
    port=3306,
    database="your-database",
    user="your-username",
    password="your-password",
    ssl_ca="/path/to/ca-cert.pem"
)

cursor = conn.cursor()
cursor.execute("SELECT DATABASE();")
print(cursor.fetchone())
conn.close()
```

---

## Option 4: Snowflake

Enterprise data warehouse for large-scale analytics.

### Step 1: Install Snowflake Connector

```powershell
pip install snowflake-connector-python
```

### Step 2: Get Your Connection Details

- Account: `your-account.snowflakecomputing.com`
- User: `your-username`
- Password: `your-password`
- Warehouse: `COMPUTE_WH`
- Database: `your-database`
- Schema: `PUBLIC`
- Role: `ACCOUNTADMIN` or your role

### Step 3: Create Connection Configuration

Edit `config.yaml`:

```yaml
data_sources:
  primary:
    type: snowflake
    connection:
      account: your-account
      user: ${SNOWFLAKE_USER}
      password: ${SNOWFLAKE_PASSWORD}
      warehouse: COMPUTE_WH
      database: your-database
      schema: PUBLIC
      role: ACCOUNTADMIN
```

### Step 4: Set Environment Variables

```powershell
$env:SNOWFLAKE_USER = "your-username"
$env:SNOWFLAKE_PASSWORD = "your-password"
```

### Step 5: Update Metrics for Snowflake

```yaml
metrics:
  daily_revenue:
    name: Daily Revenue
    description: Sum of revenue by day
    sql_template: SUM(amount)
    table: ANALYTICS.PUBLIC.TRANSACTIONS
    filter: status = 'completed'
    unit: dollars
```

### Step 6: Test Connection

```python
import snowflake.connector

conn = snowflake.connector.connect(
    account='your-account',
    user='your-username',
    password='your-password',
    warehouse='COMPUTE_WH',
    database='your-database',
    schema='PUBLIC'
)

cursor = conn.cursor()
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())
conn.close()
```

---

## Option 5: Google BigQuery

Google Cloud's serverless data warehouse.

### Step 1: Install BigQuery Client

```powershell
pip install google-cloud-bigquery
```

### Step 2: Set Up Authentication

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a service account
3. Download JSON key file
4. Set environment variable:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\your-service-account-key.json"
```

### Step 3: Create Connection Configuration

Edit `config.yaml`:

```yaml
data_sources:
  primary:
    type: bigquery
    connection:
      project_id: your-project-id
      dataset: your-dataset
      credentials_path: ${GOOGLE_APPLICATION_CREDENTIALS}
```

### Step 4: Update Metrics for BigQuery

```yaml
metrics:
  page_views:
    name: Page Views
    description: Total page view count
    sql_template: COUNT(*)
    table: your-project.analytics.page_views
    filter: ""
    unit: views
```

### Step 5: Test Connection

```python
from google.cloud import bigquery

client = bigquery.Client(project='your-project-id')

query = "SELECT COUNT(*) as total FROM `your-project.your-dataset.your-table`"
results = client.query(query)

for row in results:
    print(f"Total rows: {row.total}")
```

---

## Option 6: Databricks

Unified analytics platform built on Apache Spark.

### Step 1: Install Databricks SQL Connector

```powershell
pip install databricks-sql-connector
```

### Step 2: Get Your Connection Details

1. Go to your Databricks workspace
2. Click "Compute" → Select your cluster
3. Go to "Advanced Options" → "JDBC/ODBC"
4. Note:
   - Server hostname: `your-workspace.cloud.databricks.com`
   - HTTP path: `/sql/1.0/warehouses/xxxxx`
   - Access token: Generate from User Settings

### Step 3: Create Connection Configuration

Edit `config.yaml`:

```yaml
data_sources:
  primary:
    type: databricks
    connection:
      server_hostname: your-workspace.cloud.databricks.com
      http_path: /sql/1.0/warehouses/xxxxx
      access_token: ${DATABRICKS_TOKEN}
```

### Step 4: Set Environment Variable

```powershell
$env:DATABRICKS_TOKEN = "your-access-token"
```

### Step 5: Update Metrics

```yaml
metrics:
  active_users:
    name: Active Users
    description: Distinct active user count
    sql_template: COUNT(DISTINCT user_id)
    table: default.users
    filter: is_active = true
    unit: users
```

### Step 6: Test Connection

```python
from databricks import sql

conn = sql.connect(
    server_hostname='your-workspace.cloud.databricks.com',
    http_path='/sql/1.0/warehouses/xxxxx',
    access_token='your-access-token'
)

cursor = conn.cursor()
cursor.execute("SELECT current_database()")
print(cursor.fetchone())
conn.close()
```

---

## Option 7: Excel / CSV Files

Perfect for quick analysis of local files without database setup.

### Step 1: Install Pandas

```powershell
pip install pandas openpyxl
```

### Step 2: Organize Your Files

Create a data directory:
```
C:\Users\YourName\Projects\ai-assisted-insights-agent\data\
  ├── customers.csv
  ├── orders.csv
  └── products.xlsx
```

### Step 3: Create Connection Configuration

Edit `config.yaml`:

```yaml
data_sources:
  primary:
    type: csv
    connection:
      data_directory: C:\Users\YourName\Projects\ai-assisted-insights-agent\data
      file_format: csv  # or 'excel'
```

### Step 4: Update Metrics for File-Based Data

```yaml
metrics:
  total_customers:
    name: Total Customers
    description: Count of customers
    sql_template: COUNT(*)
    table: customers  # This will read customers.csv
    filter: ""
    unit: customers
```

### Step 5: Create Data Connector Module

Create `insights_agent/connectors/csv_connector.py`:

```python
import pandas as pd
import os

class CSVConnector:
    def __init__(self, data_directory):
        self.data_directory = data_directory
    
    def execute_query(self, table_name, query=None):
        """Load CSV/Excel file and execute pandas query"""
        # Try CSV first
        csv_path = os.path.join(self.data_directory, f"{table_name}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            # Try Excel
            xlsx_path = os.path.join(self.data_directory, f"{table_name}.xlsx")
            if os.path.exists(xlsx_path):
                df = pd.read_excel(xlsx_path)
            else:
                raise FileNotFoundError(f"No file found for table: {table_name}")
        
        # Execute pandas query if provided
        if query:
            df = df.query(query)
        
        return df
```

### Step 6: Test File Access

```python
import pandas as pd

# Read CSV
df = pd.read_csv('03_data/customers.csv')
print(df.head())
print(f"Total rows: {len(df)}")

# Read Excel
df_excel = pd.read_excel('03_data/products.xlsx')
print(df_excel.head())
```

---

## Option 8: Local SQLite Database

Lightweight, serverless database - perfect for development and testing.

### Step 1: SQLite is Built-in (No Installation Needed!)

Python includes SQLite support by default.

### Step 2: Create Your Database

```python
import sqlite3

# Connect (creates file if doesn't exist)
conn = sqlite3.connect('insights.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    signup_date DATE,
    status TEXT
)
''')

# Insert sample data
cursor.execute('''
INSERT INTO customers (name, email, signup_date, status)
VALUES ('John Doe', 'john@example.com', '2025-01-01', 'active')
''')

conn.commit()
conn.close()
```

### Step 3: Create Connection Configuration

Edit `config.yaml`:

```yaml
data_sources:
  primary:
    type: sqlite
    connection:
      database_path: C:\Users\YourName\Projects\ai-assisted-insights-agent\insights.db
```

### Step 4: Update Metrics

```yaml
metrics:
  total_customers:
    name: Total Customers
    description: Active customer count
    sql_template: COUNT(DISTINCT customer_id)
    table: customers
    filter: status = 'active'
    unit: customers
```

### Step 5: Test Connection

```python
import sqlite3

conn = sqlite3.connect('insights.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM customers LIMIT 5")
for row in cursor.fetchall():
    print(row)

conn.close()
```

---

## Option 9: Azure Synapse Analytics

Enterprise-scale analytics service.

### Step 1: Install Driver

```powershell
pip install pyodbc
```

### Step 2: Get Connection Details

- Server: `your-workspace-name.sql.azuresynapse.net`
- Database: `your-sql-pool`
- Username: `your-username`
- Password: `your-password`

### Step 3: Create Connection Configuration

Edit `config.yaml`:

```yaml
data_sources:
  primary:
    type: synapse
    connection:
      server: your-workspace-name.sql.azuresynapse.net
      database: your-sql-pool
      username: ${SYNAPSE_USER}
      password: ${SYNAPSE_PASSWORD}
      driver: "ODBC Driver 18 for SQL Server"
      encrypt: true
```

### Step 4: Set Environment Variables

```powershell
$env:SYNAPSE_USER = "your-username"
$env:SYNAPSE_PASSWORD = "your-password"
```

### Step 5: Test Connection

```python
import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=your-workspace-name.sql.azuresynapse.net;"
    "DATABASE=your-sql-pool;"
    "UID=your-username;"
    "PWD=your-password;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")
print(cursor.fetchone())
conn.close()
```

---

## Option 10: Microsoft Fabric

Microsoft's unified analytics platform.

### Step 1: Install Required Packages

```powershell
pip install pyodbc azure-identity
```

### Step 2: Get Fabric Connection Details

1. Go to your Fabric workspace
2. Open your Lakehouse
3. Click "SQL analytics endpoint"
4. Copy connection details

### Step 3: Configure with Azure AD Authentication

Edit `config.yaml`:

```yaml
data_sources:
  primary:
    type: fabric
    connection:
      server: your-workspace.datawarehouse.fabric.microsoft.com
      database: your-lakehouse
      authentication: azure_ad_interactive  # or azure_ad_service_principal
```

### Step 4: Test Connection

```python
from azure.identity import DefaultAzureCredential
import pyodbc

credential = DefaultAzureCredential()
token = credential.get_token("https://database.windows.net/.default")

conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=your-workspace.datawarehouse.fabric.microsoft.com;"
    "DATABASE=your-lakehouse;"
    f"AccessToken={token.token};"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute("SELECT TOP 5 * FROM INFORMATION_SCHEMA.TABLES")
for row in cursor:
    print(row)
conn.close()
```

---

## General Configuration Tips

### 1. Keep Credentials Secure

**Never commit passwords to Git!** Use environment variables or `.env` files:

Create `.env` file:
```
DB_USER=your-username
DB_PASSWORD=your-password
DB_HOST=your-host
```

Load in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
```

### 2. Use Connection Pooling

For production, implement connection pooling:

```yaml
data_sources:
  primary:
    type: postgresql
    connection:
      # ... connection details ...
      pool_size: 5
      max_overflow: 10
      pool_timeout: 30
```

### 3. Configure Read Replicas

For high-traffic scenarios:

```yaml
data_sources:
  primary:
    type: postgresql
    connection:
      host: primary-server.com
      # ... other settings ...
  
  read_replica:
    type: postgresql
    connection:
      host: read-replica.com
      # ... other settings ...
```

### 4. Set Query Timeouts

Prevent long-running queries:

```yaml
query_settings:
  timeout_seconds: 30
  max_rows: 10000
  enable_query_cache: true
  cache_ttl_seconds: 300
```

---

## Updating Metrics for Your Data

After connecting to your database, update the metrics in `config.yaml` to match your schema:

### Step 1: Discover Your Tables

```sql
-- SQL Server / Azure SQL
SELECT TABLE_SCHEMA, TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'

-- PostgreSQL
SELECT schemaname, tablename 
FROM pg_tables 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')

-- MySQL
SHOW TABLES
```

### Step 2: Discover Your Columns

```sql
-- SQL Server / Azure SQL / PostgreSQL
SELECT COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'your_table'

-- MySQL
DESCRIBE your_table
```

### Step 3: Create Custom Metrics

Example for an e-commerce database:

```yaml
metrics:
  total_orders:
    name: Total Orders
    description: Count of all completed orders
    sql_template: COUNT(DISTINCT order_id)
    table: sales.orders
    filter: status = 'completed'
    unit: orders
    
  total_revenue:
    name: Total Revenue
    description: Sum of all order amounts
    sql_template: SUM(order_total)
    table: sales.orders
    filter: status = 'completed' AND payment_status = 'paid'
    unit: dollars
    
  average_order_value:
    name: Average Order Value (AOV)
    description: Average order amount
    sql_template: AVG(order_total)
    table: sales.orders
    filter: status = 'completed'
    unit: dollars
    
  conversion_rate:
    name: Conversion Rate
    description: Percentage of sessions that resulted in purchase
    sql_template: COUNT(DISTINCT order_id) * 100.0 / (SELECT COUNT(DISTINCT session_id) FROM analytics.sessions)
    table: sales.orders
    filter: ""
    unit: percent
    
  customer_lifetime_value:
    name: Customer LTV
    description: Average total revenue per customer
    sql_template: SUM(order_total) / COUNT(DISTINCT customer_id)
    table: sales.orders
    filter: status = 'completed'
    unit: dollars
```

---

## Troubleshooting

### Connection Timeout Errors

**Problem:** `Connection timeout` or `Unable to connect`

**Solutions:**
1. Check firewall rules allow your IP
2. Verify server/host address is correct
3. Test with ping or telnet:
   ```powershell
   Test-NetConnection -ComputerName your-server.com -Port 1433
   ```
4. For Azure SQL, add your IP to firewall in Azure Portal

### Authentication Failures

**Problem:** `Login failed` or `Authentication failed`

**Solutions:**
1. Verify username and password
2. Check user has correct permissions:
   ```sql
   -- Grant read access
   GRANT SELECT ON DATABASE::your_database TO your_user;
   ```
3. For Azure SQL, use full username: `username@servername`
4. Verify MFA/conditional access isn't blocking

### Driver Not Found

**Problem:** `Driver not found` or `ODBC Driver not available`

**Solutions:**
1. Install ODBC Driver:
   - Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   - For Linux: `apt-get install unixodbc-dev`
2. List available drivers:
   ```python
   import pyodbc
   print(pyodbc.drivers())
   ```
3. Update driver name in config to match installed driver

### SSL/TLS Errors

**Problem:** `SSL certificate validation failed`

**Solutions:**
1. For development, disable SSL verification:
   ```yaml
   connection:
     trust_server_certificate: true
   ```
2. For production, install proper CA certificate
3. For Azure services, download CA cert from Azure Portal

### Query Performance Issues

**Problem:** Queries are slow

**Solutions:**
1. Add indexes to frequently queried columns
2. Reduce query timeout if needed
3. Add `LIMIT` clauses to queries
4. Use read replicas for reporting
5. Consider caching results:
   ```yaml
   query_settings:
     enable_query_cache: true
     cache_ttl_seconds: 300
   ```

### Permission Denied Errors

**Problem:** `Permission denied on table`

**Solutions:**
1. Grant SELECT permission:
   ```sql
   GRANT SELECT ON schema.table TO username;
   ```
2. For all tables in schema:
   ```sql
   GRANT SELECT ON SCHEMA::schema_name TO username;
   ```
3. Verify user role has read access

---

## Testing Your Connection

After configuration, run this test script:

```python
"""Test database connection"""
import sys
sys.path.insert(0, '.')

from insights_agent.config import Config

# Load config
config = Config()

print("=" * 70)
print("Database Connection Test")
print("=" * 70)

# Show configuration
print(f"\nData Source Type: {config.get('data_sources.primary.type')}")
print(f"Connection Details: {config.get('data_sources.primary.connection')}")

# Test metrics loaded
metrics = config.get_metrics()
print(f"\nLoaded {len(metrics)} metrics:")
for metric_id, metric in list(metrics.items())[:5]:
    print(f"  • {metric['name']}: {metric['description']}")

print("\n✅ Configuration loaded successfully!")
print("\nNext steps:")
print("1. Test a simple query")
print("2. Verify table access")
print("3. Run the agent CLI or Python examples")
print("=" * 70)
```

Save as `test_connection.py` and run:
```powershell
python test_connection.py
```

---

## Next Steps

Once connected:

1. **Test with CLI:**
   ```powershell
   python -m insights_agent.cli
   ```
   Then try: `ask What are total customers?`

2. **Query via Python:**
   ```python
   from insights_agent.server import ask_question
   result = ask_question("What is our revenue this month?", "this month")
   print(result)
   ```

3. **Build dashboards** using your queries

4. **Schedule reports** with task scheduler

5. **Integrate with other tools** (Power BI, Excel, etc.)

---

## Security Best Practices

✅ **Always:**
- Use environment variables for credentials
- Use read-only database users
- Enable SSL/TLS encryption
- Implement query timeouts
- Log all queries for audit
- Use service accounts, not personal accounts
- Rotate credentials regularly

❌ **Never:**
- Commit passwords to Git
- Use admin/root accounts
- Disable SSL in production
- Allow public internet access without firewall
- Share credentials in chat/email

---

## Getting Help

**Issues with specific databases:**
- SQL Server: https://learn.microsoft.com/sql
- PostgreSQL: https://www.postgresql.org/docs/
- MySQL: https://dev.mysql.com/doc/
- Snowflake: https://docs.snowflake.com
- BigQuery: https://cloud.google.com/bigquery/docs
- Databricks: https://docs.databricks.com

**General Python database libraries:**
- pyodbc: https://github.com/mkleehammer/pyodbc/wiki
- psycopg2: https://www.psycopg.org/docs/
- mysql-connector: https://dev.mysql.com/doc/connector-python/

**Need more help?**
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [API.md](API.md) for function reference
- See [02_examples/](../02_examples/) for code samples

---

*Last updated: January 3, 2026*
