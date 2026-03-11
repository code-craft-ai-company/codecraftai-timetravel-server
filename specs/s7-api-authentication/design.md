# S7.2 — API Authentication: Design

## Module: `auth/api_auth.py`

### Authentication Decorator
```python
def require_auth(f):
    """Flask decorator that checks Bearer token, session cookie, or API key."""
```

### Authentication Chain
1. Check `Authorization: Bearer <token>` header → validate against API key store.
2. Check session cookie → validate via UserAuthService.
3. If neither → 401.

### Dependencies
- S7.1 (UserAuthService), S0.2 (CredentialStore for pod tokens distinction)
