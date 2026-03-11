# S6.10 — Credential Management View: Tasks

## Implementation Tasks
- [ ] Create `templates/admin/credentials.html` with WebComponent tags
- [ ] Implement `<tt-credential-table>` WebComponent
- [ ] Implement `<tt-credential-create-form>` WebComponent
- [ ] Implement `<tt-token-display-modal>` WebComponent with copy button
- [ ] Implement `<tt-credential-actions>` WebComponent (Rotate, Revoke, Delete)
- [ ] Wire CustomEvents for credential lifecycle operations
- [ ] Add admin role guard

## Testing Tasks
- [ ] Test credential table renders correctly
- [ ] Test create form dispatches event and shows token modal
- [ ] Test rotate generates new token and shows modal
- [ ] Test revoke and delete update table
- [ ] Test non-admin user is denied access
