# S6.11 — Server Configuration View: Tasks

## Implementation Tasks
- [ ] Create `templates/admin/configuration.html` with WebComponent tags
- [ ] Implement `<tt-config-table>` WebComponent with pending change tracking
- [ ] Implement `<tt-config-editor>` WebComponent with type-appropriate inputs and client-side validation
- [ ] Implement `<tt-config-toolbar>` WebComponent with Apply/Revert buttons
- [ ] Wire `value-changed`, `apply-changes`, `revert-changes` CustomEvents
- [ ] Add admin role guard

## Testing Tasks
- [ ] Test configuration table displays all keys with defaults
- [ ] Test inline editing with validation
- [ ] Test Apply Changes submits all pending values
- [ ] Test Revert Changes restores original values
- [ ] Test invalid value shows inline error
- [ ] Test non-admin user is denied access
