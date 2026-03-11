# S6.6 — Timeline Viewer: Design

## Technical Architecture

### Template: `templates/sessions/timeline.html`

### WebComponents

| Component | Tag | Description |
|---|---|---|
| `TimelineCanvas` | `<tt-timeline-canvas>` | Canvas-based timeline with events as colored markers on horizontal axis |
| `TimelineControls` | `<tt-timeline-controls>` | Zoom in/out, reset zoom, pan mode toggle buttons |
| `EventTypeFilter` | `<tt-event-type-filter>` | Checkboxes to filter by event type with color legend |
| `EventDetailPanel` | `<tt-event-detail-panel>` | Slide-out panel showing full event fields on click |

### Component Communication
- `<tt-timeline-canvas>` dispatches `event-selected` CustomEvent carrying the event data.
- `<tt-event-detail-panel>` listens for `event-selected` to display details.
- `<tt-event-type-filter>` dispatches `filter-changed` CustomEvent.
- `<tt-timeline-canvas>` listens for `filter-changed` to re-render.
- `<tt-timeline-canvas>` dispatches `position-changed` for synchronization with other views.

### Component Attributes
```html
<tt-timeline-canvas session-id="uuid"></tt-timeline-canvas>
<tt-timeline-controls target="timeline-canvas-id"></tt-timeline-controls>
<tt-event-type-filter></tt-event-type-filter>
<tt-event-detail-panel></tt-event-detail-panel>
```

### Module Layout
```
source/site/automojo/timetravelwebsite/static/js/components/
    tt-timeline-canvas.js
    tt-timeline-controls.js
    tt-event-type-filter.js
    tt-event-detail-panel.js
```

### Data Source
- `GET /api/v1/sessions/{id}/timeline` and `GET /api/v1/sessions/{id}/events`

### Dependencies
- S5.5 (Trace Data API)
