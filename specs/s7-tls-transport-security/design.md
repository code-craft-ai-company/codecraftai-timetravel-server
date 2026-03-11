# S7.5 — TLS / Transport Security: Design

## Module: `security/tls.py`

### TLS Context Factory
```python
def create_tls_context(cert_path: str, key_path: str) -> ssl.SSLContext:
    """Create SSL context from certificate and key files."""
```

### Integration
- Applied to Flask WSGI server for API (via `ssl_context` parameter).
- Applied to TCP/Unix socket stream receivers.

### Dependencies
- S0.3 (tls_enabled, tls_cert_path, tls_key_path configuration)
- Python `ssl` (stdlib)
