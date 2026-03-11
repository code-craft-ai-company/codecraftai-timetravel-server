# S1.1 — Service Registration Endpoint: Tasks

## Implementation Tasks

- [ ] Create `registration/` package with `__init__.py`
- [ ] Create `registration/service.py` with `RegistrationService` class
- [ ] Implement `register()` — credential validation, duplicate check, process creation/update
- [ ] Define request/response schemas
- [ ] Wire endpoint in REST API layer (deferred to S5.1)

## Testing Tasks

- [ ] Test successful registration with valid credentials
- [ ] Test registration rejected with invalid credentials (401)
- [ ] Test registration rejected with revoked credentials (401)
- [ ] Test duplicate host+pid updates existing record
- [ ] Test response contains process_id and status
- [ ] Test registered process is queryable from the database
