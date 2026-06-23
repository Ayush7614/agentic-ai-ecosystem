#!/usr/bin/env python3
"""MiniCPM-V MCP server — vision tools for Cursor, Claude Desktop, and Hermes.

Exposes three tools over MCP:

    describe_image(path, question?)  → general image understanding
    ocr_document(path)               → structured text extraction
    compare_images(path_a, path_b, focus?) → side-by-side visual diff

Powered by MiniCPM-V 4.6 via Ollama (~1.6 GB, text + image, 256K context).

Run:  python examples/server.py        # stdio transport (for MCP hosts)
"""
from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

try:
    from . import vision_backend as vb
except ImportError:  # pragma: no cover
    import vision_backend as vb  # type: ignore

mcp = FastMCP("minicpm-vision")

DESCRIBE_DEFAULT = (
    "Describe this image in detail. Include objects, text visible, layout, "
    "colors, and anything notable for a developer reviewing a screenshot."
)
OCR_PROMPT = (
    "Extract all readable text from this document or screenshot. "
    "Preserve structure with markdown headings and bullet lists where appropriate. "
    "If tables are present, format them as markdown tables."
)
COMPARE_DEFAULT = (
    "Compare these two images. List similarities and differences. "
    "Note UI changes, text changes, and layout shifts."
)


def _resolve(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(f"Not a file: {p}")
    return p


def _tool_result(text: str, **meta) -> str:
    return json.dumps({"result": text, **meta}, indent=2)


@mcp.tool()
def describe_image(path: str, question: str = "") -> str:
    """Describe or answer questions about a single image using MiniCPM-V 4.6.

    Args:
        path: Absolute or relative path to a PNG, JPG, WEBP, or GIF file.
        question: Optional specific question about the image. Leave empty for
            a general description.

    Returns JSON with the model's answer and metadata.
    """
    try:
        img = _resolve(path)
        prompt = question.strip() or DESCRIBE_DEFAULT
        answer = vb.chat_vision(prompt, [img])
        return _tool_result(answer, tool="describe_image", path=str(img), model=vb.VISION_MODEL)
    except (FileNotFoundError, vb.VisionError) as exc:
        return json.dumps({"error": str(exc)}, indent=2)


@mcp.tool()
def ocr_document(path: str) -> str:
    """OCR a document, receipt, whiteboard photo, or screenshot to markdown text.

    Args:
        path: Absolute or relative path to the image file.

    Returns JSON with extracted text in markdown format.
    """
    try:
        img = _resolve(path)
        answer = vb.chat_vision(OCR_PROMPT, [img])
        return _tool_result(answer, tool="ocr_document", path=str(img), model=vb.VISION_MODEL)
    except (FileNotFoundError, vb.VisionError) as exc:
        return json.dumps({"error": str(exc)}, indent=2)


@mcp.tool()
def compare_images(path_a: str, path_b: str, focus: str = "") -> str:
    """Compare two images and report visual differences.

    Args:
        path_a: Path to the first image (e.g. before screenshot).
        path_b: Path to the second image (e.g. after screenshot).
        focus: Optional aspect to focus on (e.g. "navigation bar", "error message").

    Returns JSON with a structured comparison.
    """
    try:
        a, b = _resolve(path_a), _resolve(path_b)
        prompt = COMPARE_DEFAULT
        if focus.strip():
            prompt += f"\n\nFocus especially on: {focus.strip()}"
        answer = vb.chat_vision(prompt, [a, b])
        return _tool_result(
            answer,
            tool="compare_images",
            path_a=str(a),
            path_b=str(b),
            model=vb.VISION_MODEL,
        )
    except (FileNotFoundError, vb.VisionError) as exc:
        return json.dumps({"error": str(exc)}, indent=2)


@mcp.resource("minicpm-vision://model")
def model_info() -> str:
    """Capability hint: which vision model and host this server uses."""
    status = vb.health_check()
    return json.dumps(
        {
            "model": vb.VISION_MODEL,
            "ollama_host": vb.OLLAMA_HOST,
            "tools": ["describe_image", "ocr_document", "compare_images"],
            "status": status,
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
