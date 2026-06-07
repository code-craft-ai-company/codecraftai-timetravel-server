# S6.10 — Credential Management View: Design

## Technical Architecture

### Template: `templates/admin/credentials.html`

### WebComponents

| Component | Tag | Description |
|---|---|---|
| `CredentialTable` | `<tt-credential-table>` | Data table of credentials with action buttons per row |
| `CredentialCreateForm` | `<tt-credential-create-form>` | Form to create a new credential with label and optional expiration |
| `TokenDisplayModal` | `<tt-token-display-modal>` | One-time display of plaintext token with copy button |
| `CredentialActions` | `<tt-credential-actions>` | Per-row action buttons: Rotate, Revoke, Delete |

### Component Communication
- `<tt-credential-create-form>` dispatches `credential-created` CustomEvent with the new token.
- `<tt-token-display-modal>` listens for `credential-created` and `credential-rotated` to show the token.
- `<tt-credential-actions>` dispatches `credential-rotated`, `credential-revoked`, `credential-deleted`.
- `<tt-credential-table>` listens for all credential events to refresh the table.

### Module Layout
```
source/site/ccai/timetravelwebsite/static/js/components/
    tt-credential-table.js
    tt-credential-create-form.js
    tt-token-display-modal.js
    tt-credential-actions.js
```

### Data Source
- `GET /api/v1/credentials`, `POST /api/v1/credentials`, etc. (S5.6)

### Dependencies
- S5.6 (Credential Management API), S7.3 (admin role check)
