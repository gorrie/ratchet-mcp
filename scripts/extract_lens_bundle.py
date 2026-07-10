"""Export the tradecraft TEXT lenses to a client-side JSON bundle for the Tradecraft Lens UI.

The deployed Lens grades via the LLM backend (the meaningful, context-verified read). This bundle powers
the OPEN + REPEATABLE in-browser layer: the deterministic cue-floor grader runs client-side off these
taxonomies (cues, weights, grading config) so anyone can paste text and get an instant, reproducible read
with the methodology fully visible — no backend, nothing hidden. The LLM read is the upgrade, not the
gate. Output: website/static/tech/lens-bundle.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
OUT = ROOT.parents[1] / "website" / "static" / "tech" / "lens-bundle.json"


def main():
    from ratchet_mcp.texts import _import_tradecraft, _tradecraft_detectors_dir
    load_lenses, _, text_lenses = _import_tradecraft()
    lenses = text_lenses(load_lenses(_tradecraft_detectors_dir()))
    bundle = []
    for t in lenses.values():
        c = t.config
        bundle.append({
            "id": t.id, "name": t.name, "description": t.description,
            "config": {"mpt": c.marker_present_threshold, "wb": c.w_breadth, "wi": c.w_intensity,
                       "wd": c.w_density, "cap": c.density_cap_per_1k,
                       "tiers": [{"min": x["min"], "label": x["label"]} for x in c.tiers]},
            "markers": [{"id": m.id, "name": m.name, "bw": m.base_weight,
                         "detections": [{"id": d.id, "weight": d.weight, "definition": d.definition,
                                         "cues": d.cues} for d in m.detections]}
                        for m in t.markers],
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
    cues = sum(len(d["cues"]) for L in bundle for m in L["markers"] for d in m["detections"])
    print(f"{len(bundle)} lenses, {cues} cues -> {OUT}")


if __name__ == "__main__":
    main()
