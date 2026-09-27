"""Every Wikidata QID in the dataset was verified to be the entity it is attached to.

2026-09-26: 255 of 404 QIDs pointed at unrelated items (Larry Page's was Steve Wozniak's), and
Jerome Powell's record cited Colin Powell's Wikipedia page and Wikidata item. Nothing compared
an ID to the name it sat on. scripts/verify_qids.py --refresh checks each against the Wikidata
API and records it; this test fails when a QID in the data was never checked, or moved record.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("verify_qids", ROOT / "scripts" / "verify_qids.py")
VQ = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(VQ)


def test_every_qid_was_verified_against_wikidata():
    assert VQ.check() == 0, "run: python scripts/verify_qids.py --refresh"


def test_name_matching_accepts_formal_names_and_rejects_other_people():
    assert VQ.names_match("Tom Donilon", {"label": "Thomas E. Donilon"})
    assert VQ.names_match("Borge Brende", {"label": "Børge Brende"})
    assert not VQ.names_match("Jerome Powell", {"label": "Colin Powell", "enwiki": "Colin Powell"})
    assert not VQ.names_match("Larry Page", {"label": "Steve Wozniak"})
