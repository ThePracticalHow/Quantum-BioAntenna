#!/usr/bin/env python3
"""
atlas_api.py -- Serve the Binary Atlas as a local HTTP API.

This runs locally and serves the same endpoints that u-os.dev/atlas will serve.
Use this for development/testing. Deploy to Cloudflare Workers for production.

Usage:
  python atlas_api.py                    # Start server on port 8787
  python atlas_api.py --port 9000        # Custom port
  python atlas_api.py --export-json      # Export full atlas as static JSON (for Worker D1)

Endpoints:
  GET /atlas                    -- Summary
  GET /atlas/conditions         -- All conditions with tensors
  GET /atlas/axis               -- Independence axis (sorted)
  GET /atlas/cells?tissue=lung  -- Cells by filter
  GET /atlas/compare?a=X&b=Y   -- Compare two conditions
  GET /atlas/structural         -- All structural entries
  GET /atlas/export?tissue=X    -- Export subset as JSON
"""
import sqlite3, json, os, sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_PATH = Path(__file__).parent / "atlas.db"


def query_db(sql, params=()):
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_summary():
    tables = {}
    conn = sqlite3.connect(str(DB_PATH))
    for t in ["cells", "operators", "conditions", "coupling_tensor", "base4_xor",
              "structural", "junctions", "chains"]:
        try:
            n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            if n > 0:
                tables[t] = n
        except:
            pass
    meta = dict(conn.execute("SELECT key, value FROM atlas_meta").fetchall())
    tissues = [r[0] for r in conn.execute(
        "SELECT DISTINCT tissue FROM conditions WHERE tissue IS NOT NULL").fetchall()]
    conn.close()
    return {"tables": tables, "meta": meta, "tissues": tissues}


def get_conditions():
    return query_db("""
        SELECT c.condition_id, c.name, c.tissue, c.disease, c.n_cells,
               t.ribo_indep, t.k_rg, t.k_rm, t.det_k
        FROM conditions c
        LEFT JOIN coupling_tensor t ON c.condition_id = t.condition_id
        ORDER BY t.ribo_indep
    """)


def get_axis():
    return query_db("""
        SELECT c.name, c.tissue, c.disease, t.n_cells, t.ribo_indep, t.k_rg, t.k_rm, t.det_k
        FROM conditions c
        JOIN coupling_tensor t ON c.condition_id = t.condition_id
        WHERE t.ribo_indep IS NOT NULL
        ORDER BY t.ribo_indep
    """)


def get_structural():
    return query_db("SELECT * FROM structural ORDER BY mfe_per_nt")


def compare(a, b):
    rows_a = query_db("""
        SELECT c.name, t.* FROM conditions c
        JOIN coupling_tensor t ON c.condition_id = t.condition_id
        WHERE c.name LIKE ? OR c.condition_id LIKE ?
    """, (f"%{a}%", f"%{a}%"))
    rows_b = query_db("""
        SELECT c.name, t.* FROM conditions c
        JOIN coupling_tensor t ON c.condition_id = t.condition_id
        WHERE c.name LIKE ? OR c.condition_id LIKE ?
    """, (f"%{b}%", f"%{b}%"))
    return {"a": rows_a[0] if rows_a else None, "b": rows_b[0] if rows_b else None}


class AtlasHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        params = parse_qs(parsed.query)

        routes = {
            "/atlas": lambda: get_summary(),
            "/atlas/conditions": lambda: get_conditions(),
            "/atlas/axis": lambda: get_axis(),
            "/atlas/structural": lambda: get_structural(),
        }

        if path == "/atlas/compare":
            a = params.get("a", [""])[0]
            b = params.get("b", [""])[0]
            data = compare(a, b)
        elif path in routes:
            data = routes[path]()
        elif path == "" or path == "/":
            data = {"service": "Binary Atlas API", "version": "0.1",
                    "endpoints": list(routes.keys()) + ["/atlas/compare?a=X&b=Y"],
                    "source": "https://github.com/ThePracticalHow/Quantum-BioAntenna"}
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def log_message(self, format, *args):
        print(f"  {args[0]}")


def export_json():
    """Export full atlas as static JSON for embedding in Worker D1 or static hosting."""
    data = {
        "summary": get_summary(),
        "conditions": get_conditions(),
        "axis": get_axis(),
        "structural": get_structural(),
    }
    out = Path(__file__).parent / "atlas_static.json"
    with open(out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Exported: {out} ({out.stat().st_size // 1024} KB)")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--export-json", action="store_true")
    args = parser.parse_args()

    if args.export_json:
        export_json()
        return

    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found. Run atlas_ingest.py first.")
        return

    print(f"Binary Atlas API starting on http://localhost:{args.port}")
    print(f"Database: {DB_PATH}")
    print(f"Endpoints: /atlas, /atlas/conditions, /atlas/axis, /atlas/compare?a=X&b=Y")
    server = HTTPServer(("", args.port), AtlasHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
