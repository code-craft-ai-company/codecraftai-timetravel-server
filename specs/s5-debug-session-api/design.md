# S5.4 — Debug Session API: Design

## Endpoints

| Method | Path | Service |
|---|---|---|
| POST | `/api/v1/sessions` | `DebugSessionManager.create_session()` |
| GET | `/api/v1/sessions` | `DebugSessionManager.list_sessions()` |
| GET | `/api/v1/sessions/{id}` | `DebugSessionManager.get_session()` |
| POST | `/api/v1/sessions/{id}/close` | `DebugSessionManager.close_session()` |

### Module: `sessions.py` in REST API v1 feature directory.

### Dependencies
- S2.4 (DebugSessionManager)
