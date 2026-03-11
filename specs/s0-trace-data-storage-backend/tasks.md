# S0.4 — Trace Data Storage Backend: Tasks

## Implementation Tasks

- [ ] Create `persistence/trace_storage/` package with `__init__.py`
- [ ] Create `backend_abc.py` with `TraceStorageBackend` ABC and all abstract methods
- [ ] Create `filesystem_backend.py` with `FilesystemTraceStorage` implementation
- [ ] Implement `write()` — create temp file, return data reference
- [ ] Implement `append()` — append bytes to temp file
- [ ] Implement `finalize()` — rename temp to final path
- [ ] Implement `read()` — read finalized file bytes
- [ ] Implement `list_references()` — walk directory tree
- [ ] Implement `delete()` — remove file
- [ ] Implement `exists()` — check file existence
- [ ] Implement `list_expired()` — filter by file modification time
- [ ] Export from `persistence/__init__.py`

## Testing Tasks

- [ ] Test write/read roundtrip preserves data
- [ ] Test append accumulates data correctly
- [ ] Test finalize makes data visible to read
- [ ] Test read raises error for non-existent reference
- [ ] Test list_references returns all stored references
- [ ] Test delete removes data
- [ ] Test list_expired correctly identifies old files
- [ ] Test atomic write — incomplete write not visible to readers
