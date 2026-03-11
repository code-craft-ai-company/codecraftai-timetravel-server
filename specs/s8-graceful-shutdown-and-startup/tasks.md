# S8.5 — Graceful Shutdown and Startup: Tasks

## Implementation Tasks
- [ ] Create `ops/lifecycle.py` with `ServerLifecycle`
- [ ] Implement ordered startup of components
- [ ] Implement reverse-order shutdown with timeout
- [ ] Register signal handlers

## Testing Tasks
- [ ] Test components start in correct order
- [ ] Test shutdown completes gracefully
- [ ] Test shutdown timeout triggers force terminate
