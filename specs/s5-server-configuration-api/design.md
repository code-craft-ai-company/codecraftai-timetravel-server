# S5.7 — Server Configuration API: Design

## Endpoints

| Method | Path | Service |
|---|---|---|
| GET | `/api/v1/config` | `ServerConfigStore.get_all()` |
| GET | `/api/v1/config/{key}` | `ServerConfigStore.get()` |
| PUT | `/api/v1/config/{key}` | `ServerConfigStore.set()` |

### Module: `server_config.py` in REST API v1 feature directory.

### Dependencies
- S0.3 (ServerConfigStore)
- S7.3 (Role-based access — admin required)
