# S3.5 — Back-Pressure and Flow Control: Tasks

## Implementation Tasks

- [ ] Create `streamreceiver/flow_control.py` with `FlowController`
- [ ] Implement per-connection buffer tracking
- [ ] Implement high/low watermark pause/resume logic
- [ ] Implement global memory limit tracking
- [ ] Implement `should_accept_new()` for connection admission control
- [ ] Integrate with `StreamSessionLifecycle`

## Testing Tasks

- [ ] Test buffer exceeding high watermark returns PAUSE
- [ ] Test buffer dropping below low watermark returns RESUME
- [ ] Test global memory limit rejects new connections
- [ ] Test connection registration and unregistration
