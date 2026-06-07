from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from ccai.timetravelserver.persistence.models import ServerConfiguration

CONFIG_SCHEMA = {
    "listen_address": {"type": str, "default": "0.0.0.0"},
    "listen_port": {"type": int, "default": 8080},
    "tls_enabled": {"type": bool, "default": False},
    "data_retention_days": {"type": int, "default": 30},
    "max_concurrent_connections": {"type": int, "default": 100},
    "default_trace_granularity": {"type": str, "default": "function"},
    "heartbeat_timeout_seconds": {"type": int, "default": 30},
}

class ServerConfigStore:
    def __init__(self, session: Session):
        self._session = session

    def _cast_value(self, key: str, value_str: str) -> Any:
        expected_type = CONFIG_SCHEMA[key]["type"]
        if expected_type == bool:
            return value_str.lower() in ("true", "1", "yes")
        elif expected_type == int:
            return int(value_str)
        return value_str

    def validate(self, key: str, value: Any) -> bool:
        """Validates if a key exists and the value matches the expected type."""
        if key not in CONFIG_SCHEMA:
            return False
        expected_type = CONFIG_SCHEMA[key]["type"]
        if not isinstance(value, expected_type):
            return False
        return True

    def get(self, key: str) -> Any:
        """Gets a configuration value by key, returning default if not set."""
        if key not in CONFIG_SCHEMA:
            raise KeyError(f"Unknown configuration key: {key}")

        try:
            config = self._session.query(ServerConfiguration).filter_by(key=key).one()
            return self._cast_value(key, config.value)
        except NoResultFound:
            return CONFIG_SCHEMA[key]["default"]

    def set(self, key: str, value: Any) -> bool:
        """Sets a configuration value, validating key and type."""
        if not self.validate(key, value):
            return False

        value_str = str(value)

        try:
            config = self._session.query(ServerConfiguration).filter_by(key=key).one()
            config.value = value_str
        except NoResultFound:
            config = ServerConfiguration(key=key, value=value_str)
            self._session.add(config)

        self._session.commit()
        return True

    def get_all(self) -> Dict[str, Any]:
        """Gets all configuration values, merging DB overrides with defaults."""
        configs_db = {c.key: self._cast_value(c.key, c.value) for c in self._session.query(ServerConfiguration).all()}

        result = {}
        for key, schema in CONFIG_SCHEMA.items():
            result[key] = configs_db.get(key, schema["default"])

        return result
