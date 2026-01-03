"""
Query history management with persistent storage.
"""
import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path


class QueryHistory:
    """Manage query history with SQLite persistence."""
    
    def __init__(self, db_path: str = "insights_agent.db"):
        """
        Initialize query history storage.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    time_period TEXT NOT NULL,
                    sql_query TEXT NOT NULL,
                    result_value REAL,
                    metric_id TEXT,
                    timestamp TEXT NOT NULL,
                    execution_time_ms INTEGER,
                    data_quality_score INTEGER
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS query_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    sql_query TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    run_count INTEGER DEFAULT 0,
                    tags TEXT
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON query_history(timestamp)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_metric 
                ON query_history(metric_id)
            """)
            
            conn.commit()
    
    def add_query(
        self,
        question: str,
        time_period: str,
        sql_query: str,
        result_value: Optional[float] = None,
        metric_id: Optional[str] = None,
        execution_time_ms: Optional[int] = None,
        data_quality_score: Optional[int] = None
    ) -> int:
        """
        Add a query to history.
        
        Args:
            question: Natural language question
            time_period: Time period used
            sql_query: Generated SQL query
            result_value: Query result value
            metric_id: Metric identifier
            execution_time_ms: Query execution time in milliseconds
            data_quality_score: Data quality score (0-100)
            
        Returns:
            Query ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO query_history 
                (question, time_period, sql_query, result_value, metric_id, 
                 timestamp, execution_time_ms, data_quality_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                question,
                time_period,
                sql_query,
                result_value,
                metric_id,
                datetime.now().isoformat(),
                execution_time_ms,
                data_quality_score
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_history(
        self,
        limit: int = 100,
        metric_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get query history with optional filters.
        
        Args:
            limit: Maximum number of results
            metric_id: Filter by metric ID
            start_date: Filter by start date (ISO format)
            end_date: Filter by end date (ISO format)
            
        Returns:
            List of query history entries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            query = "SELECT * FROM query_history WHERE 1=1"
            params = []
            
            if metric_id:
                query += " AND metric_id = ?"
                params.append(metric_id)
            
            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def search_history(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search query history by question text.
        
        Args:
            search_term: Term to search for
            limit: Maximum results
            
        Returns:
            Matching queries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM query_history 
                WHERE question LIKE ? OR sql_query LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (f"%{search_term}%", f"%{search_term}%", limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get query history statistics.
        
        Returns:
            Statistics dictionary
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Total queries
            total = conn.execute("SELECT COUNT(*) as count FROM query_history").fetchone()["count"]
            
            # Most used metrics
            metrics = conn.execute("""
                SELECT metric_id, COUNT(*) as count 
                FROM query_history 
                WHERE metric_id IS NOT NULL
                GROUP BY metric_id 
                ORDER BY count DESC 
                LIMIT 5
            """).fetchall()
            
            # Average execution time
            avg_time = conn.execute("""
                SELECT AVG(execution_time_ms) as avg_time 
                FROM query_history 
                WHERE execution_time_ms IS NOT NULL
            """).fetchone()["avg_time"]
            
            # Average data quality
            avg_quality = conn.execute("""
                SELECT AVG(data_quality_score) as avg_quality 
                FROM query_history 
                WHERE data_quality_score IS NOT NULL
            """).fetchone()["avg_quality"]
            
            return {
                "total_queries": total,
                "most_used_metrics": [dict(m) for m in metrics],
                "avg_execution_time_ms": avg_time,
                "avg_data_quality_score": avg_quality
            }
    
    def export_history(
        self,
        output_path: str,
        format: str = "json",
        limit: Optional[int] = None
    ) -> None:
        """
        Export query history to file.
        
        Args:
            output_path: Output file path
            format: Export format (json or csv)
            limit: Optional limit on number of entries
        """
        history = self.get_history(limit=limit or 10000)
        
        if format == "json":
            with open(output_path, 'w') as f:
                json.dump(history, f, indent=2)
        
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='') as f:
                if history:
                    writer = csv.DictWriter(f, fieldnames=history[0].keys())
                    writer.writeheader()
                    writer.writerows(history)
    
    def clear_history(self, older_than_days: Optional[int] = None) -> int:
        """
        Clear query history.
        
        Args:
            older_than_days: Only clear entries older than this many days
            
        Returns:
            Number of entries deleted
        """
        with sqlite3.connect(self.db_path) as conn:
            if older_than_days:
                from datetime import timedelta
                cutoff = (datetime.now() - timedelta(days=older_than_days)).isoformat()
                cursor = conn.execute(
                    "DELETE FROM query_history WHERE timestamp < ?",
                    (cutoff,)
                )
            else:
                cursor = conn.execute("DELETE FROM query_history")
            
            conn.commit()
            return cursor.rowcount
    
    # Template Management
    
    def save_template(
        self,
        template_id: str,
        name: str,
        sql_query: str,
        description: str = "",
        tags: Optional[List[str]] = None
    ) -> None:
        """
        Save a query template.
        
        Args:
            template_id: Unique template identifier
            name: Template name
            sql_query: SQL query
            description: Template description
            tags: Optional list of tags
        """
        with sqlite3.connect(self.db_path) as conn:
            now = datetime.now().isoformat()
            conn.execute("""
                INSERT OR REPLACE INTO query_templates 
                (template_id, name, sql_query, description, created_at, updated_at, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                template_id,
                name,
                sql_query,
                description,
                now,
                now,
                json.dumps(tags) if tags else None
            ))
            conn.commit()
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a query template.
        
        Args:
            template_id: Template identifier
            
        Returns:
            Template dictionary or None
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM query_templates WHERE template_id = ?",
                (template_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List all query templates.
        
        Returns:
            List of templates
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM query_templates ORDER BY name"
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_template(self, template_id: str) -> bool:
        """
        Delete a query template.
        
        Args:
            template_id: Template identifier
            
        Returns:
            True if deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM query_templates WHERE template_id = ?",
                (template_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def increment_template_run_count(self, template_id: str) -> None:
        """
        Increment run count for a template.
        
        Args:
            template_id: Template identifier
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE query_templates 
                SET run_count = run_count + 1,
                    updated_at = ?
                WHERE template_id = ?
            """, (datetime.now().isoformat(), template_id))
            conn.commit()
