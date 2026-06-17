#!/usr/bin/env python3
"""Minimal MCP weather server — demonstrates tools + dynamic JSON schema."""
from __future__ import annotations

import json
from datetime import date

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-demo")


@mcp.tool()
def get_forecast(location: str, day: str | None = None, unit: str = "celsius") -> str:
    """Return a stub forecast for a city. Supports optional day and temperature unit."""
    day = day or date.today().isoformat()
    temp = 22 if unit == "celsius" else 72
    symbol = "°C" if unit == "celsius" else "°F"
    payload = {
        "location": location,
        "date": day,
        "unit": unit,
        "forecast": f"Sunny, {temp}{symbol}, light wind",
    }
    return json.dumps(payload, indent=2)


@mcp.resource("weather://schema")
def capability_schema() -> str:
    """Human-readable capability notes for clients (demo resource)."""
    return (
        "Tools: get_forecast(location, day?, unit='celsius')\n"
        "Add new optional params without breaking existing hosts — "
        "clients discover schema at connect time."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
