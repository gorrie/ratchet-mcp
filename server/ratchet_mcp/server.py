"""Ratchet MCP server entry point.

Uses the official MCP Python SDK (https://github.com/modelcontextprotocol/python-sdk).
Run with ``python -m ratchet_mcp.server`` or via the ``ratchet-mcp`` console
script. Communicates over stdio by default; the SDK handles framing.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from . import queries
from .data import Graph
from .littlesis import get_relationships, search_entity

logging.basicConfig(level=logging.INFO, format="%(levelname)s ratchet-mcp: %(message)s")

mcp = FastMCP("ratchet")
_graph: Graph | None = None


def graph() -> Graph:
    """Lazy-load the dataset on first tool call (avoids load on import)."""
    global _graph
    if _graph is None:
        _graph = Graph.load()
        logging.info(
            "Loaded %d people, %d institutions, %d edges",
            len(_graph.people), len(_graph.institutions), len(_graph.edges),
        )
    return _graph


@mcp.tool()
def query_cohort(
    sector: str | None = None,
    admin: str | None = None,
    network: str | None = None,
    play: str | None = None,
    actor: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Filter the named-persons dataset by any combination of dimensions.

    Each filter is AND-ed. See ``docs/PLAYS.md`` and ``docs/ACTORS.md``
    for the closed vocabulary on the ``play`` / ``actor`` fields.
    """
    return queries.query_cohort(
        graph(),
        sector=sector, admin=admin, network=network, play=play, actor=actor, limit=limit,
    )


@mcp.tool()
def get_entity(entity_id: str) -> dict[str, Any] | None:
    """Return the full record (person or institution) for ``entity_id``.

    Includes adjacent node IDs under ``edges``. IDs are short strings
    (e.g. ``"Rubin"``, ``"Treasury"``) — see ``query_cohort`` results
    for the ``id`` field.
    """
    return queries.get_entity(graph(), entity_id)


@mcp.tool()
def who_connects(a: str, b: str, max_hops: int = 4) -> list[list[str]]:
    """Find all shortest paths between two entity IDs, up to ``max_hops``.

    Useful for "what connects Person X to Institution Y?" questions.
    Returns paths as lists of IDs; empty list if no path exists.
    """
    return queries.who_connects(graph(), a, b, max_hops=max_hops)


@mcp.tool()
def find_overlap(
    plays: list[str] | None = None,
    actors: list[str] | None = None,
    networks: list[str] | None = None,
    admins: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Find persons tagged with EVERY supplied tag across the supplied
    dimensions. The headline query for the book's thesis: who runs
    multiple staffing plays / touches multiple control-grid actors?

    Example: ``find_overlap(actors=["tap", "backdoor"])``.
    """
    return queries.find_overlap(
        graph(), plays=plays, actors=actors, networks=networks, admins=admins,
    )


@mcp.tool()
def list_plays_for(person_id: str) -> list[str]:
    """Return the play tags on a single person."""
    return queries.list_plays_for(graph(), person_id)


@mcp.tool()
def list_players_for(play: str | None = None, actor: str | None = None) -> list[dict[str, Any]]:
    """Return all persons tagged with a given play OR actor.

    Pass exactly one argument.
    """
    return queries.list_players_for(graph(), play=play, actor=actor)


@mcp.tool()
def find_in_administration(admin: str) -> list[dict[str, Any]]:
    """All persons in the dataset who served in the named administration.

    Administrations: ``carter``, ``reagan``, ``bush1``, ``clinton``,
    ``bush2``, ``obama``, ``trump1``, ``biden``, ``trump2``.
    """
    return queries.find_in_administration(graph(), admin)


@mcp.tool()
def list_clusters() -> list[dict[str, Any]]:
    """List all saved cluster definitions (named thesis-relevant queries).

    Each cluster has an id, label, summary, the Ratchet click(s) it
    illuminates, and a book-chapter pointer. Use ``apply_cluster`` to
    execute a named cluster and return its members.

    Examples: ``tap-backdoor-trinity`` (the surveillance-state cluster),
    ``treasury-vault-loop`` (Wall Street -> Treasury revolver),
    ``federalist-judicial-pipeline``, ``ts-fbi-bridge``.
    """
    return queries.list_clusters(graph())


@mcp.tool()
def apply_cluster(cluster_id: str) -> dict[str, Any]:
    """Execute a saved cluster query and return its members + metadata.

    Cluster definitions live in ``server/data/clusters.json``. Adding
    persons to the dataset automatically updates cluster membership;
    cluster definitions only need editing when a NEW pattern is named.

    Use ``list_clusters`` to see available cluster ids.
    """
    return queries.apply_cluster(graph(), cluster_id)


@mcp.tool()
async def enrich_from_littlesis(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search LittleSis (Public Accountability Initiative) for a named
    person or organization and return matching entities.

    Results carry LittleSis's own IDs, summaries, and primary types. Use
    these when verifying or expanding records in the Ratchet dataset.
    Network call; respects a 10s timeout.
    """
    return await search_entity(query, limit=limit)


@mcp.tool()
async def littlesis_relationships(entity_id: int, limit: int = 20) -> list[dict[str, Any]]:
    """Fetch the LittleSis relationship records for an entity by ID.

    Use after ``enrich_from_littlesis`` to walk an entity's edges.
    """
    return await get_relationships(entity_id, limit=limit)


def main() -> None:
    """Console entry point: run the MCP server over stdio."""
    asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    main()
