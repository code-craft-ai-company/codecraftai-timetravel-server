# S5.2 — Portal Control API: Design

## Technical Architecture

### Endpoints

| Method | Path | Service |
|---|---|---|
| GET | `/api/v1/processes/{id}/portals` | `PortalDiscoveryService.discover()` |
| POST | `/api/v1/processes/{id}/portals/{name}/activate` | `PortalControlService.activate_portal()` |
| POST | `/api/v1/processes/{id}/portals/{name}/deactivate` | `PortalControlService.deactivate_portal()` |
| POST | `/api/v1/processes/{id}/portals/activate` | `PortalControlService.activate_portals()` |
| POST | `/api/v1/processes/{id}/portals/deactivate` | `PortalControlService.deactivate_portals()` |

### Module Layout
```
source/site/automojo/timetravelwebsite/restapis/versions/v1/feature/
    portals.py
```

### Dependencies
- S2.1 (PortalDiscoveryService), S2.2 (PortalControlService)
