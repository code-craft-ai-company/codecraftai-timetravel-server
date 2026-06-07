# S6.1 — Dashboard: Design

## Technical Architecture

### Template: `templates/dashboard.html`

### WebComponents

All interactive controls are implemented as JavaScript WebComponent custom elements.

| Component | Tag | Description |
|---|---|---|
| `HealthSummaryCard` | `<tt-health-summary>` | Displays server health status, uptime, and component statuses |
| `ProcessSummaryCard` | `<tt-process-summary>` | Displays process counts grouped by lifecycle state |
| `SessionSummaryCard` | `<tt-session-summary>` | Displays active and recently completed session counts |
| `ActivityFeed` | `<tt-activity-feed>` | Reverse-chronological list of recent events |
| `QuickActions` | `<tt-quick-actions>` | Button links to key pages |

### Component Pattern

All WebComponents follow the standard pattern:
```javascript
class HealthSummaryCard extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() { this._render(); this._startAutoRefresh(); }
    disconnectedCallback() { this._stopAutoRefresh(); }
    _render() { /* Fetch data and render shadow DOM */ }
}
customElements.define('tt-health-summary', HealthSummaryCard);
```

### Module Layout
```
source/site/ccai/timetravelwebsite/static/js/components/
    tt-health-summary.js
    tt-process-summary.js
    tt-session-summary.js
    tt-activity-feed.js
    tt-quick-actions.js
```

### Data Sources
- `GET /api/v1/health`, `GET /api/v1/processes` (summary), `GET /api/v1/sessions` (summary).
- Each component fetches its own data and manages auto-refresh internally.

### Dependencies
- S5.1 (Process Management API), S5.4 (Debug Session API), S5.8 (Health API)
