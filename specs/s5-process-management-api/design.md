# S5.1 — Process Management API: Design

## Technical Architecture

### Endpoints

| Method | Path | Description | Service Method |
|---|---|---|---|
| GET | `/api/v1/processes` | List processes | `ProcessRegistry.list_processes()` |
| GET | `/api/v1/processes/{id}` | Get detail | `ProcessRegistry.get_process()` |
| POST | `/api/v1/processes/{id}/refresh` | Force refresh | `MetadataRefreshService.refresh()` |
| POST | `/api/v1/processes/{id}/disconnect` | Force disconnect | `RegistrationService.unregister()` |
| DELETE | `/api/v1/processes/{id}` | Delete record | `ProcessRegistry.delete_process()` |
| POST | `/api/v1/processes/register` | Pod registration | `RegistrationService.register()` |
| POST | `/api/v1/processes/unregister` | Pod unregistration | `RegistrationService.unregister()` |
| POST | `/api/v1/processes/heartbeat` | Pod heartbeat | `HeartbeatService.receive()` |

### Module Layout
```
source/site/ccai/timetravelwebsite/restapis/versions/v1/feature/
    processes.py   # Process management namespace
```

### Dependencies
- S1.1–S1.5 (Service layer)
- S7.2 (API authentication)
