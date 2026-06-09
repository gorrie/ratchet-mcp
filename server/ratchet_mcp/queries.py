"""Query primitives for the Ratchet MCP server.

The tool surface (see ``docs/PROMPTS.md``) maps 1:1 to functions here. Each
function takes a ``Graph`` plus filter kwargs and returns plain dicts /
lists so the MCP layer can hand them straight back to the model.

Filters are intersected (AND), not unioned. Multi-value filters within one
dimension (``admins=["clinton","obama"]``) are unioned within that dimension.
"""
from __future__ import annotations

from collections import deque
from typing import Any, Iterable

from .data import Graph


def _matches_person(rec: dict[str, Any], filters: dict[str, Any]) -> bool:
    """Apply intersection filters to a person record."""
    for key, want in filters.items():
        if want is None:
            continue
        have = rec.get(key, [])
        if isinstance(have, str):
            have = [have]
        if isinstance(want, str):
            if want not in have:
                return False
        else:
            if not set(want) & set(have):
                return False
    return True


def query_cohort(
    g: Graph,
    *,
    sector: str | list[str] | None = None,
    admin: str | list[str] | None = None,
    network: str | list[str] | None = None,
    play: str | list[str] | None = None,
    actor: str | list[str] | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Return persons matching the supplied filters.

    Each filter dimension is a person record field:
      - ``sector``   → ``sector`` (single string)
      - ``admin``    → ``admin`` (list)
      - ``network``  → ``networks`` (list)
      - ``play``     → ``plays`` (list)
      - ``actor``    → ``actors`` (list)

    Filters are AND-ed; values within one filter are OR-ed.
    """
    filters = {
        "sector": sector,
        "admin": admin,
        "networks": network,
        "plays": play,
        "actors": actor,
    }
    out = [p for p in g.people.values() if _matches_person(p, filters)]
    return out[:limit]


def get_entity(g: Graph, entity_id: str) -> dict[str, Any] | None:
    """Return the full record (person or institution) for ``entity_id``."""
    rec = g.entity(entity_id)
    if rec is None:
        return None
    out = dict(rec)
    out["edges"] = g.neighbors_of(entity_id)
    return out


def who_connects(
    g: Graph,
    a: str,
    b: str,
    max_hops: int = 4,
) -> list[list[str]]:
    """All shortest paths between two entity IDs, up to ``max_hops``.

    Returns a list of paths (each a list of node IDs). Empty if no path
    exists within the limit.
    """
    if a not in g.people and a not in g.institutions:
        return []
    if b not in g.people and b not in g.institutions:
        return []
    if a == b:
        return [[a]]

    # BFS layer-by-layer, keep ALL shortest paths.
    frontier: dict[str, list[list[str]]] = {a: [[a]]}
    visited: set[str] = {a}
    for _ in range(max_hops):
        new_frontier: dict[str, list[list[str]]] = {}
        for node, paths in frontier.items():
            for n in g.neighbors_of(node):
                if n in visited:
                    continue
                new_frontier.setdefault(n, []).extend(p + [n] for p in paths)
        if not new_frontier:
            return []
        if b in new_frontier:
            return new_frontier[b]
        visited.update(new_frontier.keys())
        frontier = new_frontier
    return []


def find_overlap(
    g: Graph,
    *,
    plays: Iterable[str] | None = None,
    actors: Iterable[str] | None = None,
    networks: Iterable[str] | None = None,
    admins: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """Return persons who have ALL of the supplied tags across every
    listed dimension. Use this for "same person touched X and Y" queries.

    Example: ``find_overlap(actors=["tap", "backdoor"])`` returns persons
    tagged with both ``tap`` AND ``backdoor`` actors.
    """
    required = {
        "plays": set(plays or []),
        "actors": set(actors or []),
        "networks": set(networks or []),
        "admin": set(admins or []),
    }
    out: list[dict[str, Any]] = []
    for p in g.people.values():
        ok = True
        for field, want in required.items():
            if not want:
                continue
            have = set(p.get(field, []) or [])
            if not want.issubset(have):
                ok = False
                break
        if ok:
            out.append(p)
    return out


def list_plays_for(g: Graph, person_id: str) -> list[str]:
    """Plays tagged on a given person."""
    rec = g.people.get(person_id)
    return list(rec.get("plays", [])) if rec else []


def list_players_for(
    g: Graph,
    *,
    play: str | None = None,
    actor: str | None = None,
) -> list[dict[str, Any]]:
    """People tagged with a given play OR actor.

    Exactly one of ``play`` / ``actor`` must be provided.
    """
    if (play is None) == (actor is None):
        raise ValueError("Pass exactly one of `play` or `actor`")
    field = "plays" if play else "actors"
    want = play if play else actor
    return [p for p in g.people.values() if want in (p.get(field) or [])]


def find_in_administration(g: Graph, admin: str) -> list[dict[str, Any]]:
    """People who served in the named administration.

    Convenience wrapper around ``query_cohort(admin=...)``.
    """
    return query_cohort(g, admin=admin, limit=10_000)


def list_clusters(g: Graph) -> list[dict[str, Any]]:
    """Return all saved cluster definitions (metadata only, no members)."""
    return [
        {k: c.get(k) for k in ("id", "label", "summary", "ratchet_clicks", "book_chapter")}
        for c in g.clusters
    ]


def apply_cluster(g: Graph, cluster_id: str) -> dict[str, Any]:
    """Execute a saved cluster query and return its members + metadata.

    Cluster definitions live in ``server/data/clusters.json`` as
    ``{id, label, summary, query, ...}``. The ``query`` field has
    ``tool`` (one of: ``query_cohort``, ``find_overlap``) and ``args``
    (kwargs for that tool). Optional ``filter_ids`` (only return these
    IDs) and ``filter_sector`` (restrict to a sector) further narrow.

    Returns ``{cluster, members}`` where ``members`` is the list of
    person records, or ``{error}`` if the cluster id is unknown.
    """
    cluster = next((c for c in g.clusters if c["id"] == cluster_id), None)
    if cluster is None:
        return {"error": f"Unknown cluster id: {cluster_id!r}"}
    q = cluster.get("query") or {}
    tool = q.get("tool")
    args = q.get("args") or {}
    if tool == "query_cohort":
        members = query_cohort(g, **args, limit=args.get("limit", 1000))
    elif tool == "find_overlap":
        members = find_overlap(g, **args)
    else:
        return {"error": f"Unsupported cluster tool: {tool!r}"}
    # Optional post-filters
    if "filter_ids" in cluster:
        wanted = set(cluster["filter_ids"])
        members = [m for m in members if m["id"] in wanted]
    if "filter_sector" in cluster:
        members = [m for m in members if m.get("sector") == cluster["filter_sector"]]
    return {
        "cluster": {k: cluster.get(k) for k in ("id", "label", "summary", "ratchet_clicks", "book_chapter")},
        "members": members,
        "member_count": len(members),
    }
