---
name: vision-photo
description: Analyze photos with local MiniCPM-V 4.6 — OCR, describe, summarize receipts and screenshots via the vision LitServe API.
user-invocable: true
metadata:
  {"openclaw":{"emoji":"📷","requires":{"bins":["curl","jq"],"env":["VISION_API_URL"]},"primaryEnv":"VISION_API_URL"}}
---

# Vision Photo (MiniCPM-V 4.6)

Use when the user sends a **photo**, **screenshot**, **receipt**, or asks you to **read an image**.
Do not use for plain text chat — answer those directly with MiniCPM-V.

## When to invoke

- User attaches or references an image file path
- "What does this receipt say?", "Read this screenshot", "Describe this photo"
- OCR, UI review, or visual Q&A on local files

## How to invoke

1. Get the **absolute path** to the image (OpenClaw media downloads often land under workspace media dirs).

2. Run:

```bash
"{baseDir}/scripts/vision_query.sh" "/absolute/path/to/image.jpg" "USER_QUESTION"
```

3. Return the **Suggested reply** section to the channel if present; otherwise summarize the API output for Telegram/WhatsApp.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `VISION_API_URL` | `http://127.0.0.1:8002` | LitServe vision API base URL |

Start the API: `python vision_server.py` in `guides/openclaw-minicpm-v`.

## Notes

- Vision calls take **5–60 s** on a laptop while MiniCPM-V loads.
- Keep **MiniCPM-V 4.6** as the OpenClaw chat model — same Ollama tag for planning and vision.
- Pair with [MiniCPM-V MCP](../minicpm-v-mcp-server/) for Cursor-side vision tools.
