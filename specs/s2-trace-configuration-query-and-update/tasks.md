# S2.3 — Trace Configuration Query and Update: Tasks

## Implementation Tasks

- [x] Create `debugcontrol/trace_config.py` with `TraceConfigService`
- [x] Define `TraceConfigInfo` dataclass
- [x] Implement `get_config()` — send `get_trace_config` command, parse response
- [x] Implement `update_config()` — send `update_trace_config` command, return confirmed config

## Testing Tasks

- [x] Test get_config returns current configuration from mock remote
- [x] Test update_config sends correct command and returns updated config
- [x] Test update_config with invalid granularity returns error
- [x] Test connection failure returns descriptive error
