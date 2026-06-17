# 10 Steps to Build an ML Model — Visual Blog Pack

Original blog content and animated diagrams for a **10-step** machine learning lifecycle article (expandable from the common **6 macro stage** framing).

## Contents

| Asset | Purpose |
|-------|---------|
| [BLOG.md](./BLOG.md) | Full publish-ready article — 10 steps, FAQ, GIF map |
| `assets/blog-poster-1200x600.png` | Hero / Medium / general blog (**PNG**) |
| `assets/blog-poster-linkedin-1200x627.png` | **LinkedIn article & link preview** (1200×627) |
| `assets/gif-01-pipeline-overview.gif` | Macro pipeline overview |
| `assets/gif-mix-6-steps.gif` | **All 6 steps in one loop** (~12s) — great for Medium hero or LinkedIn |
| `assets/gif-02-problem-framing.gif` | Steps 1–2 — problem & KPIs |
| `assets/gif-03-data-prep-funnel.gif` | Steps 3–6 — data pipeline |
| `assets/gif-04-model-selection-matrix.gif` | Step 7 — model choice |
| `assets/gif-05-train-loop.gif` | Step 8 — train & tune |
| `assets/gif-06-evaluation-dashboard.gif` | Step 9 — evaluate & slice |
| `assets/gif-07-deploy-monitor.gif` | Step 10 — deploy & monitor |

## 6 vs 10 steps

- **6 macro stages** — good for executive summaries and GIF 1 (Problem → Deploy).
- **10 steps** — what the blog teaches; splits data prep and adds feasibility, EDA, features, and leakage as first-class steps.

## Quick start

```bash
cd guides/ml-model-6-steps/assets
python3 render_blog_poster.py    # 1200×600 PNG hero
python3 render_gif_05_07.py all    # re-render GIFs 5–7
```

Part of the [Agentic AI Ecosystem](https://github.com/Ayush7614/agentic-ai-ecosystem).
