# S3.6 — Stream Routing and Multiplexing: Tasks

## Implementation Tasks

- [ ] Create `streamreceiver/stream_router.py` with `StreamRouter`
- [ ] Implement `route_stream()` — create storage reference, register in routing table
- [ ] Implement `get_data_reference()` — lookup from routing table
- [ ] Implement `finalize_route()` — finalize storage, update session
- [ ] Ensure thread safety with locking

## Testing Tasks

- [ ] Test routing creates separate storage for different processes
- [ ] Test routing creates separate storage for different sessions
- [ ] Test concurrent routing operations are thread-safe
- [ ] Test finalize_route updates session data reference
