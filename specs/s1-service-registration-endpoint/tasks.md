# S1.1 — Service Registration Endpoint: Tasks

## Implementation Tasks

- [x] Create `registration/` package with `__init__.py`
- [x] Create `registration/service.py` with `RegistrationService` class
- [x] Implement `register()` — credential validation, duplicate check, process creation/update
- [x] Define request/response schemas
- [ ] Wire endpoint in REST API layer (deferred to S5.1)

## Testing Tasks

- [x] Test successful registration with valid credentials
- [x] Test registration rejected with invalid credentials (401)
- [x] Test registration rejected with revoked credentials (401)
- [x] Test duplicate host+pid updates existing record
- [x] Test response contains process_id and status
- [x] Test registered process is queryable from the database
