# S6.11 — Server Configuration View: Design

## Technical Architecture

### Template: `templates/admin/configuration.html`

### WebComponents

| Component | Tag | Description |
|---|---|---|
| `ConfigTable` | `<tt-config-table>` | Configuration table with key, current value, default, and type columns |
| `ConfigEditor` | `<tt-config-editor>` | Inline editor per row — text input for strings, number input for integers, checkbox for booleans |
| `ConfigToolbar` | `<tt-config-toolbar>` | Apply Changes and Revert Changes buttons |

### Component Communication
- `<tt-config-editor>` dispatches `value-changed` CustomEvent carrying the key and new value.
- `<tt-config-table>` tracks pending changes internally.
- `<tt-config-toolbar>` dispatches `apply-changes` and `revert-changes` CustomEvents.
- `<tt-config-table>` listens for `apply-changes` to submit all pending values via `PUT /api/v1/config/{key}`.

### Component Attributes
```html
<tt-config-table></tt-config-table>
<tt-config-toolbar></tt-config-toolbar>
```

### Validation
- `<tt-config-editor>` performs client-side type validation before dispatching `value-changed`.
- Invalid values display inline error messages within the shadow DOM.

### Module Layout
```
source/site/automojo/timetravelwebsite/static/js/components/
    tt-config-table.js
    tt-config-editor.js
    tt-config-toolbar.js
```

### Data Source
- `GET /api/v1/config`, `PUT /api/v1/config/{key}` (S5.7)

### Dependencies
- S5.7 (Server Configuration API), S7.3 (admin role check)
