# S6.4 — Portal Control Panel: Design

## Technical Architecture

### WebComponent: `<tt-portal-panel>`

The entire portal control panel is implemented as a single composite WebComponent that manages its own child elements.

```html
<tt-portal-panel process-id="uuid"></tt-portal-panel>
```

### Internal Structure
The `<tt-portal-panel>` renders:
- A checkbox list of portals using `<tt-portal-item>` child WebComponents
- A toolbar with Select All, Deselect All, Activate Selected, Deactivate Selected, Start Debug Session buttons

### Child WebComponents

| Component | Tag | Description |
|---|---|---|
| `PortalItem` | `<tt-portal-item>` | Single portal with checkbox and activation state indicator |

### Component Communication
- `<tt-portal-panel>` dispatches `portal-activated` and `portal-deactivated` CustomEvents.
- `<tt-portal-panel>` dispatches `session-created` CustomEvent when "Start Debug Session" is clicked.
- Inline state updates via shadow DOM re-render (no full page refresh).

### Module Layout
```
source/site/automojo/timetravelwebsite/static/js/components/
    tt-portal-panel.js
    tt-portal-item.js
```

### Data Sources
- AJAX calls to S5.2 (Portal Control API) and S5.4 (Debug Session API).

### Dependencies
- S5.2 (Portal Control API), S5.4 (Debug Session API)
