# S0.3 — Server Configuration Model: Tasks

## Implementation Tasks

- [ ] Create `persistence/server_config_store.py` with `ServerConfigStore` class
- [ ] Define `CONFIG_SCHEMA` dict with all keys, types, and defaults
- [ ] Implement `get()` — query DB, fall back to default
- [ ] Implement `set()` — validate type, upsert DB row
- [ ] Implement `get_all()` — merge DB overrides with defaults
- [ ] Implement `validate()` — type check and key existence check
- [ ] Export from `persistence/__init__.py`

## Testing Tasks

- [ ] Test `get()` returns default when no DB entry exists
- [ ] Test `get()` returns DB value when entry exists
- [ ] Test `set()` persists value and subsequent `get()` returns it
- [ ] Test `set()` rejects invalid type
- [ ] Test `set()` rejects unknown key
- [ ] Test `get_all()` merges defaults and overrides correctly
