# S7.5 — TLS / Transport Security: Tasks

## Implementation Tasks
- [ ] Create `security/tls.py` with `create_tls_context()`
- [ ] Integrate TLS with Flask server startup
- [ ] Integrate TLS with stream receivers
- [ ] Handle missing/invalid certificate files at startup

## Testing Tasks
- [ ] Test server starts with valid TLS config
- [ ] Test server starts without TLS when disabled
- [ ] Test invalid certificate path produces startup error
