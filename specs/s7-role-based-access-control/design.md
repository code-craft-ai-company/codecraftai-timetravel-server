# S7.3 — Role-Based Access Control: Design

## Module: `auth/rbac.py`

### Role Decorator
```python
def require_role(*roles):
    """Decorator that checks the authenticated user has one of the specified roles."""
```

### Role Hierarchy
- `admin` > `operator` > `viewer`
- Higher roles inherit lower role permissions.

### Dependencies
- S7.1/S7.2 (authentication — provides the user context for role checking)
