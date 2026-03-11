# S5.1 — Process Management API: Tasks

## Implementation Tasks

- [ ] Create `processes.py` API namespace with Flask-RESTX
- [ ] Implement GET `/api/v1/processes` with pagination, filtering, sorting
- [ ] Implement GET `/api/v1/processes/{id}` with full detail
- [ ] Implement POST `/api/v1/processes/{id}/refresh`
- [ ] Implement POST `/api/v1/processes/{id}/disconnect`
- [ ] Implement DELETE `/api/v1/processes/{id}`
- [ ] Implement POST registration, unregistration, heartbeat endpoints
- [ ] Add authentication decorator to all endpoints

## Testing Tasks

- [ ] Test list endpoint with pagination
- [ ] Test list endpoint with state filtering
- [ ] Test get detail returns complete process info
- [ ] Test refresh triggers metadata refresh
- [ ] Test disconnect changes state
- [ ] Test delete removes disconnected process
- [ ] Test unauthenticated request returns 401
