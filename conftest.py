"""Skip the tradecraft-integration tests when tradecraft is not available.

`tradecraft` is an optional sibling: `ratchet_mcp.texts` prefers an installed package, falls
back to a `TRADECRAFT_PATH` override, then to a `tradecraft/` directory beside a combined
workspace checkout. A standalone clone has none of those, which is supported — those tests
should skip, not fail.

The list is explicit rather than inferred; `test_skip_list_is_current` fails if a listed test
disappears, so the exemptions cannot rot.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "server"))

#: Tests that exercise the tradecraft integration. Node id suffixes, matched against the end
#: of the pytest node id so the list is independent of how the suite is invoked.
TRADECRAFT_TESTS = (
    "lens/test_lens.py::test_grade_text_cues_fires_and_sorts",
    "lens/test_lens.py::test_grade_text_benign_stays_low",
    "lens/test_lens.py::test_http_endpoints",
    "server/tests/test_gaps.py::test_import_tradecraft_env_path",
    "server/tests/test_server.py::test_grade_person_texts_tool",
    "server/tests/test_server.py::test_profile_person_tool",
    "server/tests/test_texts.py::test_populated_subject_graded_per_lens",
    "server/tests/test_texts.py::test_profile_person_combined_two_lanes",
    "server/tests/test_texts.py::test_verified_receipts_populated",
)

REASON = ("tradecraft is not importable here. This is an optional integration: install the "
          "package, set TRADECRAFT_PATH, or check out tradecraft/ beside this repo. The rest "
          "of the suite covers the server and dataset on their own.")


def _tradecraft_available() -> bool:
    try:
        from ratchet_mcp import texts  # noqa: WPS433
        texts._import_tradecraft()
        return True
    except Exception:
        return False


AVAILABLE = _tradecraft_available()


def _norm(nodeid: str) -> str:
    return nodeid.replace(os.sep, "/")


def pytest_collection_modifyitems(config, items):
    if AVAILABLE:
        return
    mark = pytest.mark.skip(reason=REASON)
    for item in items:
        nid = _norm(item.nodeid)
        if any(nid.endswith(t) for t in TRADECRAFT_TESTS):
            item.add_marker(mark)


def test_skip_list_is_current(request):
    """Every entry in TRADECRAFT_TESTS still names a test that exists.

    A stale skip entry is an exemption for a test that no longer runs, which is the same
    failure mode as a stale known-issues registry: it hides the next real problem.
    """
    collected = {_norm(i.nodeid) for i in request.session.items}
    missing = [t for t in TRADECRAFT_TESTS
               if not any(n.endswith(t) for n in collected)]
    assert not missing, (
        "TRADECRAFT_TESTS names tests that no longer exist: %s. Remove them." % missing)
