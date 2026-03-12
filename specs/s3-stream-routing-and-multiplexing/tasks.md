# S3.6 — Stream Routing and Multiplexing: Tasks

## Implementation Tasks

- [x] Create `streamreceiver/stream_router.py` with `StreamRouter`
- [x] Implement `route_stream()` — create storage reference, register in routing table
- [x] Implement `get_data_reference()` — lookup from routing table
- [x] Implement `finalize_route()` — finalize storage, update session
- [x] Ensure thread safety with locking

## Testing Tasks

- [x] Test routing creates separate storage for different processes
- [x] Test routing creates separate storage for different sessions
- [x] Test concurrent routing operations are thread-safe
- [x] Test finalize_route updates session data reference
