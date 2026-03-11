# S8.4 — Data Retention and Cleanup: Tasks

## Implementation Tasks
- [ ] Create `ops/retention.py` with `RetentionJob`
- [ ] Implement trace data cleanup using storage backend `list_expired` and `delete`
- [ ] Implement session and process record cleanup
- [ ] Implement scheduling

## Testing Tasks
- [ ] Test expired trace data is deleted
- [ ] Test active data is not affected
- [ ] Test retention period is configurable
