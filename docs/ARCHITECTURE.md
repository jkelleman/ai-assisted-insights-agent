# Architecture

Overview of the AI-Assisted Insights Agent architecture.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Client Layer                        │
│            (Claude Desktop, Custom Clients, etc.)           │
└────────────────────────────┬────────────────────────────────┘
                             │ MCP Protocol (stdio)
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    FastMCP Server                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  MCP Tools Layer                     │   │
│  │  • ask_question        • validate_query              │   │
│  │  • generate_query      • explain_result              │   │
│  │  • suggest_followups   • compare_metrics             │   │
│  │  • save_query_template • check_data_quality          │   │
│  └──────────────────────────────────────────────────────┘   │
│                             │                                │
│  ┌──────────────────────────▼──────────────────────────┐   │
│  │              Business Logic Layer                    │   │
│  │  • Question Parsing                                  │   │
│  │  • Query Generation                                  │   │
│  │  • Query Validation                                  │   │
│  │  • Result Explanation                                │   │
│  │  • Data Quality Assessment                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                             │                                │
│  ┌──────────────────────────▼──────────────────────────┐   │
│  │            Configuration & Storage Layer             │   │
│  │  • Config (config.py)                                │   │
│  │  • QueryHistory (history.py)                         │   │
│  │  • Metric Definitions                                │   │
│  │  • Business Glossary                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                  Persistent Storage                         │
│              (SQLite, config.yaml)                          │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. MCP Client Layer

**Purpose:** Interface for users to interact with the agent

**Supported Clients:**
- Claude Desktop (via MCP protocol)
- Custom Python clients
- CLI tool (insights_agent.cli)
- Jupyter notebooks

**Communication:**
- Protocol: MCP (Model Context Protocol)
- Transport: stdio (standard input/output)
- Format: JSON-RPC

### 2. FastMCP Server

**Purpose:** Core server implementing MCP protocol

**Key Components:**
- Tool registration and dispatch
- Prompt registration
- Request/response handling
- Error handling and validation

**File:** `insights_agent/server.py`

### 3. MCP Tools Layer

**Purpose:** Expose functionality as MCP tools

**Tools:**
- `ask_question` - Natural language query processing
- `generate_query` - Structured SQL generation
- `validate_query` - Query validation
- `explain_result` - Result interpretation
- `suggest_followups` - Follow-up suggestions
- `save_query_template` - Template management
- `list_templates` - Template listing
- `check_data_quality` - Quality assessment
- `compare_metrics` - Metric comparison

**Prompts:**
- `insights_query_guide` - Usage guide

### 4. Business Logic Layer

**Purpose:** Core functionality for query processing

**Key Functions:**

#### Question Parsing
- Extract metrics from natural language
- Identify time periods
- Map business terms to technical terms
- Intent detection

#### Query Generation
- Convert parsed questions to SQL
- Apply metric definitions
- Add filters and time constraints
- Handle GROUP BY clauses

#### Query Validation
- Syntax checking
- Performance analysis
- Best practices validation
- Security checks

#### Result Explanation
- Historical context
- Statistical analysis
- Interpretation
- Recommended actions

#### Data Quality Assessment
- Freshness checks
- Completeness validation
- Anomaly detection
- Quality scoring

### 5. Configuration & Storage Layer

**Purpose:** Manage configuration and persistent data

**Components:**

#### Config (config.py)
- Load configuration from YAML/JSON
- Manage metric definitions
- Handle data source configurations
- Business glossary management

#### QueryHistory (history.py)
- SQLite-based persistence
- Query history tracking
- Template management
- Statistics and analytics
- Export functionality

#### In-Memory Stores
- `METRIC_DEFINITIONS` - Available metrics
- `BUSINESS_GLOSSARY` - Term mappings
- `QUERY_HISTORY` - Recent queries (also persisted)
- `QUERY_TEMPLATES` - Saved templates (also persisted)

### 6. Persistent Storage

**Purpose:** Long-term data storage

**Databases:**

#### SQLite (insights_agent.db)
- Query history
- Query templates
- Execution statistics

**Tables:**
```sql
query_history (
    id, question, time_period, sql_query,
    result_value, metric_id, timestamp,
    execution_time_ms, data_quality_score
)

query_templates (
    id, template_id, name, sql_query,
    description, created_at, updated_at,
    run_count, tags
)
```

#### Configuration Files
- `config.yaml` - Main configuration
- Custom metric definitions
- Data source configurations

## Data Flow

### Example: Ask Question Flow

```
1. User asks question in Claude
   "How many active users last week?"
   
2. Claude calls ask_question tool via MCP
   {
     "tool": "ask_question",
     "arguments": {
       "question": "How many active users last week?",
       "time_period": "last 7 days"
     }
   }

3. Server receives request
   ↓
4. Parse question
   → Identify metric: "active_users"
   → Extract time period: "last 7 days"
   
5. Generate SQL query
   → Get metric definition
   → Apply time filter
   → Build SQL: "SELECT COUNT(DISTINCT user_id) FROM ..."
   
6. Simulate execution (or execute against real DB)
   → Result: 12470
   
7. Assess data quality
   → Check freshness
   → Check completeness
   → Check for anomalies
   
8. Format response
   → Include SQL query
   → Add explanation
   → Add data quality context
   → Suggest follow-ups
   
9. Store in history
   → Save to SQLite
   → Add to in-memory cache
   
10. Return to Claude
    → Formatted response
    
11. Claude presents to user
    → Natural language summary
    → Formatted query and data
```

## Extension Points

### Adding New Metrics

1. Update `config.yaml`:
```yaml
metrics:
  new_metric:
    name: New Metric
    description: What it measures
    sql_template: SQL aggregation
    table: schema.table
    filter: Optional filter
    unit: units
```

2. Reload configuration or restart server

### Adding New Data Sources

1. Update `config.yaml`:
```yaml
data_sources:
  new_source:
    type: postgresql
    host: db.example.com
    port: 5432
    database: analytics
```

2. Implement connection logic in server.py

### Adding New Tools

1. Add tool function in `server.py`:
```python
@mcp.tool()
def new_tool(param: str) -> str:
    """Tool description."""
    # Implementation
    return result
```

2. Update API documentation

### Adding Business Terms

1. Update `config.yaml`:
```yaml
business_glossary:
  new_business_term: technical_term
```

## Security Considerations

### Query Validation
- Syntax validation prevents SQL injection
- Query complexity limits prevent DoS
- Table access controls (future)

### Data Access
- Read-only queries (no INSERT/UPDATE/DELETE)
- Metric definitions control accessible tables
- Data source isolation

### Configuration
- Configuration files should be secured
- Database credentials in environment variables
- Access control on config files

## Performance Considerations

### Caching
- In-memory metric definitions
- Query template caching
- Configuration caching

### Database
- Indexed columns for history queries
- Query result pagination
- Connection pooling (future)

### Optimization
- Lazy loading of history
- Batch operations for exports
- Query validation before execution

## Scalability

### Current Architecture
- Single process
- In-memory + SQLite storage
- Suitable for: Individual users, small teams

### Future Enhancements
- Multi-process support
- PostgreSQL backend
- Query result caching
- Distributed deployment
- API gateway integration
