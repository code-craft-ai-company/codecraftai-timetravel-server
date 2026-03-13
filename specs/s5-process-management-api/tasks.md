# S5.1 — Process Management API: Tasks

## Implementation Tasks

- [x] Create `processes.py` API namespace with Flask-RESTX
- [x] Implement GET `/api/v1/processes` with pagination, filtering, sorting
- [x] Implement GET `/api/v1/processes/{id}` with full detail
- [x] Implement POST `/api/v1/processes/{id}/refresh`
- [x] Implement POST `/api/v1/processes/{id}/disconnect`
- [x] Implement DELETE `/api/v1/processes/{id}`
- [x] Implement POST registration, unregistration, heartbeat endpoints
- [x] Add authentication decorator to all endpoints

## Testing Tasks

- [x] Test list endpoint with pagination
- [x] Test list endpoint with state filtering
- [x] Test get detail returns complete process info
- [x] Test refresh triggers metadata refresh
- [x] Test disconnect changes state
- [x] Test delete removes disconnected process
- [x] Test unauthenticated request returns 401
