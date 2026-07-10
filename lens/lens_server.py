"""The Tradecraft Lens — local demo backend (flagship component A).

Paste any text -> the tradecraft TEXT lenses read it for influence-method markers, ideology-blind,
method-not-verdict, with the verbatim span + the model's rationale as the receipt. This is the public
instrument the flagship leads with ("here is the tool; see the method yourself").

Stdlib only (http.server) — no Flask dep, matching the project's vanilla ethos. The detector calls an
LLM (cloud via OpenRouter / local Ollama, backend=auto), so this is a served endpoint, not client-side.
Pasted text is UNTRUSTED by definition (a public box); `detect()` already routes it through
`sanitize_untrusted` (prompt-injection fence-break + flag) and frames it as data, never instructions.

Run:  python lens/lens_server.py            # serves http://127.0.0.1:8770
Then open the page or:  curl -s localhost:8770/grade-text -d '{"text":"...","backend":"cues"}'
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "server"))

# Load OpenRouter key (for backend=auto/cloud) from the gitignored env, like the other live tools.
_ENV = os.path.expanduser("~/.claude/agents/.env")
if os.path.exists(_ENV):
    for _line in open(_ENV, encoding="utf-8"):
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))


def grade_text(text: str, backend: str = "auto") -> list[dict]:
    """Run every TEXT lens over `text`; return per-lens index/tier + receipts (span + rationale),
    sorted strongest-first. backend: 'auto' (cloud->local), 'cloud', 'local', or 'cues' (offline floor)."""
    from ratchet_mcp.texts import _import_tradecraft, _tradecraft_detectors_dir
    load_lenses, _, text_lenses = _import_tradecraft()
    from tradecraft.detect import detect
    from tradecraft.grader import grade_document_for_lens

    lenses = text_lenses(load_lenses(_tradecraft_detectors_dir()))
    tok = max(1, len(text.split()))
    out = []
    for lid, tax in lenses.items():
        hits = detect(text, tax, backend=backend)
        r = grade_document_for_lens(tax, hits, token_count=tok)
        out.append({
            "lens": lid,
            "name": tax.name,
            "description": tax.description,
            "index": round(float(r.index), 1),
            "tier": r.tier,
            "receipts": [{"marker": h.detection_id, "span": h.span, "rationale": h.rationale}
                         for h in hits],
        })
    out.sort(key=lambda x: x["index"], reverse=True)
    return out


class _Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html", "/lens.html"):
            html = (HERE / "lens.html").read_text(encoding="utf-8")
            return self._send(200, html, "text/html; charset=utf-8")
        if self.path == "/healthz":
            return self._send(200, json.dumps({"ok": True}))
        return self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/grade-text":
            return self._send(404, json.dumps({"error": "not found"}))
        try:
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
            text = (payload.get("text") or "").strip()
            backend = payload.get("backend") or "auto"
            if not text:
                return self._send(400, json.dumps({"error": "empty text"}))
            if len(text) > 50000:
                return self._send(413, json.dumps({"error": "text too long (50k cap)"}))
            result = grade_text(text, backend=backend)
            return self._send(200, json.dumps({"backend": backend, "lenses": result}))
        except Exception as e:   # noqa: BLE001
            return self._send(500, json.dumps({"error": str(e)[:300]}))

    def log_message(self, *a):   # quiet
        pass


def main():
    port = int(os.environ.get("LENS_PORT", "8770"))
    srv = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    print(f"Tradecraft Lens demo on http://127.0.0.1:{port}  (Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
