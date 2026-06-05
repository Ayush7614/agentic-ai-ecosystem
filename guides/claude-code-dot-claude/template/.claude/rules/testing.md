# Testing rules

Applies when editing files under `tests/` or `src/`.

- Use **pytest**; no unittest-style classes unless the file already uses them.
- Name tests `test_<behavior>_<condition>`.
- Prefer fixtures in `tests/conftest.py` over duplicated setup.
- After code changes, run: `pytest -q`
