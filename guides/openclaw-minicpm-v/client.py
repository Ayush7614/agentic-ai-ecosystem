#!/usr/bin/env python3
"""CLI client for the vision photo API."""
from __future__ import annotations

import argparse
import json
import os
import urllib.request

DEFAULT_URL = os.environ.get("VISION_API_URL", "http://127.0.0.1:8002")


def main() -> None:
    p = argparse.ArgumentParser(description="Query local MiniCPM-V vision API")
    p.add_argument("--image", required=True, help="Path to image file")
    p.add_argument("--query", default="Describe this photo in detail.")
    p.add_argument("--url", default=f"{DEFAULT_URL.rstrip('/')}/predict")
    args = p.parse_args()

    body = json.dumps({"query": args.query, "image_path": args.image}).encode()
    req = urllib.request.Request(args.url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode())
    print(data.get("output") or data.get("error") or data)


if __name__ == "__main__":
    main()
