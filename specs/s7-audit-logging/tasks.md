# S7.6 — Audit Logging: Tasks

## Implementation Tasks
- [ ] Create `security/audit.py` with `AuditLogger`
- [ ] Implement `log()` method
- [ ] Implement `query()` method with filtering
- [ ] Integrate audit logging into all security-relevant service methods

## Testing Tasks
- [ ] Test login produces audit entry
- [ ] Test credential operations produce audit entries
- [ ] Test query filtering by time, actor, action
