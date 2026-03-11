# S6.7 — Call Graph Viewer: Requirements

## Overview
Tree or flame-graph visualization of the call hierarchy within a portal scope.

## Requirements (EARS Notation)

### REQ-S6.7-001: Graph Rendering
The view shall render the call graph as a tree or flame graph with nodes representing function calls.

### REQ-S6.7-002: Node Data
Each node shall display function name, file, line number, and execution duration.

### REQ-S6.7-003: Expand/Collapse
The view shall support click-to-expand and click-to-collapse for subtrees.

### REQ-S6.7-004: Node Inspection
WHEN a node is clicked, THE view SHALL show call/return details including arguments and return value.

### REQ-S6.7-005: Thread Selection
WHEN multiple threads are present, THE view SHALL provide a thread selector.

## Acceptance Criteria
- Call graph accurately represents the invocation hierarchy.
- Expand/collapse works for subtrees.
- Node click shows detailed information.
