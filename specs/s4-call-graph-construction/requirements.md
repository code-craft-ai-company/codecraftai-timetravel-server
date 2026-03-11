# S4.4 — Call Graph Construction: Requirements

## Overview
Builds call graphs from `CallEvent` and `ReturnEvent` sequences, representing the function invocation hierarchy with timing data for each node.

## Requirements (EARS Notation)

### REQ-S4.4-001: Graph Building
WHEN `CallEvent` and `ReturnEvent` sequences are provided, THE system SHALL construct a tree structure representing the function invocation hierarchy.

### REQ-S4.4-002: Node Data
Each call graph node shall contain: `function_name`, `filename`, `line_number`, `start_offset`, `end_offset`, `duration`, `arguments` (optional), `return_value` (optional), and `children` (list of sub-calls).

### REQ-S4.4-003: Root Node
The system shall represent the outermost function call as the root node of the call graph.

### REQ-S4.4-004: Timing Data
Each node shall have `duration` computed as the difference between the `ReturnEvent` and `CallEvent` timestamp offsets.

### REQ-S4.4-005: Multi-Thread Support
The system shall build separate call graphs per thread when events from multiple threads are present.

## Acceptance Criteria
- Call graph correctly represents the function invocation hierarchy.
- Timing data is accurate for each node.
- Nested calls are represented as children.
- Multiple threads produce separate graphs.
