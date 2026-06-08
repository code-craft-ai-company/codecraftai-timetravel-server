# S6.3 — Process Detail View: Design

## Technical Architecture

### Template: `templates/processes/detail.html`

### WebComponents

| Component | Tag | Description |
|---|---|---|
| `ProcessMetadata` | `<tt-process-metadata>` | Key-value display of process fields |
| `PortalPanel` | `<tt-portal-panel>` | Embedded portal control panel (S6.4) |
| `TraceConfigEditor` | `<tt-trace-config-editor>` | Editable form for granularity and inner-portal settings |
| `SessionList` | `<tt-session-list>` | Table of associated debug sessions |
| `ActionBar` | `<tt-action-bar>` | Buttons for Refresh, Disconnect, Delete |

### Component Attributes
```html
<tt-process-metadata process-id="uuid"></tt-process-metadata>
<tt-portal-panel process-id="uuid"></tt-portal-panel>
<tt-trace-config-editor process-id="uuid"></tt-trace-config-editor>
<tt-session-list process-id="uuid"></tt-session-list>
<tt-action-bar process-id="uuid" state="active"></tt-action-bar>
```

### Module Layout
```
source/site/ccai/timetravelwebsite/static/js/components/
    tt-process-metadata.js
    tt-trace-config-editor.js
    tt-session-list.js
    tt-action-bar.js
```

### Data Sources
- `GET /api/v1/processes/{id}`, `GET /api/v1/processes/{id}/portals`, `GET /api/v1/processes/{id}/trace-config`, `GET /api/v1/sessions?process_id={id}`

### Dependencies
- S5.1, S5.2, S5.3, S5.4 (REST APIs)
- S6.4 (Portal Control Panel — `<tt-portal-panel>`)
