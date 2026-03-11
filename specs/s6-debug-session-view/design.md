# S6.5 — Debug Session View: Design

## Technical Architecture

### Template: `templates/sessions/detail.html`

### WebComponents

| Component | Tag | Description |
|---|---|---|
| `SessionHeader` | `<tt-session-header>` | Session ID, status badge, Close Session button |
| `SessionMetadata` | `<tt-session-metadata>` | Process name, timestamps, duration display |
| `SessionPortals` | `<tt-session-portals>` | List of associated portal names |
| `ViewsNavigation` | `<tt-views-nav>` | Tab navigation to Timeline, Call Graph, Variable Inspector |

### Component Attributes
```html
<tt-session-header session-id="uuid" status="active"></tt-session-header>
<tt-session-metadata session-id="uuid"></tt-session-metadata>
<tt-session-portals session-id="uuid"></tt-session-portals>
<tt-views-nav session-id="uuid"></tt-views-nav>
```

- `<tt-session-header>` dispatches `session-closed` CustomEvent when Close is clicked.

### Module Layout
```
source/site/automojo/timetravelwebsite/static/js/components/
    tt-session-header.js
    tt-session-metadata.js
    tt-session-portals.js
    tt-views-nav.js
```

### Data Sources
- `GET /api/v1/sessions/{id}`

### Dependencies
- S5.4 (Debug Session API), S6.6, S6.7, S6.8 (linked views)
