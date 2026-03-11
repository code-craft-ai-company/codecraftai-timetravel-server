# S4.4 — Call Graph Construction: Tasks

## Implementation Tasks

- [ ] Create `tracedata/call_graph.py` with `CallGraphNode` and `CallGraphBuilder`
- [ ] Implement stack-based call graph construction algorithm
- [ ] Implement per-thread graph separation
- [ ] Compute duration from call/return timestamp offsets

## Testing Tasks

- [ ] Test simple linear call graph (A calls B calls C)
- [ ] Test nested/recursive call graph
- [ ] Test multi-thread produces separate graphs
- [ ] Test timing data accuracy
- [ ] Test unmatched CallEvent (missing ReturnEvent) handling
