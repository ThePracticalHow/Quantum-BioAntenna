#!/usr/bin/env python3
"""
fold_isoforms.py — Structural Isoform Atlas: Proof of Concept
================================================================

Fetches excised intron sequences from UCSC DAS, folds them with ViennaRNA,
and compares 3D structural properties between cancer-specific and
fetal-specific splice variants.

No Biowulf. No PI approval. No bureaucracy. Runs on your laptop.

Dependencies: ViennaRNA (pip install ViennaRNA), urllib (stdlib)

Jixiang Leng, April 13, 2026
"""
import json
import os
import sys
import urllib.request
import urllib.error
import time
import statistics

# Try ViennaRNA
try:
    import RNA
    HAVE_VIENNA = True
except ImportError:
    HAVE_VIENNA = False
    print("WARNING: ViennaRNA not found. Install with: pip install ViennaRNA")
    print("Or run with Python 3.12: python3.12 fold_isoforms.py")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_sequence_ucsc(chrom, start, end, genome="hg38"):
    """Fetch genomic sequence from UCSC DAS server."""
    chrom_str = f"chr{chrom}" if not str(chrom).startswith("chr") else str(chrom)
    url = f"https://genome.ucsc.edu/cgi-bin/das/{genome}/dna?segment={chrom_str}:{start},{end}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml = resp.read().decode("utf-8")
        # Parse DNA from DAS XML
        import re
        match = re.search(r"<DNA[^>]*>(.*?)</DNA>", xml, re.DOTALL)
        if match:
            seq = match.group(1).replace("\n", "").replace(" ", "").upper()
            return seq
    except Exception as e:
        print(f"  UCSC DAS failed for {chrom_str}:{start}-{end}: {e}")

    # Fallback: Ensembl REST
    try:
        url2 = f"https://rest.ensembl.org/sequence/region/human/{chrom_str}:{start}..{end}?content-type=text/plain"
        req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=30) as resp2:
            seq = resp2.read().decode("utf-8").strip().upper()
            return seq
    except Exception as e2:
        print(f"  Ensembl also failed: {e2}")
        return None


def fold_vienna(sequence, name=""):
    """Fold RNA with ViennaRNA. Returns (structure, mfe, stats)."""
    # Convert DNA to RNA
    rna_seq = sequence.replace("T", "U")

    if len(rna_seq) > 3000:
        print(f"  {name}: sequence too long ({len(rna_seq)}bp), truncating to 3000")
        rna_seq = rna_seq[:3000]

    if HAVE_VIENNA:
        structure, mfe = RNA.fold(rna_seq)
    else:
        # Command-line fallback
        import subprocess
        result = subprocess.run(
            ["RNAfold", "--noPS"],
            input=f">{name}\n{rna_seq}\n",
            capture_output=True, text=True, timeout=300
        )
        lines = result.stdout.strip().split("\n")
        if len(lines) >= 2:
            last = lines[-1]
            parts = last.rsplit(" ", 1)
            structure = parts[0].strip()
            mfe = float(parts[1].strip("() "))
        else:
            return None, None, None

    # Compute structural statistics
    n = len(structure)
    paired = structure.count("(") + structure.count(")")
    unpaired = structure.count(".")
    pct_paired = (paired / n * 100) if n > 0 else 0
    mfe_per_nt = mfe / n if n > 0 else 0

    # Count structural elements
    stems = 0
    in_stem = False
    for c in structure:
        if c == "(" and not in_stem:
            stems += 1
            in_stem = True
        elif c != "(":
            in_stem = False

    loops = structure.count("(.")  # Rough loop count
    gc_content = (rna_seq.count("G") + rna_seq.count("C")) / len(rna_seq) * 100

    stats = {
        "length": n,
        "gc_pct": round(gc_content, 1),
        "mfe": round(mfe, 2),
        "mfe_per_nt": round(mfe_per_nt, 4),
        "pct_paired": round(pct_paired, 1),
        "stems": stems,
        "paired_bases": paired,
        "unpaired_bases": unpaired,
    }

    return structure, mfe, stats


def analyze_intron(entry, name):
    """Fetch, fold, and analyze one excised intron."""
    chrom = entry["chrom"]
    start = entry["start"]
    end = entry["end"]
    size = entry["size"]

    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"  {entry.get('gene','?')} | chr{chrom}:{start}-{end} | {size}bp")
    print(f"  Count: {entry.get('count','?')} molecules")
    print(f"{'='*60}")

    # Fetch sequence
    print(f"  Fetching sequence from UCSC/Ensembl...")
    seq = fetch_sequence_ucsc(chrom, start, end)
    if not seq:
        print(f"  FAILED to fetch sequence")
        return None

    if len(seq) < 10:
        print(f"  Sequence too short: {len(seq)}bp")
        return None

    print(f"  Got {len(seq)}bp sequence")
    print(f"  First 40bp: {seq[:40]}...")
    print(f"  Last 40bp:  ...{seq[-40:]}")

    # Fold
    print(f"  Folding with ViennaRNA...")
    t0 = time.time()
    structure, mfe, stats = fold_vienna(seq, name)
    dt = time.time() - t0

    if structure is None:
        print(f"  FAILED to fold")
        return None

    print(f"  Folded in {dt:.1f}s")
    print(f"  MFE: {mfe:.2f} kcal/mol ({stats['mfe_per_nt']:.4f} kcal/mol/nt)")
    print(f"  GC: {stats['gc_pct']:.1f}%")
    print(f"  Paired: {stats['pct_paired']:.1f}% ({stats['paired_bases']}/{stats['length']})")
    print(f"  Stems: {stats['stems']}")

    # Show structure for short sequences
    if len(structure) <= 200:
        print(f"  Structure: {structure}")

    result = {
        "name": name,
        "gene": entry.get("gene", "unknown"),
        "cell_type": name.split("_")[0],
        "chrom": chrom,
        "start": start,
        "end": end,
        "size": size,
        "count": entry.get("count", 0),
        "sequence": seq,
        "structure": structure,
        **stats
    }

    return result


def main():
    # Load the structural isoform catalog
    catalog_path = os.path.join(SCRIPT_DIR, "structural_isoform_analysis.json")
    with open(catalog_path) as f:
        catalog = json.load(f)

    print("=" * 72)
    print("  STRUCTURAL ISOFORM ATLAS — PROOF OF CONCEPT")
    print("  Fold excised introns from cancer vs fetal splice variants")
    print("  ViennaRNA on laptop. No Biowulf. No PI. No bureaucracy.")
    print("=" * 72)
    print(f"\n  {len(catalog)} introns to analyze")
    print(f"  ViennaRNA: {'Python API' if HAVE_VIENNA else 'command-line'}")

    results = {}
    cancer_stats = []
    fetal_stats = []

    for key, entry in catalog.items():
        result = analyze_intron(entry, key)
        if result:
            results[key] = result
            if "cancer" in key.lower():
                cancer_stats.append(result)
            elif "fetal" in key.lower():
                fetal_stats.append(result)
        time.sleep(0.5)  # Be nice to UCSC

    # === COMPARATIVE ANALYSIS ===
    print("\n" + "=" * 72)
    print("  COMPARATIVE ANALYSIS: CANCER vs FETAL EXCISED INTRONS")
    print("=" * 72)

    if cancer_stats and fetal_stats:
        print(f"\n  Cancer introns: {len(cancer_stats)}")
        print(f"  Fetal introns:  {len(fetal_stats)}")

        # Table
        print(f"\n  {'Name':<45} {'Size':>5} {'GC%':>5} {'MFE/nt':>8} {'%Paired':>8} {'Stems':>6}")
        print(f"  {'-'*45} {'-'*5} {'-'*5} {'-'*8} {'-'*8} {'-'*6}")

        print(f"\n  CANCER:")
        for r in cancer_stats:
            print(f"  {r['name']:<45} {r['length']:>5} {r['gc_pct']:>5.1f} {r['mfe_per_nt']:>8.4f} {r['pct_paired']:>8.1f} {r['stems']:>6}")

        print(f"\n  FETAL:")
        for r in fetal_stats:
            print(f"  {r['name']:<45} {r['length']:>5} {r['gc_pct']:>5.1f} {r['mfe_per_nt']:>8.4f} {r['pct_paired']:>8.1f} {r['stems']:>6}")

        # Averages
        c_mfe = [r["mfe_per_nt"] for r in cancer_stats]
        f_mfe = [r["mfe_per_nt"] for r in fetal_stats]
        c_gc = [r["gc_pct"] for r in cancer_stats]
        f_gc = [r["gc_pct"] for r in fetal_stats]
        c_pair = [r["pct_paired"] for r in cancer_stats]
        f_pair = [r["pct_paired"] for r in fetal_stats]

        print(f"\n  SUMMARY:")
        print(f"  {'Metric':<25} {'Cancer Mean':>12} {'Fetal Mean':>12} {'Difference':>12}")
        print(f"  {'-'*25} {'-'*12} {'-'*12} {'-'*12}")
        print(f"  {'GC content (%)':<25} {statistics.mean(c_gc):>12.1f} {statistics.mean(f_gc):>12.1f} {statistics.mean(c_gc)-statistics.mean(f_gc):>+12.1f}")
        print(f"  {'MFE/nt (kcal/mol/nt)':<25} {statistics.mean(c_mfe):>12.4f} {statistics.mean(f_mfe):>12.4f} {statistics.mean(c_mfe)-statistics.mean(f_mfe):>+12.4f}")
        print(f"  {'Paired bases (%)':<25} {statistics.mean(c_pair):>12.1f} {statistics.mean(f_pair):>12.1f} {statistics.mean(c_pair)-statistics.mean(f_pair):>+12.1f}")

        # Welch t-test if scipy available
        try:
            from scipy import stats as sp_stats
            t_mfe, p_mfe = sp_stats.ttest_ind(c_mfe, f_mfe, equal_var=False)
            t_gc, p_gc = sp_stats.ttest_ind(c_gc, f_gc, equal_var=False)
            t_pair, p_pair = sp_stats.ttest_ind(c_pair, f_pair, equal_var=False)
            print(f"\n  Statistical tests (Welch t):")
            print(f"  GC:     t={t_gc:.3f}, p={p_gc:.4f}")
            print(f"  MFE/nt: t={t_mfe:.3f}, p={p_mfe:.4f}")
            print(f"  Paired: t={t_pair:.3f}, p={p_pair:.4f}")
        except ImportError:
            print("\n  (scipy not available for t-test)")

    # Save results
    out_path = os.path.join(SCRIPT_DIR, "structural_atlas_results.json")
    with open(out_path, "w") as f:
        # Don't save full sequences to keep file small
        save = {}
        for k, v in results.items():
            sv = {kk: vv for kk, vv in v.items() if kk != "sequence"}
            sv["sequence_length"] = len(v.get("sequence", ""))
            sv["sequence_first_40"] = v.get("sequence", "")[:40]
            sv["sequence_last_40"] = v.get("sequence", "")[-40:]
            save[k] = sv
        json.dump(save, f, indent=2)
    print(f"\n  Results saved to: {out_path}")

    print("\n" + "=" * 72)
    print("  STRUCTURAL ISOFORM ATLAS — PROOF OF CONCEPT COMPLETE")
    print(f"  {len(results)} introns folded. Cancer vs fetal compared.")
    print("  All from public data. All on this laptop.")
    print("  No Biowulf. No PI. No bureaucracy.")
    print("=" * 72)


if __name__ == "__main__":
    main()
