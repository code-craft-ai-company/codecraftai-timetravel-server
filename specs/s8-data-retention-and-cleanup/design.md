# S8.4 — Data Retention and Cleanup: Design

## Module: `ops/retention.py`

### Class: RetentionJob
```python
class RetentionJob:
    def __init__(self, session_factory, storage_backend, config_store):
        ...
    def run(self) -> RetentionResult:
        """Delete expired data. Returns counts of deleted items."""
```

### Scheduling
- Background thread or timer, runs daily by default.

### Dependencies
- S0.3 (data_retention_days), S0.4 (TraceStorageBackend), S0.1 (ORM models)
