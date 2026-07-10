"""The texts-by-person lane: grade a dataset person from the texts they authored.

The graph half of this project profiles a person by their career/funding TOPOLOGY. This module is
the prose half: it stores verbatim texts attributed to dataset persons (speeches, op-eds, posts,
testimony, with a source URL) and runs the Tradecraft TEXT lenses over them — graded per subject,
NEVER blended across lenses, never a verdict. The grading engine lives in the sibling ``tradecraft``
package (the single source of truth for lenses + grader); this module is only the store + the bridge.

Store: ``<data-dir>/texts.jsonl``, one JSON object per line:

    {"person_id": "<ratchet person id>",   # required; must match a person in people.jsonl
     "id": "<short text id>",               # optional; defaults to person_id#N
     "text": "<verbatim text>",             # required
     "url": "<source url>",                 # optional but expected (the receipt)
     "date": "YYYY-MM-DD"}                  # optional; enables the escalation timeline

Texts must be REAL and SOURCED — this is an evidence store about real people. Do not invent quotes.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from .data import Graph, _data_dir


def texts_path() -> Path:
    """Resolve the texts store: ``<RATCHET_DATA_DIR or data dir>/texts.jsonl``."""
    return _data_dir() / "texts.jsonl"


def load_texts(person_id: str | None = None) -> list[dict[str, Any]]:
    """Load the texts store, optionally filtered to one ``person_id``. Empty list if no store."""
    path = texts_path()
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if person_id and rec.get("person_id") != person_id:
                continue
            out.append(rec)
    return out


def _import_tradecraft():
    """Import the sibling ``tradecraft`` package.

    Prefer an installed package; fall back to the dev workspace layout
    (``evil-robots-series/tradecraft``) or a ``TRADECRAFT_PATH`` override.
    Returns the modules needed, or raises ImportError with an actionable hint.
    """
    try:
        from tradecraft.loader import load_lenses  # noqa: F401
        import tradecraft  # noqa: F401
    except ImportError:
        candidates = []
        env = os.environ.get("TRADECRAFT_PATH")
        if env:
            candidates.append(Path(env))
        # texts.py -> ratchet_mcp -> server -> ratchet-mcp -> research -> evil-robots-series
        series_root = Path(__file__).resolve().parents[4]
        candidates.append(series_root / "tradecraft")
        for c in candidates:
            if (c / "tradecraft" / "__init__.py").exists():
                sys.path.insert(0, str(c))
                break
    try:
        from tradecraft.loader import load_lenses
        from tradecraft.subject import grade_person, text_lenses
        return load_lenses, grade_person, text_lenses
    except ImportError as e:  # pragma: no cover - environment dependent
        raise ImportError(
            "The texts-by-person lane needs the 'tradecraft' package. Install it "
            "(`pip install tradecraft`) or set TRADECRAFT_PATH to its repo root "
            "(the dir containing the 'tradecraft/' package)."
        ) from e


def _import_tradecraft_profile():
    """Import the combined-profile + graph-adapter entry points (after _import_tradecraft puts
    tradecraft on the path)."""
    _import_tradecraft()
    from tradecraft.profile import profile_subject
    from tradecraft.adapters import write_ratchet_graph
    return profile_subject, write_ratchet_graph


def _tradecraft_detectors_dir() -> str:
    """The detectors/ dir inside the resolved tradecraft repo."""
    import tradecraft
    pkg = Path(tradecraft.__file__).resolve().parent           # .../tradecraft/tradecraft
    return str(pkg.parent / "detectors")                       # .../tradecraft/detectors


def _plain(obj):
    """Dataclass tree -> JSON-serializable dict (for the MCP return)."""
    if is_dataclass(obj):
        return {k: _plain(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_plain(v) for v in obj]
    return obj


def grade_person_texts(
    graph: Graph,
    person_id: str,
    *,
    backend: str = "cues",
    model: str | None = None,
) -> dict[str, Any]:
    """Run the Tradecraft TEXT lenses over a person's stored texts; aggregate per subject.

    ``backend="cues"`` is the deterministic offline default (no key, no model). Pass
    ``"cloud"``/``"local"``/``"auto"`` for the model read. Returns a per-lens profile + receipts +
    the per-document profiles — never a single blended score, never a verdict.
    """
    person = graph.people.get(person_id)
    if person is None:
        return {"person_id": person_id, "error": "unknown person_id",
                "hint": "use query_cohort / get_entity to find a valid id"}
    texts = load_texts(person_id)
    if not texts:
        return {"person_id": person_id, "label": person.get("label"), "n_texts": 0,
                "note": f"no texts stored for {person_id!r}. Add records to "
                        f"{texts_path().name} (see texts.README.md) to enable this lane."}

    load_lenses, grade_person, _ = _import_tradecraft()
    lenses = load_lenses(_tradecraft_detectors_dir())
    profile, docs = grade_person(lenses, person_id, texts, backend=backend, model=model)
    return {
        "person_id": person_id,
        "label": person.get("label"),
        "backend": backend,
        "n_texts": len(texts),
        "subject": _plain(profile),
        "documents": [_plain(d) for d in docs],
        "note": "Per-lens profile + receipts for human review. Never blended across lenses; "
                "a profile of what the texts exhibit, not a verdict about the person.",
    }


def verified_person_receipts(
    graph: Graph,
    person_id: str,
    *,
    backend: str = "auto",
    model: str | None = None,
) -> dict[str, Any]:
    """Publishable receipts only — the precision path on top of ``grade_person_texts``.

    ``grade_person_texts`` returns the full per-lens profile, INCLUDING the blunt offline cue hits.
    Against short texts those cue hits are mostly context-blind false positives (and some fire on the
    OPPOSITE of the text's meaning), so they are NOT safe to publish on a named real person. This
    function runs ``detect.verified_cue_receipts`` per text: it keeps a cue hit only when a context
    read confirms the AUTHOR genuinely employs the method, defaulting to rejection. It returns the
    small, audited set — each with lens, span, source URL, date, and the verifier's rationale — to be
    human-reviewed before anything is shown publicly. ``cues`` is rejected: verification needs a
    context-reading backend (``auto``/``cloud``/``local``).
    """
    person = graph.people.get(person_id)
    if person is None:
        return {"person_id": person_id, "error": "unknown person_id",
                "hint": "use query_cohort / get_entity to find a valid id"}
    if backend == "cues":
        return {"person_id": person_id, "error": "verification needs a context backend",
                "hint": "use backend='auto'|'cloud'|'local'; 'cues' has no context read to verify with"}
    texts = load_texts(person_id)
    if not texts:
        return {"person_id": person_id, "label": person.get("label"), "n_texts": 0, "receipts": []}

    load_lenses, _, text_lenses = _import_tradecraft()
    from tradecraft.detect import verified_cue_receipts
    lenses = text_lenses(load_lenses(_tradecraft_detectors_dir()))
    receipts: list[dict[str, Any]] = []
    for t in texts:
        body = t.get("text") or ""
        for lens_id, tax in lenses.items():
            for hit in verified_cue_receipts(body, tax, backend=backend, model=model):
                receipts.append({
                    "lens": lens_id,
                    "detection_id": hit.detection_id,
                    "span": hit.span,
                    "confidence": hit.confidence,
                    "rationale": hit.rationale,
                    "url": t.get("url"),
                    "date": t.get("date"),
                })
    return {
        "person_id": person_id,
        "label": person.get("label"),
        "backend": backend,
        "n_texts": len(texts),
        "n_receipts": len(receipts),
        "receipts": receipts,
        "note": "Context-verified receipts only — each confirmed by a model read that the AUTHOR "
                "genuinely employs the method; incidental and opposite-meaning cue hits dropped. For "
                "human review before publication. Never a verdict.",
    }


def profile_person(
    graph: Graph,
    person_id: str,
    *,
    backend: str = "cues",
    model: str | None = None,
) -> dict[str, Any]:
    """The combined two-lane profile: GRAPH lenses on this person's ratchet topology AND the TEXT
    lenses on their stored texts, each lens on its own axis, never blended, never a verdict.

    The graph lane runs both ``network_brokerage`` (betweenness/degree/sector-brokerage) and
    ``revolving_door`` (cross-sector affiliation breadth, annotated as breadth not trajectory since
    the ratchet edges are untyped). The text lane runs the text lenses on the texts store. ``cues``
    is the offline default; pass ``cloud``/``local``/``auto`` for the model read on the text lane.
    """
    person = graph.people.get(person_id)
    if person is None:
        return {"person_id": person_id, "error": "unknown person_id",
                "hint": "use query_cohort / get_entity to find a valid id"}

    profile_subject, write_ratchet_graph = _import_tradecraft_profile()
    texts = [{"id": t.get("id"), "text": t.get("text"), "url": t.get("url"), "date": t.get("date")}
             for t in load_texts(person_id)]

    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    tmp.close()
    try:
        write_ratchet_graph(str(_data_dir()), tmp.name)
        out = profile_subject(person_id, detectors_dir=_tradecraft_detectors_dir(),
                              graph_path=tmp.name, texts=texts or None,
                              backend=backend, model=model)
    finally:
        os.unlink(tmp.name)
    out["label"] = person.get("label")
    out["n_texts"] = len(texts)
    return _plain(out)
