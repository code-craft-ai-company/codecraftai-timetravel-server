# S2.4 — Debug Session Management: Tasks

## Implementation Tasks

- [x] Create `debugcontrol/session_manager.py` with `DebugSessionManager`
- [x] Implement `create_session()` — create TraceSession, record portal names
- [x] Implement `close_session()` — set stopped_at and status
- [x] Implement `list_sessions()` — with process and status filtering
- [x] Implement `get_session()` — single session retrieval
- [x] Implement `update_data_reference()` — link trace data to session

## Testing Tasks

- [x] Test session creation with valid process_id
- [x] Test session closure sets stopped_at and status to completed
- [x] Test listing sessions by process_id
- [x] Test listing sessions by status
- [x] Test get_session returns correct session
- [x] Test update_data_reference links data correctly
