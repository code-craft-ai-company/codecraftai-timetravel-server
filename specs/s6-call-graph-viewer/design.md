# S6.7 — Call Graph Viewer: Design

## Technical Architecture

### Template: `templates/sessions/call_graph.html`

### WebComponents

| Component | Tag | Description |
|---|---|---|
| `CallGraphTree` | `<tt-call-graph-tree>` | Expandable tree or flame-graph visualization of function calls |
| `CallGraphNode` | `<tt-call-graph-node>` | Single node showing function name, file, line, duration bar |
| `ThreadSelector` | `<tt-thread-selector>` | Dropdown for selecting which thread's call graph to display |
| `NodeDetailPanel` | `<tt-node-detail-panel>` | Panel showing call/return details, arguments, return value |

### Component Communication
- `<tt-call-graph-node>` dispatches `node-selected` CustomEvent carrying the node data.
- `<tt-node-detail-panel>` listens for `node-selected` to display details.
- `<tt-thread-selector>` dispatches `thread-changed` CustomEvent.
- `<tt-call-graph-tree>` listens for `thread-changed` to re-render the selected thread's graph.

### Module Layout
```
source/site/automojo/timetravelwebsite/static/js/components/
    tt-call-graph-tree.js
    tt-call-graph-node.js
    tt-thread-selector.js
    tt-node-detail-panel.js
```

### Data Source
- `GET /api/v1/sessions/{id}/call-graph`

### Dependencies
- S5.5 (Trace Data API)
