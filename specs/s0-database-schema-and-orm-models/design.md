# S0.1 — Database Schema and ORM Models: Design

## Overview
This feature establishes the relational persistence layer for the time travel server. All entities are modeled as SQLAlchemy ORM classes backed by a SQLite database (with easy swap to PostgreSQL for production). Alembic is used for schema migrations.

## Technical Architecture

### Database Engine
- **SQLAlchemy** as the ORM framework (declarative mapping).
- **SQLite** as the default development database; configurable URI for production (PostgreSQL, MySQL).
- **Alembic** for schema migration management.

### Module Layout
```
source/packages/automojo/timetravelserver/
    persistence/
        __init__.py
        models/
            __init__.py
            base.py            # Declarative base, common mixins
            user.py            # User model
            credential.py      # Credential model
            process.py         # RegisteredProcess model
            portal_snapshot.py  # PortalSnapshot model
            trace_session.py    # TraceSession model
            server_config.py    # ServerConfiguration model
        engine.py              # Engine factory, session factory
        migrations/
            env.py
            versions/
```

### Data Models

#### User
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK, default uuid4 |
| username | String(128) | Unique, NOT NULL |
| password_hash | String(256) | NOT NULL |
| email | String(256) | Nullable |
| role | String(32) | NOT NULL, default "viewer" |
| created_at | DateTime | NOT NULL, default utcnow |
| updated_at | DateTime | NOT NULL, default utcnow, onupdate utcnow |

#### Credential
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK, default uuid4 |
| token_hash | String(256) | Unique, NOT NULL |
| label | String(128) | NOT NULL |
| created_at | DateTime | NOT NULL, default utcnow |
| last_used_at | DateTime | Nullable |
| revoked_at | DateTime | Nullable |
| expires_at | DateTime | Nullable |

#### RegisteredProcess
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK, default uuid4 |
| host | String(256) | NOT NULL |
| pid | Integer | NOT NULL |
| application_name | String(256) | Nullable |
| pod_version | String(64) | Nullable |
| remote_control_address | String(512) | Nullable |
| lifecycle_state | String(32) | NOT NULL, default "registered" |
| registered_at | DateTime | NOT NULL, default utcnow |
| last_heartbeat_at | DateTime | Nullable |
| disconnected_at | DateTime | Nullable |

#### PortalSnapshot
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK, default uuid4 |
| process_id | UUID | FK → registered_processes.id, NOT NULL |
| portal_name | String(256) | NOT NULL |
| is_active | Boolean | NOT NULL, default False |
| snapshot_at | DateTime | NOT NULL, default utcnow |

#### TraceSession
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK, default uuid4 |
| process_id | UUID | FK → registered_processes.id, NOT NULL |
| started_at | DateTime | NOT NULL, default utcnow |
| stopped_at | DateTime | Nullable |
| status | String(32) | NOT NULL, default "active" |
| data_reference | String(1024) | Nullable |

#### ServerConfiguration
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK, default uuid4 |
| key | String(256) | Unique, NOT NULL |
| value | Text | NOT NULL |
| updated_at | DateTime | NOT NULL, default utcnow, onupdate utcnow |

### Indexes
- `users`: index on `username`
- `credentials`: index on `token_hash`
- `registered_processes`: index on `lifecycle_state`, composite index on (`host`, `pid`)
- `portal_snapshots`: index on `process_id`
- `trace_sessions`: index on `process_id`, index on `status`
- `server_configuration`: index on `key`

### Dependencies
- `sqlalchemy` (ORM)
- `alembic` (migrations)

## Cross-Cutting Concerns
- All models inherit a `BaseMixin` providing `id`, `created_at`, and `updated_at`.
- Session management uses a scoped session factory for thread safety.
- UTC timestamps are used throughout.
