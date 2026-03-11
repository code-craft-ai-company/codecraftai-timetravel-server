# S2.3 — Trace Configuration Query and Update: Tasks

## Implementation Tasks

- [ ] Create `debugcontrol/trace_config.py` with `TraceConfigService`
- [ ] Define `TraceConfigInfo` dataclass
- [ ] Implement `get_config()` — send `get_trace_config` command, parse response
- [ ] Implement `update_config()` — send `update_trace_config` command, return confirmed config

## Testing Tasks

- [ ] Test get_config returns current configuration from mock remote
- [ ] Test update_config sends correct command and returns updated config
- [ ] Test update_config with invalid granularity returns error
- [ ] Test connection failure returns descriptive error
