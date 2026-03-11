# S8.6 — Configuration File and Environment Variable Support: Design

## Module: `ops/config_loader.py`

### Class: ConfigLoader
```python
class ConfigLoader:
    def __init__(self, config_path: Optional[str] = None):
        ...
    def load(self) -> Dict[str, Any]:
        """Load config with precedence: env vars > file > defaults."""
    def validate(self, config: Dict[str, Any]) -> None:
        """Validate all config values. Raise SystemExit on error."""
```

### Environment Variable Mapping
- `TIMETRAVEL_{KEY_UPPER}` → config key (lowercase, underscore to underscore).
- Example: `TIMETRAVEL_LISTEN_PORT` → `listen_port`.

### File Format
- YAML (primary) or TOML.
- Read with `pyyaml` or `tomllib` (Python 3.11+).

### Dependencies
- S0.3 (CONFIG_SCHEMA for validation and defaults)
