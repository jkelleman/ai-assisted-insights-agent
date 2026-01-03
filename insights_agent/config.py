"""
Configuration management for AI-Assisted Insights Agent.
"""
import os
import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration manager for the insights agent."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to configuration file (YAML or JSON)
        """
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
    
    def _find_config_file(self) -> Optional[str]:
        """Find configuration file in standard locations."""
        search_paths = [
            "config.yaml",
            "config.yml",
            "config.json",
            os.path.expanduser("~/.insights-agent/config.yaml"),
            os.path.expanduser("~/.insights-agent/config.yml"),
            "/etc/insights-agent/config.yaml"
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not self.config_path or not os.path.exists(self.config_path):
            return self._default_config()
        
        with open(self.config_path, 'r') as f:
            if self.config_path.endswith('.json'):
                return json.load(f)
            else:
                return yaml.safe_load(f) or {}
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "server": {
                "name": "ai-insights-agent",
                "version": "0.1.0"
            },
            "storage": {
                "type": "sqlite",
                "path": "insights_agent.db"
            },
            "metrics": {},
            "data_sources": {},
            "business_glossary": {}
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'server.name')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get metric definitions from configuration."""
        return self.config.get("metrics", {})
    
    def get_data_sources(self) -> Dict[str, Any]:
        """Get data source configurations."""
        return self.config.get("data_sources", {})
    
    def get_business_glossary(self) -> Dict[str, str]:
        """Get business term mappings."""
        return self.config.get("business_glossary", {})
    
    def save(self, path: Optional[str] = None) -> None:
        """
        Save configuration to file.
        
        Args:
            path: Path to save configuration (uses config_path if not provided)
        """
        save_path = path or self.config_path
        
        if not save_path:
            raise ValueError("No configuration path specified")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w') as f:
            if save_path.endswith('.json'):
                json.dump(self.config, f, indent=2)
            else:
                yaml.safe_dump(self.config, f, default_flow_style=False)
    
    def update(self, key: str, value: Any) -> None:
        """
        Update configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: New value
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def add_metric(self, metric_id: str, metric_def: Dict[str, Any]) -> None:
        """
        Add a metric definition.
        
        Args:
            metric_id: Metric identifier
            metric_def: Metric definition dictionary
        """
        if "metrics" not in self.config:
            self.config["metrics"] = {}
        
        self.config["metrics"][metric_id] = metric_def
    
    def add_data_source(self, source_id: str, source_config: Dict[str, Any]) -> None:
        """
        Add a data source configuration.
        
        Args:
            source_id: Data source identifier
            source_config: Data source configuration
        """
        if "data_sources" not in self.config:
            self.config["data_sources"] = {}
        
        self.config["data_sources"][source_id] = source_config


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Config instance
    """
    return Config(config_path)
