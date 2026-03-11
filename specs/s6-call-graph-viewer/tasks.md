# S6.7 — Call Graph Viewer: Tasks

## Implementation Tasks

- [ ] Create `templates/sessions/call_graph.html` with WebComponent tags
- [ ] Implement `<tt-call-graph-tree>` WebComponent with expand/collapse
- [ ] Implement `<tt-call-graph-node>` WebComponent with duration bar
- [ ] Implement `<tt-thread-selector>` WebComponent
- [ ] Implement `<tt-node-detail-panel>` WebComponent
- [ ] Wire `node-selected` and `thread-changed` CustomEvents

## Testing Tasks

- [ ] Test call graph renders correctly
- [ ] Test expand/collapse of subtrees
- [ ] Test node click dispatches `node-selected` and shows details
- [ ] Test thread selector switches graph
