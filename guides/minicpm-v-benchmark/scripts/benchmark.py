#!/usr/bin/env python3
"""Benchmark MiniCPM-V 4.6 vs Qwen3.5-0.8B vs Gemma4-E2B on a 16 GB Mac.

Measures: disk size, text TTFT, tokens/sec, vision latency, and response quality snippets.
Writes results/benchmark.json and results/report.md.

Usage:
  python scripts/benchmark.py
  python scripts/benchmark.py --models minicpm-v4.6,qwen3.5:0.8b
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples" / "benchmark_card.png"
RESULTS_DIR = ROOT / "results"
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")

TEXT_PROMPT = (
    "Explain cross-validation in machine learning in exactly three short sentences. "
    "Be precise and concise."
)
VISION_PROMPT = "Read all visible text in this image and list the model names mentioned."

# Models with vision support (Ollama tags)
VISION_MODELS = {"minicpm-v4.6", "gemma4:e2b", "minicpm-v4.6:latest", "gemma4:e2b:latest"}


@dataclass
class TextBench:
    ttft_ms: float | None = None
    total_ms: float | None = None
    eval_count: int = 0
    tokens_per_sec: float | None = None
    preview: str = ""
    error: str = ""


@dataclass
class VisionBench:
    total_ms: float | None = None
    preview: str = ""
    skipped: bool = False
    error: str = ""


@dataclass
class ModelResult:
    model: str
    size_gb: float | None = None
    installed: bool = False
    text: TextBench = field(default_factory=TextBench)
    vision: VisionBench = field(default_factory=VisionBench)


def _installed_models() -> dict[str, dict]:
    try:
        with httpx.Client(timeout=10) as c:
            r = c.get(f"{OLLAMA_HOST}/api/tags")
            r.raise_for_status()
            out = {}
            for m in r.json().get("models", []):
                name = m.get("name", "")
                out[name] = m
                base = name.split(":")[0]
                out.setdefault(base, m)
            return out
    except Exception as exc:  # noqa: BLE001
        print(f"Ollama unavailable: {exc}", file=sys.stderr)
        return {}


def _pull_model(model: str) -> bool:
    print(f"  Pulling {model} …")
    proc = subprocess.run(["ollama", "pull", model], capture_output=True, text=True)
    return proc.returncode == 0


def _size_gb(meta: dict) -> float | None:
    size = meta.get("size")
    if size:
        return round(size / (1024**3), 2)
    return None


def _bench_text(model: str) -> TextBench:
    bench = TextBench()
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": TEXT_PROMPT}],
        "stream": True,
        "options": {"num_predict": 120},
    }
    start = time.perf_counter()
    ttft = None
    parts: list[str] = []
    eval_count = 0
    try:
        with httpx.Client(timeout=180) as client:
            with client.stream("POST", f"{OLLAMA_HOST}/api/chat", json=payload) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    data = json.loads(line)
                    if data.get("done"):
                        eval_count = data.get("eval_count") or eval_count
                        if not parts and data.get("message", {}).get("content"):
                            parts.append(data["message"]["content"])
                        break
                    chunk = (data.get("message") or {}).get("content") or ""
                    if not chunk:
                        chunk = (data.get("message") or {}).get("thinking") or ""
                    if chunk:
                        if ttft is None:
                            ttft = time.perf_counter() - start
                        parts.append(chunk)
        total = time.perf_counter() - start
        text = "".join(parts).strip()
        bench.ttft_ms = round((ttft or total) * 1000, 1)
        bench.total_ms = round(total * 1000, 1)
        bench.eval_count = eval_count or max(1, len(text.split()))
        gen_sec = (total - (ttft or 0)) if ttft else total
        if gen_sec > 0 and bench.eval_count:
            bench.tokens_per_sec = round(bench.eval_count / gen_sec, 1)
        bench.preview = text[:280]
    except Exception as exc:  # noqa: BLE001
        bench.error = str(exc)
    return bench


def _encode_image(path: Path) -> str:
    import base64

    return base64.b64encode(path.read_bytes()).decode("ascii")


def _bench_vision(model: str, image: Path) -> VisionBench:
    bench = VisionBench()
    base = model.split(":")[0]
    if model not in VISION_MODELS and base not in {v.split(":")[0] for v in VISION_MODELS}:
        if "minicpm" not in model and "gemma" not in model:
            bench.skipped = True
            bench.error = "text-only model"
            return bench
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": VISION_PROMPT, "images": [_encode_image(image)]}],
        "stream": False,
        "options": {"num_predict": 100},
    }
    start = time.perf_counter()
    try:
        with httpx.Client(timeout=180) as client:
            r = client.post(f"{OLLAMA_HOST}/api/chat", json=payload)
            r.raise_for_status()
            msg = r.json().get("message") or {}
            content = msg.get("content") or msg.get("thinking") or ""
        bench.total_ms = round((time.perf_counter() - start) * 1000, 1)
        bench.preview = content[:280].strip()
    except Exception as exc:  # noqa: BLE001
        bench.error = str(exc)
    return bench


def _write_report(results: list[ModelResult], path: Path) -> None:
    lines = [
        "# Edge Model Benchmark — 16 GB Mac",
        "",
        "Generated by `scripts/benchmark.py` against local Ollama.",
        "",
        "## Summary table",
        "",
        "| Model | Size (GB) | TTFT (ms) | tok/s | Vision (ms) | Vision |",
        "|-------|-----------|-----------|-------|-------------|--------|",
    ]
    for r in results:
        t, v = r.text, r.vision
        ttft = t.ttft_ms if t.ttft_ms is not None else "—"
        tps = t.tokens_per_sec if t.tokens_per_sec is not None else "—"
        vms = v.total_ms if v.total_ms is not None else ("skip" if v.skipped else "—")
        vis = "✅" if v.total_ms else ("—" if v.skipped else "❌")
        lines.append(
            f"| `{r.model}` | {r.size_gb or '—'} | {ttft} | {tps} | {vms} | {vis} |"
        )
    lines.extend(["", "## Text preview (first model line each)", ""])
    for r in results:
        if r.text.preview:
            lines.append(f"### {r.model}\n\n> {r.text.preview}\n")
    path.write_text("\n".join(lines) + "\n")


def run(models: list[str], skip_pull: bool) -> list[ModelResult]:
    if not SAMPLES.is_file():
        subprocess.check_call([sys.executable, str(ROOT / "generate_sample.py")])

    installed = _installed_models()
    results: list[ModelResult] = []

    for model in models:
        print(f"\n==> {model}")
        mr = ModelResult(model=model)
        meta = installed.get(model) or installed.get(model.split(":")[0])
        if not meta:
            if skip_pull:
                mr.text.error = "not installed (set SKIP_PULL=0 to pull)"
                results.append(mr)
                continue
            if not _pull_model(model):
                mr.text.error = "pull failed"
                results.append(mr)
                continue
            installed = _installed_models()
            meta = installed.get(model) or installed.get(model.split(":")[0])

        mr.installed = True
        mr.size_gb = _size_gb(meta or {})
        print("  Text benchmark …")
        mr.text = _bench_text(model)
        print(f"    TTFT {mr.text.ttft_ms} ms · {mr.text.tokens_per_sec} tok/s")
        print("  Vision benchmark …")
        mr.vision = _bench_vision(model, SAMPLES)
        if mr.vision.skipped:
            print("    skipped (text-only)")
        elif mr.vision.total_ms:
            print(f"    {mr.vision.total_ms} ms")
        results.append(mr)

    return results


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--models",
        default=os.environ.get("BENCHMARK_MODELS", "minicpm-v4.6,qwen3.5:0.8b,gemma4:e2b"),
    )
    p.add_argument("--skip-pull", action="store_true", default=os.environ.get("SKIP_PULL", "1") == "1")
    args = p.parse_args()
    models = [m.strip() for m in args.models.split(",") if m.strip()]

    RESULTS_DIR.mkdir(exist_ok=True)
    results = run(models, args.skip_pull)
    payload = [asdict(r) for r in results]
    json_path = RESULTS_DIR / "benchmark.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n")
    _write_report(results, RESULTS_DIR / "report.md")
    print(f"\nWrote {json_path} and {RESULTS_DIR / 'report.md'}")


if __name__ == "__main__":
    main()
