# S7.6 — Audit Logging: Design

## Module: `security/audit.py`

### Class: AuditLogger
```python
class AuditLogger:
    def __init__(self, session_factory):
        ...
    def log(self, actor: str, action: str, target: str, result: str, details: dict = None) -> None:
    def query(self, time_start=None, time_end=None, actor=None, action=None, offset=0, limit=50) -> List[AuditEntry]:
```

### Dependencies
- S0.1 (AuditLog model)
