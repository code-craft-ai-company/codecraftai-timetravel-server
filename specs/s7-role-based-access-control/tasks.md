# S7.3 — Role-Based Access Control: Tasks

## Implementation Tasks
- [ ] Create `auth/rbac.py` with `require_role` decorator
- [ ] Implement role hierarchy (admin > operator > viewer)
- [ ] Apply role checks to all REST API and web UI endpoints

## Testing Tasks
- [ ] Test admin can access admin endpoints
- [ ] Test operator cannot access admin endpoints (403)
- [ ] Test viewer cannot access write endpoints (403)
- [ ] Test role hierarchy inheritance
