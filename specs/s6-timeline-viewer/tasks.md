# S6.6 — Timeline Viewer: Tasks

## Implementation Tasks

- [ ] Create `templates/sessions/timeline.html` with WebComponent tags
- [ ] Implement `<tt-timeline-canvas>` WebComponent with canvas rendering
- [ ] Implement zoom and pan in `<tt-timeline-controls>` WebComponent
- [ ] Implement `<tt-event-type-filter>` WebComponent with color legend
- [ ] Implement `<tt-event-detail-panel>` WebComponent
- [ ] Wire inter-component communication via CustomEvents (`event-selected`, `filter-changed`, `position-changed`)

## Testing Tasks

- [ ] Test timeline renders events in order
- [ ] Test zoom and pan via `<tt-timeline-controls>`
- [ ] Test `event-selected` CustomEvent triggers detail panel
- [ ] Test `filter-changed` CustomEvent updates timeline
