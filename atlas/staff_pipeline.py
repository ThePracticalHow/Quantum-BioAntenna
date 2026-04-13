#!/usr/bin/env python3
"""
staff_pipeline.py -- One-command pipeline: data in, atlas-ready measurement out.

Usage:
  # From h5ad (scRNA-seq count matrix)
  python staff_pipeline.py --input data.h5ad --tissue lung --disease cancer --accession GSE131907

  # From BAM (Nanopore or 10x -- runs STAFF binary tools)
  python staff_pipeline.py --input reads.bam --tissue embryo --disease healthy --accession SGNex --platform nanopore

  # Ingest into atlas after measurement
  python staff_pipeline.py --input data.h5ad --tissue lung --disease cancer --accession GSE131907 --ingest

What it does:
  1. Detects input type (h5ad or BAM)
  2. For h5ad: computes coupling tensor per group, exports JSON
  3. For BAM: runs base4, reading frame, splice history (if tools available)
  4. Saves atlas-ready JSON output
  5. Optionally ingests directly into atlas.db
"""
import os, sys, json, time, argparse, subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TOOLS_DIR = SCRIPT_DIR.parent / "tools"
ATLAS_DIR = SCRIPT_DIR


def detect_input(path):
    """Detect input type from extension."""
    ext = Path(path).suffix.lower()
    if ext in (".h5ad", ".h5"):
        return "h5ad"
    elif ext in (".bam",):
        return "bam"
    else:
        print(f"Unknown input type: {ext}")
        sys.exit(1)


def run_h5ad(path, tissue, disease, accession, group_key, output_dir):
    """Run coupling tensor on h5ad file."""
    print(f"=== COUPLING TENSOR: {Path(path).name} ===")
    try:
        sys.path.insert(0, str(TOOLS_DIR))
        from coupling_tensor import compute_tensor
        import scanpy as sc
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Install: pip install scanpy anndata")
        return None

    adata = sc.read_h5ad(path)
    print(f"  Loaded: {adata.n_obs:,} cells x {adata.n_vars:,} genes")

    results = compute_tensor(adata, group_key=group_key)
    results["metadata"] = {
        "source": str(path),
        "tissue": tissue,
        "disease": disease,
        "accession": accession,
        "pipeline": "staff_pipeline.py",
        "date": time.strftime("%Y-%m-%d"),
    }

    out_path = output_dir / f"{accession or Path(path).stem}_tensor.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved: {out_path}")
    return out_path


def run_bam(path, tissue, disease, accession, platform, output_dir):
    """Run STAFF binary tools on BAM file."""
    prefix = accession or Path(path).stem
    results = {"source": str(path), "tissue": tissue, "disease": disease,
               "accession": accession, "platform": platform}
    outputs = []

    staff_tools = [
        ("staff_base4.py", f"{prefix}_base4.json"),
        ("staff_reading_frame.py", f"{prefix}_frame.json"),
        ("staff_splice_history.py", f"{prefix}_history.json"),
    ]

    for script, outname in staff_tools:
        script_path = TOOLS_DIR / script
        if not script_path.exists():
            script_path = SCRIPT_DIR.parent / "tools" / script
        if not script_path.exists():
            print(f"  SKIP {script} (not found)")
            continue

        out_path = output_dir / outname
        print(f"=== {script}: {Path(path).name} ===")
        cmd = [sys.executable, str(script_path), str(path), str(out_path)]
        t0 = time.time()
        proc = subprocess.run(cmd, capture_output=True, text=True)
        dt = time.time() - t0

        if proc.returncode == 0:
            print(f"  Done in {dt:.1f}s -> {out_path.name}")
            outputs.append(str(out_path))
        else:
            print(f"  FAILED ({proc.returncode}): {proc.stderr[:200]}")

    results["outputs"] = outputs
    manifest = output_dir / f"{prefix}_manifest.json"
    with open(manifest, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Manifest: {manifest}")
    return manifest


def ingest_to_atlas(tensor_path, tissue, disease, accession):
    """Ingest results into atlas.db."""
    ingest_script = ATLAS_DIR / "atlas_ingest.py"
    if not ingest_script.exists():
        print("  atlas_ingest.py not found, skipping ingest")
        return

    cmd = [sys.executable, str(ingest_script), "tensor", str(tensor_path),
           "--tissue", tissue, "--disease", disease, "--accession", accession]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0:
        print(f"  Ingested into atlas.db")
        print(proc.stdout)
    else:
        print(f"  Ingest failed: {proc.stderr[:200]}")


def main():
    parser = argparse.ArgumentParser(description="STAFF Pipeline: data in, atlas out")
    parser.add_argument("--input", "-i", required=True, help="Input h5ad or BAM file")
    parser.add_argument("--tissue", required=True)
    parser.add_argument("--disease", default="healthy")
    parser.add_argument("--accession", default="")
    parser.add_argument("--platform", default="10x_chromium")
    parser.add_argument("--group-key", default=None)
    parser.add_argument("--output-dir", "-o", default=None)
    parser.add_argument("--ingest", action="store_true", help="Also ingest into atlas.db")
    args = parser.parse_args()

    input_type = detect_input(args.input)
    output_dir = Path(args.output_dir) if args.output_dir else Path("atlas_output")
    output_dir.mkdir(exist_ok=True)

    print(f"Input: {args.input} ({input_type})")
    print(f"Output: {output_dir}")

    if input_type == "h5ad":
        result = run_h5ad(args.input, args.tissue, args.disease,
                          args.accession, args.group_key, output_dir)
        if result and args.ingest:
            ingest_to_atlas(result, args.tissue, args.disease, args.accession)

    elif input_type == "bam":
        result = run_bam(args.input, args.tissue, args.disease,
                         args.accession, args.platform, output_dir)

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()
