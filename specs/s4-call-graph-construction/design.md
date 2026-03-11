# S4.4 — Call Graph Construction: Design

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    tracedata/
        call_graph.py   # CallGraphBuilder, CallGraphNode
```

### Data Model

```python
@dataclass
class CallGraphNode:
    function_name: str
    filename: str
    line_number: int
    start_offset: float
    end_offset: float
    duration: float
    arguments: Optional[dict]
    return_value: Optional[Any]
    children: List["CallGraphNode"]

class CallGraphBuilder:
    def build(self, events: List[TraceEvent]) -> Dict[int, CallGraphNode]:
        """Build call graphs keyed by thread_id."""
```

### Algorithm
- Maintain a stack per thread.
- On `CallEvent`: push a new node onto the stack.
- On `ReturnEvent`: pop the stack, compute duration, attach to parent as child.
- Root node is the last remaining node on the stack.

### Dependencies
- S0.5 (CallEvent, ReturnEvent)
