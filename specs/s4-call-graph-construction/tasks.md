# S4.4 — Call Graph Construction: Tasks

## Implementation Tasks

- [x] Create `tracedata/call_graph.py` with `CallGraphNode` and `CallGraphBuilder`
- [x] Implement stack-based call graph construction algorithm
- [x] Implement per-thread graph separation
- [x] Compute duration from call/return timestamp offsets

## Testing Tasks

- [x] Test simple linear call graph (A calls B calls C)
- [x] Test nested/recursive call graph
- [x] Test multi-thread produces separate graphs
- [x] Test timing data accuracy
- [x] Test unmatched CallEvent (missing ReturnEvent) handling
