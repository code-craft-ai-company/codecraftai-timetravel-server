# S2.4 — Debug Session Management: Tasks

## Implementation Tasks

- [ ] Create `debugcontrol/session_manager.py` with `DebugSessionManager`
- [ ] Implement `create_session()` — create TraceSession, record portal names
- [ ] Implement `close_session()` — set stopped_at and status
- [ ] Implement `list_sessions()` — with process and status filtering
- [ ] Implement `get_session()` — single session retrieval
- [ ] Implement `update_data_reference()` — link trace data to session

## Testing Tasks

- [ ] Test session creation with valid process_id
- [ ] Test session closure sets stopped_at and status to completed
- [ ] Test listing sessions by process_id
- [ ] Test listing sessions by status
- [ ] Test get_session returns correct session
- [ ] Test update_data_reference links data correctly
