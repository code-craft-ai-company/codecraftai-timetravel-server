# S6.8 — Variable Inspector: Design

## Technical Architecture

### Template: `templates/sessions/variables.html`

### WebComponents

| Component | Tag | Description |
|---|---|---|
| `VariableList` | `<tt-variable-list>` | Searchable list of all captured variables with current values |
| `VariableHistory` | `<tt-variable-history>` | Chronological value history for a selected variable |
| `VariableStepper` | `<tt-variable-stepper>` | Step forward/backward controls for navigating value changes |
| `VariableValue` | `<tt-variable-value>` | Formatted display of a variable's value (supports objects, lists, primitives) |

### Component Communication
- `<tt-variable-list>` dispatches `variable-selected` CustomEvent carrying the variable name.
- `<tt-variable-history>` listens for `variable-selected` to display the history.
- `<tt-variable-stepper>` dispatches `step-changed` CustomEvent carrying the new timestamp position.
- `<tt-variable-stepper>` dispatches `position-changed` for timeline synchronization with `<tt-timeline-canvas>` (S6.6).

### Component Attributes
```html
<tt-variable-list session-id="uuid"></tt-variable-list>
<tt-variable-history session-id="uuid" variable-name=""></tt-variable-history>
<tt-variable-stepper></tt-variable-stepper>
```

### Module Layout
```
source/site/ccai/timetravelwebsite/static/js/components/
    tt-variable-list.js
    tt-variable-history.js
    tt-variable-stepper.js
    tt-variable-value.js
```

### Data Source
- `GET /api/v1/sessions/{id}/variables` and `GET /api/v1/sessions/{id}/variables/{name}`

### Dependencies
- S5.5 (Trace Data API), S6.6 (Timeline Viewer — sync via `position-changed`)
