"""Offline tests for the Tradecraft Lens demo backend (cues backend — no model, no network)."""
import http.client
import json
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lens_server  # noqa: E402

TINA = "There is no alternative. AI is coming whether you like it or not; adapt or be left behind."


def test_grade_text_cues_fires_and_sorts():
    res = lens_server.grade_text(TINA, backend="cues")
    assert isinstance(res, list) and res
    by = {r["lens"]: r for r in res}
    assert by.get("inevitability_framing", {}).get("index", 0) > 0
    assert by["inevitability_framing"]["receipts"]            # has a span receipt
    assert res == sorted(res, key=lambda x: x["index"], reverse=True)   # strongest-first


def test_grade_text_benign_stays_low():
    res = lens_server.grade_text("The committee met Tuesday and approved the quarterly budget.",
                                 backend="cues")
    assert res[0]["index"] < 35     # nothing reaches 'notable' on plain minutes


def test_http_endpoints():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), lens_server._Handler)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        c = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        c.request("GET", "/healthz")
        assert c.getresponse().status == 200
        c.request("POST", "/grade-text",
                  body=json.dumps({"text": TINA, "backend": "cues"}),
                  headers={"Content-Type": "application/json"})
        r = c.getresponse()
        assert r.status == 200
        d = json.loads(r.read())
        assert d["backend"] == "cues" and any(l["index"] > 0 for l in d["lenses"])
        # empty text -> 400
        c.request("POST", "/grade-text", body=json.dumps({"text": ""}),
                  headers={"Content-Type": "application/json"})
        assert c.getresponse().status == 400
    finally:
        srv.shutdown()
