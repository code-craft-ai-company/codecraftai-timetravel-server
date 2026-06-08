# S6.2 — Process List View: Design

## Technical Architecture

### Template: `templates/processes/list.html`

### WebComponents

| Component | Tag | Description |
|---|---|---|
| `ProcessTable` | `<tt-process-table>` | Sortable, paginated data table of registered processes |
| `StateFilter` | `<tt-state-filter>` | Dropdown filter for lifecycle state |
| `SearchBar` | `<tt-search-bar>` | Text search input with debounced API query |
| `PaginationNav` | `<tt-pagination-nav>` | Page navigation controls (prev/next, page size) |
| `StateBadge` | `<tt-state-badge>` | Color-coded lifecycle state indicator |

### Component Details

```javascript
class ProcessTable extends HTMLElement {
    static get observedAttributes() { return ['state', 'search', 'sort-by', 'page', 'page-size']; }
    connectedCallback() { this._render(); }
    attributeChangedCallback(name, oldVal, newVal) { this._render(); }
}
customElements.define('tt-process-table', ProcessTable);
```

- `<tt-state-badge>` renders distinct colors: green (active), yellow (stale), red (unreachable), gray (disconnected), blue (registered).
- `<tt-process-table>` emits a `row-click` CustomEvent when a row is clicked, carrying the `process_id`.
- Parent page listens for `row-click` and navigates to `/processes/{id}`.

### Module Layout
```
source/site/ccai/timetravelwebsite/static/js/components/
    tt-process-table.js
    tt-state-filter.js
    tt-search-bar.js
    tt-pagination-nav.js
    tt-state-badge.js
```

### Data Source
- `GET /api/v1/processes` with query parameters for state, search, sort, offset, limit.

### Dependencies
- S5.1 (Process Management API)
