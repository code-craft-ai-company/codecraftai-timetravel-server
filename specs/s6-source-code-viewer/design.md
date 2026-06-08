# S6.9 — Source Code Viewer: Design

## Technical Architecture

### Template: `templates/sessions/source.html`

### WebComponents

| Component | Tag | Description |
|---|---|---|
| `SourceViewer` | `<tt-source-viewer>` | Read-only source code display with syntax highlighting and line numbers |
| `LineAnnotation` | `<tt-line-annotation>` | Gutter marker for lines with trace events |
| `LineEventPopup` | `<tt-line-event-popup>` | Popup listing trace events at a clicked annotated line |

### Component Communication
- `<tt-source-viewer>` dispatches `line-selected` CustomEvent when an annotated line is clicked.
- `<tt-line-event-popup>` listens for `line-selected` to show events at that line.
- `<tt-source-viewer>` listens for `position-changed` (from timeline/variable inspector) for synchronized scrolling.

### Component Attributes
```html
<tt-source-viewer session-id="uuid" file="path/to/file.py" highlight-line="42"></tt-source-viewer>
```

### Module Layout
```
source/site/ccai/timetravelwebsite/static/js/components/
    tt-source-viewer.js
    tt-line-annotation.js
    tt-line-event-popup.js
```

### Data Source
- Event annotations from `GET /api/v1/sessions/{id}/events?filename=...`

### Dependencies
- S5.5 (Trace Data API)
