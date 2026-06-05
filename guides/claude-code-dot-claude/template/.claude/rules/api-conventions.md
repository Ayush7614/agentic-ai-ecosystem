# API conventions

Applies when editing files under `src/api/`.

- REST paths are kebab-case: `/user-profiles`, not `/userProfiles`.
- Return JSON with `{ "data": ..., "error": null }` on success.
- Use HTTP 422 for validation errors with a `details` array.
- Document new endpoints in `docs/api.md`.
