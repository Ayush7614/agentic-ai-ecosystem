"""LitServe vision API — MiniCPM-V 4.6 photo understanding for OpenClaw."""
from __future__ import annotations

import os
from pathlib import Path

import litserve as ls
from dotenv import load_dotenv

import vision_backend as vb

load_dotenv()

PORT = int(os.getenv("PORT", "8002"))

STRUCTURED_PROMPT = """Analyze the image and answer the user's question.
Return markdown with these sections when relevant:
## Summary
(one paragraph)

## Details
(bullet points)

## Text found
(any visible text, or "none")

## Suggested reply
(a short message suitable for Telegram/WhatsApp)
"""


class VisionPhotoAPI(ls.LitAPI):
    def setup(self, device):
        self.model = vb.VISION_MODEL

    def decode_request(self, request):
        return {
            "query": (request.get("query") or "What is in this photo?").strip(),
            "image_path": (request.get("image_path") or "").strip(),
        }

    def predict(self, inputs):
        path = Path(inputs["image_path"]).expanduser().resolve()
        prompt = f"{STRUCTURED_PROMPT}\n\nUser question: {inputs['query']}"
        try:
            answer = vb.chat_vision(prompt, [path])
            return {"output": answer, "model": self.model, "image_path": str(path)}
        except vb.VisionError as exc:
            return {"error": str(exc), "model": self.model}

    def encode_response(self, output):
        return output


if __name__ == "__main__":
    server = ls.LitServer(VisionPhotoAPI(), accelerator="auto", timeout=False)
    print(f"Vision API on http://127.0.0.1:{PORT}/predict  (model: {vb.VISION_MODEL})")
    server.run(port=PORT)
