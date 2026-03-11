# S2.5 — Command Dispatch and Response Handling: Tasks

## Implementation Tasks

- [ ] Create `debugcontrol/command_dispatcher.py` with `CommandDispatcher`
- [ ] Implement TCP connection establishment with timeout
- [ ] Implement JSON-lines request serialization
- [ ] Implement JSON-lines response deserialization
- [ ] Implement authentication handshake with credential token
- [ ] Define `CommandError` and `CommandTimeoutError` exceptions
- [ ] Implement `close()` for connection cleanup

## Testing Tasks

- [ ] Test successful command dispatch and response parsing
- [ ] Test timeout raises `CommandTimeoutError`
- [ ] Test error response raises `CommandError`
- [ ] Test connection refused raises appropriate error
- [ ] Test authentication token is included in request
