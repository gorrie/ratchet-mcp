"""LittleSis API client.

LittleSis (https://littlesis.org/) is the Public Accountability Initiative's
open, no-auth influence-network database. We hit the public REST API and
return raw JSON; the MCP layer surfaces it as enrichment data. Citations
made via this tool are at the record level — see ``docs/CITATIONS.md``.

API docs: https://littlesis.org/api
"""
from __future__ import annotations

from typing import Any

import httpx

BASE_URL = "https://littlesis.org/api"
USER_AGENT = "ratchet-mcp/0.1 (https://github.com/gorrie/ratchet-mcp)"


async def search_entity(query: str, *, limit: int = 10) -> list[dict[str, Any]]:
    """Search LittleSis for persons or organizations matching ``query``.

    Returns the raw ``data`` array from the API response (one record per
    matched entity). Empty list if nothing matched or the API is down.
    """
    async with httpx.AsyncClient(timeout=10.0, headers={"User-Agent": USER_AGENT}) as c:
        try:
            r = await c.get(f"{BASE_URL}/entities/search", params={"q": query})
            r.raise_for_status()
        except (httpx.HTTPError, httpx.TimeoutException):
            return []
        payload = r.json()
    return (payload.get("data") or [])[:limit]


async def get_relationships(entity_id: int, *, limit: int = 20) -> list[dict[str, Any]]:
    """Fetch the LittleSis relationships for an entity by ID."""
    async with httpx.AsyncClient(timeout=10.0, headers={"User-Agent": USER_AGENT}) as c:
        try:
            r = await c.get(f"{BASE_URL}/entities/{entity_id}/relationships")
            r.raise_for_status()
        except (httpx.HTTPError, httpx.TimeoutException):
            return []
        payload = r.json()
    return (payload.get("data") or [])[:limit]
