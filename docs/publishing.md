# Publishing guides to GitHub Pages

The public site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and deployed via GitHub Actions on every push to `main`.

## Per-guide URLs

| Guide | Overview | Tutorial |
|-------|----------|----------|
| Qwen Agentic RAG | `/guides/qwen-agentic-rag/` | `/guides/qwen-agentic-rag/tutorial/` |
| OpenClaw + Gemma + RAG | `/guides/openclaw-gemma-rag/` | `/guides/openclaw-gemma-rag/tutorial/` |

## Add a new guide to the site

1. Add the project under `guides/<slug>/` (README + optional `TUTORIAL.md`).
2. Create wrapper pages:

   - `docs/guides/<slug>/index.md` — include `guides/<slug>/README.md`
   - `docs/guides/<slug>/tutorial.md` — include `guides/<slug>/TUTORIAL.md` (if present)

3. Register navigation in `mkdocs.yml` under `nav` → `Guides`.
4. Add a row to `docs/index.md` guide table.
5. Push to `main`; the [Deploy docs](https://github.com/Ayush7614/agentic-ai-ecosystem/actions) workflow publishes automatically.

## Build locally

```bash
./scripts/prepare-docs.sh
pip install -r requirements-docs.txt
mkdocs serve
```

Open http://127.0.0.1:8000/agentic-ai-ecosystem/ (MkDocs uses `site_url` path prefix when set).

## Enable GitHub Pages (one-time)

In the repo **Settings → Pages**, set **Source** to **GitHub Actions**. The workflow creates the deployment; no `gh-pages` branch is required.
