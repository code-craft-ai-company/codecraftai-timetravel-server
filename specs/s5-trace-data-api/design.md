# S5.5 — Trace Data API: Design

## Endpoints

| Method | Path | Service |
|---|---|---|
| GET | `/api/v1/sessions/{id}/events` | `TraceSearchEngine.search()` |
| GET | `/api/v1/sessions/{id}/timeline` | `TimelineBuilder.build()` |
| GET | `/api/v1/sessions/{id}/call-graph` | `CallGraphBuilder.build()` |
| GET | `/api/v1/sessions/{id}/variables/{name}` | `VariableTracker.build_histories()` |
| GET | `/api/v1/sessions/{id}/variables` | `VariableTracker.list_variables()` |

### Module: `trace_data.py` in REST API v1 feature directory.

### Dependencies
- S4.1–S4.6 (Trace data processing layer)
- S2.4 (DebugSessionManager — for session lookup)
