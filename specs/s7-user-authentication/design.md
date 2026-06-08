# S7.1 — User Authentication: Design

## Module Layout
```
source/packages/ccai/timetravelserver/
    auth/
        __init__.py
        user_auth.py       # UserAuthService
        password.py        # password hashing utilities
        oauth.py           # OAuth2/OIDC integration (optional)
```

### UserAuthService
- `login(username, password) -> SessionToken`
- `logout(session_token) -> None`
- `validate_session(session_token) -> Optional[User]`

### Dependencies
- S0.1 (User model), bcrypt library
