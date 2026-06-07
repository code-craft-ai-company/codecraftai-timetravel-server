# S0.1 — Database Schema and ORM Models: Tasks

## Implementation Tasks

- [ ] Create `source/packages/ccai/timetravelserver/persistence/` package with `__init__.py`
- [ ] Create `models/base.py` with declarative base and `BaseMixin` (id, created_at, updated_at)
- [ ] Create `models/user.py` — `User` ORM model
- [ ] Create `models/credential.py` — `Credential` ORM model
- [ ] Create `models/process.py` — `RegisteredProcess` ORM model
- [ ] Create `models/portal_snapshot.py` — `PortalSnapshot` ORM model with FK to process
- [ ] Create `models/trace_session.py` — `TraceSession` ORM model with FK to process
- [ ] Create `models/server_config.py` — `ServerConfiguration` ORM model
- [ ] Create `models/__init__.py` re-exporting all models
- [ ] Create `engine.py` — engine factory, scoped session factory, database URL configuration
- [ ] Configure Alembic with `migrations/env.py` and initial migration
- [ ] Add indexes on frequently queried columns per design
- [ ] Verify foreign key constraints are enforced

## Testing Tasks

- [ ] Write tests for each ORM model: insert, query, update, delete
- [ ] Write tests for foreign key constraint enforcement
- [ ] Write tests for unique constraint enforcement (username, token_hash, key)
- [ ] Write tests for default value population (id, created_at, lifecycle_state)
- [ ] Write test for Alembic upgrade/downgrade cycle
