#!/usr/bin/env python3
"""
atlas_ingest.py -- Ingest data into the Binary Atlas.

Supports:
  1. h5ad files (scRNA-seq count matrices) -> cells + operators
  2. STAFF JSON outputs (base4, frame, splice_history) -> conditions + aggregates
  3. Tensor JSON outputs -> conditions + coupling_tensor
  4. Structural JSON outputs -> structural table

Usage:
  # Ingest scRNA-seq (cell-level, the foundation)
  python atlas_ingest.py h5ad data.h5ad --tissue lung --disease cancer --accession GSE131907

  # Ingest pre-computed tensor results
  python atlas_ingest.py tensor korean_nsclc_tensor.json --tissue lung --accession GSE131907

  # Ingest STAFF base4 results
  python atlas_ingest.py base4 h9_base4.json --condition-id h9_fetal --tissue embryo

  # Ingest structural folding results
  python atlas_ingest.py structural structural_atlas_results.json
"""
import sqlite3, json, os, sys, argparse, time
import numpy as np
from pathlib import Path

ATLAS_DIR = Path(__file__).parent
DB_PATH = ATLAS_DIR / "atlas.db"
SCHEMA_PATH = ATLAS_DIR / "atlas_schema.sql"


def init_db():
    """Create database from schema if it doesn't exist."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())
    conn.commit()
    return conn


def ingest_h5ad(conn, path, tissue, species="human", disease="healthy",
                accession="", donor_id="", age_group="", sex="",
                treatment="", timepoint="", lab="", country="", platform="10x_chromium",
                group_key=None, max_cells=None):
    """Ingest an h5ad file: one row per cell in cells + operators tables."""
    try:
        import scanpy as sc
    except ImportError:
        print("ERROR: scanpy required for h5ad ingestion. pip install scanpy")
        return

    print(f"Loading {path}...")
    adata = sc.read_h5ad(path)
    print(f"  {adata.n_obs:,} cells x {adata.n_vars:,} genes")

    if max_cells and adata.n_obs > max_cells:
        sc.pp.subsample(adata, n_obs=max_cells)
        print(f"  Subsampled to {adata.n_obs:,}")

    genes = list(adata.var_names)
    ribo_mask = np.array([g.startswith("RPS") or g.startswith("RPL") for g in genes])
    mito_mask = np.array([g.startswith("MT-") or g.startswith("mt-") for g in genes])
    golgi_pfx = ("GOLGA", "GOLGB", "SEC61", "COPA", "COPB", "MAN1", "MGAT", "GORASP")
    golgi_mask = np.array([any(g.startswith(p) for p in golgi_pfx) for g in genes])

    X = adata.X
    if hasattr(X, "toarray"):
        ribo = np.asarray(X[:, ribo_mask].sum(axis=1)).flatten().astype(int)
        mito = np.asarray(X[:, mito_mask].sum(axis=1)).flatten().astype(int)
        golgi = np.asarray(X[:, golgi_mask].sum(axis=1)).flatten().astype(int)
        total = np.asarray(X.sum(axis=1)).flatten().astype(int)
        n_genes = np.asarray((X > 0).sum(axis=1)).flatten().astype(int)
    else:
        ribo = X[:, ribo_mask].sum(axis=1).astype(int)
        mito = X[:, mito_mask].sum(axis=1).astype(int)
        golgi = X[:, golgi_mask].sum(axis=1).astype(int)
        total = X.sum(axis=1).astype(int)
        n_genes = (X > 0).sum(axis=1).astype(int)
    nuclear = total - ribo - mito - golgi

    # Determine cell type if available
    cell_types = None
    if group_key and group_key in adata.obs.columns:
        cell_types = adata.obs[group_key].astype(str).values
    else:
        for key in ["cell_type", "celltype", "CellType", "leiden", "louvain",
                     "condition", "group", "sample", "batch"]:
            if key in adata.obs.columns:
                cell_types = adata.obs[key].astype(str).values
                break

    barcodes = adata.obs_names.tolist()
    prefix = accession or Path(path).stem

    print(f"  Ingesting {len(barcodes):,} cells...")
    t0 = time.time()
    cell_rows = []
    op_rows = []
    for i in range(len(barcodes)):
        cid = f"{prefix}_{barcodes[i]}"
        ct = cell_types[i] if cell_types is not None else None
        cell_rows.append((
            cid, accession, donor_id, barcodes[i],
            tissue, species, age_group, None, sex, disease, treatment, timepoint, ct,
            lab, country, platform, None,
            int(n_genes[i]), int(total[i])
        ))
        op_rows.append((
            cid, int(ribo[i]), int(mito[i]), int(golgi[i]), int(nuclear[i]), int(total[i])
        ))

    conn.executemany(
        "INSERT OR REPLACE INTO cells VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        cell_rows
    )
    conn.executemany(
        "INSERT OR REPLACE INTO operators VALUES (?,?,?,?,?,?)",
        op_rows
    )
    conn.commit()
    dt = time.time() - t0
    print(f"  Ingested {len(barcodes):,} cells in {dt:.1f}s")


def ingest_tensor(conn, path, tissue="", accession="", disease=""):
    """Ingest a pre-computed coupling tensor JSON."""
    with open(path) as f:
        data = json.load(f)

    groups = data.get("groups", data)
    if isinstance(groups, dict) and "group_key" in data:
        groups = data["groups"]

    for name, vals in groups.items():
        if not isinstance(vals, dict):
            continue
        cid = f"{accession}_{name}" if accession else name
        n = vals.get("n_cells", vals.get("n", 0))

        conn.execute("INSERT OR REPLACE INTO conditions VALUES (?,?,?,?,?,?,?)", (
            cid, name, tissue, disease, accession, n, f"Tensor from {Path(path).name}"
        ))
        conn.execute("INSERT OR REPLACE INTO coupling_tensor VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
            cid, n,
            vals.get("ribo_indep", vals.get("RIBO_independence", 0)),
            vals.get("det_k", vals.get("det_K", 0)),
            vals.get("trace_k", 0),
            vals.get("k_rm", vals.get("K_RM", 0)),
            vals.get("k_rn", vals.get("K_RN", 0)),
            vals.get("k_rg", vals.get("K_RG", 0)),
            vals.get("k_mn", vals.get("K_MN", 0)),
            vals.get("k_mg", vals.get("K_MG", 0)),
            vals.get("k_ng", vals.get("K_NG", 0)),
        ))

    conn.commit()
    print(f"  Ingested {len(groups)} conditions from {Path(path).name}")


def ingest_base4(conn, path, condition_id, tissue="", platform="nanopore"):
    """Ingest STAFF base4 XOR results."""
    with open(path) as f:
        data = json.load(f)

    xor = data.get("xor_distribution", data.get("junction_xor", data))
    if not isinstance(xor, dict):
        print(f"  WARNING: Could not parse XOR data from {path}")
        return

    conn.execute("INSERT OR REPLACE INTO conditions VALUES (?,?,?,?,?,?,?)", (
        condition_id, condition_id, tissue, "", "", 0, f"Base4 from {Path(path).name}"
    ))
    conn.execute("INSERT OR REPLACE INTO base4_xor VALUES (?,?,?,?,?,?,?,?)", (
        condition_id,
        xor.get("identity_pct", xor.get("00_identity_pct", 0)),
        xor.get("complement_pct", xor.get("01_complement_pct", 0)),
        xor.get("transversion_pct", xor.get("10_transversion_pct", 0)),
        xor.get("transition_pct", xor.get("11_transition_pct", 0)),
        data.get("gc_pct", 0),
        data.get("n_junctions", data.get("total_junctions", 0)),
        platform,
    ))
    conn.commit()
    print(f"  Ingested base4 XOR for {condition_id}")


def ingest_structural(conn, path):
    """Ingest structural folding results."""
    with open(path) as f:
        data = json.load(f)

    items = data if isinstance(data, dict) else {}
    count = 0
    for key, val in items.items():
        if not isinstance(val, dict) or "gc_pct" not in val:
            continue
        iid = val.get("name", key)
        cid = "cancer" if any(x in key.lower() for x in ["k562", "hepg2", "cancer"]) else "fetal"
        conn.execute("INSERT OR REPLACE INTO structural VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            iid, cid,
            val.get("chrom", ""), val.get("start", 0), val.get("end", 0),
            val.get("length", val.get("size", 0)),
            val.get("sequence", "")[:100],
            val.get("gc_pct", 0),
            val.get("mfe", 0),
            val.get("mfe_per_nt", 0),
            val.get("pct_paired", 0),
            val.get("stems", 0),
            val.get("structure", ""),
        ))
        count += 1
    conn.commit()
    print(f"  Ingested {count} structural entries from {Path(path).name}")


def main():
    parser = argparse.ArgumentParser(description="Binary Atlas Ingest")
    sub = parser.add_subparsers(dest="mode")

    h5 = sub.add_parser("h5ad", help="Ingest scRNA-seq h5ad")
    h5.add_argument("path")
    h5.add_argument("--tissue", required=True)
    h5.add_argument("--disease", default="healthy")
    h5.add_argument("--accession", default="")
    h5.add_argument("--species", default="human")
    h5.add_argument("--age-group", default="")
    h5.add_argument("--sex", default="")
    h5.add_argument("--treatment", default="")
    h5.add_argument("--timepoint", default="")
    h5.add_argument("--lab", default="")
    h5.add_argument("--country", default="")
    h5.add_argument("--platform", default="10x_chromium")
    h5.add_argument("--group-key", default=None)
    h5.add_argument("--max-cells", type=int, default=None)

    t = sub.add_parser("tensor", help="Ingest coupling tensor JSON")
    t.add_argument("path")
    t.add_argument("--tissue", default="")
    t.add_argument("--accession", default="")
    t.add_argument("--disease", default="")

    b = sub.add_parser("base4", help="Ingest STAFF base4 XOR JSON")
    b.add_argument("path")
    b.add_argument("--condition-id", required=True)
    b.add_argument("--tissue", default="")
    b.add_argument("--platform", default="nanopore")

    s = sub.add_parser("structural", help="Ingest structural folding JSON")
    s.add_argument("path")

    args = parser.parse_args()
    if not args.mode:
        parser.print_help()
        return

    conn = init_db()
    print(f"Atlas DB: {DB_PATH}")

    if args.mode == "h5ad":
        ingest_h5ad(conn, args.path, tissue=args.tissue, species=args.species,
                    disease=args.disease, accession=args.accession,
                    age_group=args.age_group, sex=args.sex,
                    treatment=args.treatment, timepoint=args.timepoint,
                    lab=args.lab, country=args.country, platform=args.platform,
                    group_key=args.group_key, max_cells=args.max_cells)
    elif args.mode == "tensor":
        ingest_tensor(conn, args.path, tissue=args.tissue,
                      accession=args.accession, disease=args.disease)
    elif args.mode == "base4":
        ingest_base4(conn, args.path, condition_id=args.condition_id,
                     tissue=args.tissue, platform=args.platform)
    elif args.mode == "structural":
        ingest_structural(conn, args.path)

    # Print summary
    for table in ["cells", "operators", "conditions", "coupling_tensor",
                   "base4_xor", "structural", "junctions", "chains"]:
        try:
            n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            if n > 0:
                print(f"  {table}: {n:,} rows")
        except:
            pass

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
