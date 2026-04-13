#!/usr/bin/env python3
"""
atlas_query.py -- Query the Binary Atlas.

Usage:
  python atlas_query.py summary                    # Atlas overview
  python atlas_query.py cells --tissue lung        # List cells by tissue
  python atlas_query.py conditions                 # List all conditions
  python atlas_query.py tensor --tissue lung       # Coupling tensors for lung
  python atlas_query.py compare --a cancer --b fetal  # Compare two states
  python atlas_query.py axis                       # Full independence axis
  python atlas_query.py export --tissue lung -o lung_cells.json  # Export subset
"""
import sqlite3, json, sys, argparse
from pathlib import Path
from collections import defaultdict

DB_PATH = Path(__file__).parent / "atlas.db"


def get_conn():
    if not DB_PATH.exists():
        print(f"ERROR: Atlas not found at {DB_PATH}")
        print("Run atlas_ingest.py first to create the database.")
        sys.exit(1)
    return sqlite3.connect(str(DB_PATH))


def cmd_summary(args):
    """Print atlas overview."""
    conn = get_conn()
    print("=" * 60)
    print("  BINARY ATLAS SUMMARY")
    print("=" * 60)

    for table in ["cells", "operators", "conditions", "coupling_tensor",
                   "base4_xor", "reading_frame", "splice_chains", "structural",
                   "junctions", "chains", "proteins"]:
        try:
            n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            if n > 0:
                print(f"  {table:20s} {n:>10,} rows")
        except:
            pass

    meta = dict(conn.execute("SELECT key, value FROM atlas_meta").fetchall())
    print(f"\n  Schema version: {meta.get('schema_version', '?')}")
    print(f"  Created: {meta.get('created', '?')}")

    # Tissue breakdown
    rows = conn.execute(
        "SELECT tissue, COUNT(*) FROM cells GROUP BY tissue ORDER BY COUNT(*) DESC"
    ).fetchall()
    if rows:
        print(f"\n  Cells by tissue:")
        for tissue, n in rows:
            print(f"    {tissue:20s} {n:>10,}")

    # Disease breakdown
    rows = conn.execute(
        "SELECT disease, COUNT(*) FROM cells GROUP BY disease ORDER BY COUNT(*) DESC"
    ).fetchall()
    if rows:
        print(f"\n  Cells by disease:")
        for disease, n in rows:
            print(f"    {disease:20s} {n:>10,}")

    # Condition count
    rows = conn.execute(
        "SELECT COUNT(*) FROM conditions"
    ).fetchone()
    if rows and rows[0] > 0:
        print(f"\n  Pre-computed conditions: {rows[0]}")

    print("=" * 60)
    conn.close()


def cmd_cells(args):
    """Query cells by metadata filters."""
    conn = get_conn()
    where = []
    params = []
    if args.tissue:
        where.append("tissue = ?")
        params.append(args.tissue)
    if args.disease:
        where.append("disease = ?")
        params.append(args.disease)
    if args.species:
        where.append("species = ?")
        params.append(args.species)
    if args.accession:
        where.append("accession = ?")
        params.append(args.accession)
    if args.sex:
        where.append("sex = ?")
        params.append(args.sex)
    if args.age_group:
        where.append("age_group = ?")
        params.append(args.age_group)

    clause = " AND ".join(where) if where else "1=1"
    query = f"""
        SELECT c.cell_id, c.tissue, c.disease, c.cell_type, c.accession,
               o.ribo_total, o.mito_total, o.golgi_total, o.nuclear_total, o.total
        FROM cells c LEFT JOIN operators o ON c.cell_id = o.cell_id
        WHERE {clause}
        ORDER BY c.tissue, c.disease
        LIMIT {args.limit}
    """
    rows = conn.execute(query, params).fetchall()
    print(f"Cells matching query: {len(rows)} (limit {args.limit})")
    print(f"{'cell_id':40s} {'tissue':12s} {'disease':12s} {'type':15s} {'RIBO':>6s} {'MITO':>6s} {'GOLGI':>6s} {'NUC':>8s}")
    print("-" * 110)
    for r in rows:
        cid, tissue, disease, ct, acc, ribo, mito, golgi, nuc, tot = r
        print(f"{cid[:40]:40s} {tissue or '':12s} {disease or '':12s} {(ct or '')[:15]:15s} "
              f"{ribo or 0:6d} {mito or 0:6d} {golgi or 0:6d} {nuc or 0:8d}")
    conn.close()


def cmd_conditions(args):
    """List all pre-computed conditions with tensors."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT c.condition_id, c.name, c.tissue, c.disease, c.n_cells,
               t.ribo_indep, t.k_rg, t.det_k
        FROM conditions c
        LEFT JOIN coupling_tensor t ON c.condition_id = t.condition_id
        ORDER BY t.ribo_indep
    """).fetchall()
    print(f"{'condition':30s} {'tissue':12s} {'disease':12s} {'cells':>8s} {'RIBO_ind':>9s} {'K_RG':>7s} {'det_K':>8s}")
    print("-" * 95)
    for r in rows:
        cid, name, tissue, disease, n, ri, krg, dk = r
        print(f"{(name or cid)[:30]:30s} {tissue or '':12s} {disease or '':12s} "
              f"{n or 0:8d} {ri or 0:9.3f} {krg or 0:7.3f} {dk or 0:8.4f}")
    conn.close()


def cmd_axis(args):
    """Print the full independence axis sorted by RIBO independence."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT c.name, c.tissue, c.disease, t.n_cells, t.ribo_indep, t.k_rg, t.k_rm
        FROM conditions c
        JOIN coupling_tensor t ON c.condition_id = t.condition_id
        WHERE t.ribo_indep IS NOT NULL
        ORDER BY t.ribo_indep
    """).fetchall()
    print(f"\n  INDEPENDENCE AXIS ({len(rows)} conditions)")
    print(f"  {'Condition':25s} {'Tissue':12s} {'Disease':12s} {'Cells':>7s} {'RIBO_ind':>9s} {'K_RG':>7s} {'K_RM':>7s}")
    print("  " + "-" * 85)
    for name, tissue, disease, n, ri, krg, krm in rows:
        bar = "#" * int(ri * 40) if ri else ""
        print(f"  {(name or '?')[:25]:25s} {tissue or '':12s} {disease or '':12s} "
              f"{n or 0:7d} {ri or 0:9.3f} {krg or 0:7.3f} {krm or 0:7.3f}  {bar}")
    conn.close()


def cmd_compare(args):
    """Compare two conditions."""
    conn = get_conn()
    rows_a = conn.execute("""
        SELECT c.name, t.* FROM conditions c
        JOIN coupling_tensor t ON c.condition_id = t.condition_id
        WHERE c.name LIKE ? OR c.disease LIKE ? OR c.condition_id LIKE ?
    """, (f"%{args.a}%", f"%{args.a}%", f"%{args.a}%")).fetchall()
    rows_b = conn.execute("""
        SELECT c.name, t.* FROM conditions c
        JOIN coupling_tensor t ON c.condition_id = t.condition_id
        WHERE c.name LIKE ? OR c.disease LIKE ? OR c.condition_id LIKE ?
    """, (f"%{args.b}%", f"%{args.b}%", f"%{args.b}%")).fetchall()

    if not rows_a:
        print(f"No conditions matching '{args.a}'")
        return
    if not rows_b:
        print(f"No conditions matching '{args.b}'")
        return

    a = rows_a[0]
    b = rows_b[0]
    fields = ["name", "condition_id", "n_cells", "ribo_indep", "det_k", "trace_k",
              "k_rm", "k_rn", "k_rg", "k_mn", "k_mg", "k_ng"]

    print(f"\n  COMPARISON: {a[0]} vs {b[0]}")
    print(f"  {'Metric':20s} {'A':>12s} {'B':>12s} {'Delta':>12s}")
    print("  " + "-" * 60)
    for i, field in enumerate(fields[2:], start=3):
        va = a[i] if a[i] is not None else 0
        vb = b[i] if b[i] is not None else 0
        delta = vb - va
        print(f"  {field:20s} {va:12.4f} {vb:12.4f} {delta:+12.4f}")
    conn.close()


def cmd_export(args):
    """Export a subset of cells as JSON."""
    conn = get_conn()
    where = []
    params = []
    if args.tissue:
        where.append("c.tissue = ?")
        params.append(args.tissue)
    if args.disease:
        where.append("c.disease = ?")
        params.append(args.disease)
    if args.accession:
        where.append("c.accession = ?")
        params.append(args.accession)

    clause = " AND ".join(where) if where else "1=1"
    rows = conn.execute(f"""
        SELECT c.cell_id, c.tissue, c.species, c.disease, c.cell_type, c.accession,
               o.ribo_total, o.mito_total, o.golgi_total, o.nuclear_total, o.total
        FROM cells c LEFT JOIN operators o ON c.cell_id = o.cell_id
        WHERE {clause}
    """, params).fetchall()

    export = []
    for r in rows:
        export.append({
            "cell_id": r[0], "tissue": r[1], "species": r[2],
            "disease": r[3], "cell_type": r[4], "accession": r[5],
            "ribo": r[6], "mito": r[7], "golgi": r[8], "nuclear": r[9], "total": r[10]
        })

    out = args.output or "atlas_export.json"
    with open(out, "w") as f:
        json.dump({"n_cells": len(export), "cells": export}, f, indent=2)
    print(f"Exported {len(export):,} cells to {out}")
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Binary Atlas Query")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("summary", help="Atlas overview")

    c = sub.add_parser("cells", help="Query cells")
    c.add_argument("--tissue", default=None)
    c.add_argument("--disease", default=None)
    c.add_argument("--species", default=None)
    c.add_argument("--accession", default=None)
    c.add_argument("--sex", default=None)
    c.add_argument("--age-group", default=None)
    c.add_argument("--limit", type=int, default=50)

    sub.add_parser("conditions", help="List conditions with tensors")
    sub.add_parser("axis", help="Full independence axis")

    cmp = sub.add_parser("compare", help="Compare two conditions")
    cmp.add_argument("--a", required=True)
    cmp.add_argument("--b", required=True)

    exp = sub.add_parser("export", help="Export cells as JSON")
    exp.add_argument("--tissue", default=None)
    exp.add_argument("--disease", default=None)
    exp.add_argument("--accession", default=None)
    exp.add_argument("-o", "--output", default=None)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return

    {"summary": cmd_summary, "cells": cmd_cells, "conditions": cmd_conditions,
     "axis": cmd_axis, "compare": cmd_compare, "export": cmd_export}[args.cmd](args)


if __name__ == "__main__":
    main()
