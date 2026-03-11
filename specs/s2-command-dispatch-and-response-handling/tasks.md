# S2.5 — Command Dispatch and Response Handling: Tasks

## Implementation Tasks

- [x] Create `debugcontrol/command_dispatcher.py` with `CommandDispatcher`
- [x] Implement TCP connection establishment with timeout
- [x] Implement JSON-lines request serialization
- [x] Implement JSON-lines response deserialization
- [x] Implement authentication handshake with credential token
- [x] Define `CommandError` and `CommandTimeoutError` exceptions
- [x] Implement `close()` for connection cleanup

## Testing Tasks

- [x] Test successful command dispatch and response parsing
- [x] Test timeout raises `CommandTimeoutError`
- [x] Test error response raises `CommandError`
- [x] Test connection refused raises appropriate error
- [x] Test authentication token is included in request
