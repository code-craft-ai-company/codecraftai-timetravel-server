# S3.5 — Back-Pressure and Flow Control: Tasks

## Implementation Tasks

- [x] Create `streamreceiver/flow_control.py` with `FlowController`
- [x] Implement per-connection buffer tracking
- [x] Implement high/low watermark pause/resume logic
- [x] Implement global memory limit tracking
- [x] Implement `should_accept_new()` for connection admission control
- [x] Integrate with `StreamSessionLifecycle`

## Testing Tasks

- [x] Test buffer exceeding high watermark returns PAUSE
- [x] Test buffer dropping below low watermark returns RESUME
- [x] Test global memory limit rejects new connections
- [x] Test connection registration and unregistration
