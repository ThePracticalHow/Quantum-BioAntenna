"""
generate_forum_figures.py — Publication-quality figures for quantum biology forum.
All data from GREEN-zone public datasets. No NIH data.

Run: python generate_forum_figures.py
Output: forum_figures/ directory with PNGs

Jixiang Leng, April 13, 2026. Personal laptop. Public data.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "forum_figures")
os.makedirs(OUT, exist_ok=True)

C_BLUE = "#2d5aa0"
C_RED = "#c44e52"
C_GOLD = "#d4a017"
C_GREEN = "#2e8b57"
C_GREY = "#888888"
C_LIGHT = "#6baed6"
C_PURPLE = "#7b68ee"

def fig1_independence_axis():
    """The monotonic coupling axis across 20 conditions."""
    conditions = [
        ("Proliferative\n(GSE250041)", 0.154, C_GREEN),
        ("Normal\nStroma", 0.206, C_BLUE),
        ("Normal\nLung", 0.220, C_BLUE),
        ("Normal Adult\nLung (GSE150247)", 0.295, C_BLUE),
        ("Primary\nTumor", 0.310, C_RED),
        ("WI-38 Fetal\n(GSE226225)", 0.345, C_GOLD),
        ("Broncho", 0.387, C_RED),
        ("Effusion", 0.416, C_RED),
        ("Metastatic\n(Lymph Node)", 0.508, C_RED),
        ("GBM\n(GSE131928)", 0.890, C_RED),
    ]
    names = [c[0] for c in conditions]
    vals = [c[1] for c in conditions]
    colors = [c[2] for c in conditions]

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(range(len(names)), vals, color=colors, edgecolor="white", width=0.7, linewidth=0.8)
    for i, (bar, val) in enumerate(zip(bars, vals)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.012,
                f"{val:.3f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, fontsize=8, ha="center")
    ax.set_ylabel("RIBO Independence", fontsize=12, fontweight="bold")
    ax.set_title("Operator Independence Axis: 10 Conditions, 500K+ Cells\nZero crossings within Korean cohort (GSE131907, 208,506 cells)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_ylim(0, 1.0)
    ax.axhspan(0.30, 0.36, alpha=0.1, color=C_GOLD, label="Cancer-fetal overlap zone")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    patches = [mpatches.Patch(color=C_GREEN, label="Proliferative"),
               mpatches.Patch(color=C_BLUE, label="Normal tissue"),
               mpatches.Patch(color=C_GOLD, label="Fetal"),
               mpatches.Patch(color=C_RED, label="Cancer / metastatic")]
    ax.legend(handles=patches, loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig1_independence_axis.png"), dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("  [1] Independence axis")

def fig2_xor_shift():
    """Base-4 XOR shift from fetal to cancer."""
    categories = ["Identity\n(00)", "Complement\n(01)", "Transversion\n(10)", "Transition\n(11)"]
    fetal =  [36.74, 15.35, 18.34, 29.56]
    k562 =   [44.16, 15.80, 14.31, 25.72]
    hepg2 =  [43.71, 15.67, 14.74, 25.87]

    x = np.arange(len(categories))
    w = 0.25
    fig, ax = plt.subplots(figsize=(10, 5))
    b1 = ax.bar(x - w, fetal, w, label="H9 Fetal Stem (SGNex)", color=C_GOLD, edgecolor="white")
    b2 = ax.bar(x, k562, w, label="K562 Blood Cancer (SGNex)", color=C_RED, edgecolor="white")
    b3 = ax.bar(x + w, hepg2, w, label="HepG2 Liver Cancer (SGNex)", color=C_PURPLE, edgecolor="white")
    for bars in [b1, b2, b3]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                    f"{h:.1f}%", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylabel("Frequency (%)", fontsize=12, fontweight="bold")
    ax.set_title("Splice Junction XOR Shift: Fetal vs Cancer\n7M+ junctions from Nanopore full-length transcripts (SGNex, SRA public)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.legend(fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 52)
    ax.annotate("", xy=(0-w, fetal[0]+2), xytext=(0, k562[0]+2),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=2))
    ax.text(-0.15, 41, "+7.4%", fontsize=9, fontweight="bold", color=C_RED)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig2_xor_shift.png"), dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("  [2] XOR shift")

def fig3_chain_uniqueness():
    """Per-molecule splice chain uniqueness."""
    types = ["H9 Fetal\nStem", "K562 Blood\nCancer", "HepG2 Liver\nCancer"]
    uniqueness = [99.98, 99.0, 98.4]
    divergence = [38.4, 18.1, 17.9]
    colors_u = [C_GOLD, C_RED, C_PURPLE]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    bars1 = ax1.bar(types, uniqueness, color=colors_u, edgecolor="white", width=0.5)
    ax1.set_ylim(97.5, 100.2)
    ax1.set_ylabel("Chain Uniqueness (%)", fontsize=11, fontweight="bold")
    ax1.set_title("Splice Chain Uniqueness\n(per-molecule, Nanopore full-length)", fontsize=12, fontweight="bold", pad=10)
    for bar, val in zip(bars1, uniqueness):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                f"{val:.2f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    bars2 = ax2.bar(types, divergence, color=colors_u, edgecolor="white", width=0.5)
    ax2.set_ylabel("Divergence at Junction 0 (%)", fontsize=11, fontweight="bold")
    ax2.set_title("First-Junction Divergence\n(how quickly molecules branch)", fontsize=12, fontweight="bold", pad=10)
    for bar, val in zip(bars2, divergence):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    fig.suptitle("Fetal Cells Explore. Cancer Converges.", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig3_chain_uniqueness.png"), dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("  [3] Chain uniqueness")

def fig4_structural_atlas():
    """Excised intron structural comparison from fold results."""
    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "structural_atlas_results.json")
    if not os.path.exists(results_path):
        print("  [4] SKIPPED - structural_atlas_results.json not found")
        return
    with open(results_path) as f:
        data = json.load(f)

    cancer, fetal = [], []
    for key, r in data.items():
        if not isinstance(r, dict) or "gc_pct" not in r:
            continue
        row = (r.get("name", key)[:20], r["gc_pct"], abs(r["mfe_per_nt"]), r["pct_paired"])
        if "cancer" in key.lower() or "K562" in key or "HepG2" in key:
            cancer.append(row)
        elif "fetal" in key.lower() or "H9" in key:
            fetal.append(row)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    metrics = [("GC Content (%)", 1), ("Stability (|MFE/nt|)", 2), ("Base Pairing (%)", 3)]
    for ax, (label, idx) in zip(axes, metrics):
        c_vals = [c[idx] for c in cancer]
        f_vals = [f_[idx] for f_ in fetal]
        positions = [1, 2]
        bp = ax.boxplot([c_vals, f_vals], positions=positions, widths=0.4, patch_artist=True,
                        showmeans=True, meanprops=dict(marker="D", markerfacecolor="white", markersize=6))
        bp["boxes"][0].set_facecolor(C_RED)
        bp["boxes"][0].set_alpha(0.6)
        bp["boxes"][1].set_facecolor(C_GOLD)
        bp["boxes"][1].set_alpha(0.6)
        for c_v in c_vals:
            ax.scatter(1 + np.random.uniform(-0.1, 0.1), c_v, color=C_RED, alpha=0.7, s=30, zorder=5)
        for f_v in f_vals:
            ax.scatter(2 + np.random.uniform(-0.1, 0.1), f_v, color=C_GOLD, alpha=0.7, s=30, zorder=5)
        ax.set_xticks(positions)
        ax.set_xticklabels(["Cancer\n(8 introns)", "Fetal\n(3 introns)"], fontsize=10)
        ax.set_ylabel(label, fontsize=11, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("Structural Properties of Cell-Type-Specific Excised Introns\n(ViennaRNA MFE, all public sequences, folded on laptop)",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig4_structural_atlas.png"), dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("  [4] Structural atlas")

def fig5_intron_sizes():
    """Excised intron functional RNA size ranges."""
    comparisons = ["H9 fetal-only", "K562 cancer-only\n(vs H9)", "K562 cancer-only\n(vs HepG2)", "HepG2 cancer-only\n(vs H9)", "HepG2 cancer-only\n(vs K562)"]
    mirna = [10.6, 10.7, 10.7, 8.6, 7.9]
    snorna_extra = [20.2-10.6, 19.8-10.7, 20.5-10.7, 16.1-8.6, 15.0-7.9]
    colors_m = [C_GOLD, C_RED, C_RED, C_PURPLE, C_PURPLE]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(comparisons))
    ax.bar(x, mirna, 0.5, label="miRNA range (60-150bp)", color=[c for c in colors_m], alpha=0.8, edgecolor="white")
    ax.bar(x, snorna_extra, 0.5, bottom=mirna, label="snoRNA range (150-300bp)", color=[c for c in colors_m], alpha=0.4, edgecolor="white")
    for i, (m, s) in enumerate(zip(mirna, [m+s for m, s in zip(mirna, snorna_extra)])):
        ax.text(i, s + 0.3, f"{s:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(comparisons, fontsize=9)
    ax.set_ylabel("% of Excised Introns", fontsize=11, fontweight="bold")
    ax.set_title("Excised Introns in Functional RNA Size Ranges\nCell-type-specific junctions from Nanopore (SGNex, SRA public)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.legend(fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig5_intron_sizes.png"), dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("  [5] Intron sizes")

def fig6_stop_codon():
    """Stop codon avoidance at splice junctions."""
    types = ["H9 Fetal\nStem", "K562 Blood\nCancer", "HepG2 Liver\nCancer", "WI-38 Fetal\nFibroblast"]
    stop_pct = [2.33, 1.84, 1.77, 1.66]
    atg_pct = [20.0, 24.1, 23.8, 24.5]
    colors_bar = [C_GOLD, C_RED, C_PURPLE, C_GOLD]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    bars1 = ax1.bar(types, stop_pct, color=colors_bar, edgecolor="white", width=0.5)
    ax1.set_ylabel("Stop Codons at Split Position (%)", fontsize=10, fontweight="bold")
    ax1.set_title("Stop Codon Avoidance", fontsize=12, fontweight="bold", pad=10)
    for bar, val in zip(bars1, stop_pct):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{val:.2f}%", ha="center", fontsize=10, fontweight="bold")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.annotate("Cancer avoids stops", xy=(1, 1.84), xytext=(1.5, 2.2),
                arrowprops=dict(arrowstyle="->", color=C_GREY), fontsize=9, color=C_GREY, style="italic")

    bars2 = ax2.bar(types, atg_pct, color=colors_bar, edgecolor="white", width=0.5)
    ax2.set_ylabel("ATG Near Junction (%)", fontsize=10, fontweight="bold")
    ax2.set_title("Start Codon Enrichment", fontsize=12, fontweight="bold", pad=10)
    for bar, val in zip(bars2, atg_pct):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f"{val:.1f}%", ha="center", fontsize=10, fontweight="bold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle("The Spliceosome Edits for Survival\n(reading frame analysis at every junction)", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig6_stop_codon.png"), dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("  [6] Stop codon avoidance")

def fig7_data_provenance():
    """Visual summary of data provenance across countries."""
    countries = ["South Korea", "Israel/USA", "Singapore\n/Aus/Spain", "USA (GEO)", "Germany", "Global (CZI)"]
    cells_k = [208.5, 7.9, 2000, 72, 5, 500]
    colors_c = [C_RED, C_PURPLE, C_GREEN, C_BLUE, C_GOLD, C_LIGHT]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(countries, cells_k, color=colors_c, edgecolor="white", height=0.5)
    for bar, val in zip(bars, cells_k):
        label = f"{val:.0f}K" if val < 100 else f"{val/1000:.1f}M" if val >= 1000 else f"{val:.0f}K"
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                label + " reads/cells", va="center", fontsize=10, fontweight="bold")
    ax.set_xlabel("Scale (thousands of cells/reads)", fontsize=11, fontweight="bold")
    ax.set_title("International Data Provenance\n7+ countries, 10+ labs, all public repositories",
                 fontsize=13, fontweight="bold", pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, 700)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig7_data_provenance.png"), dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("  [7] Data provenance")

def main():
    print("Generating forum figures...")
    fig1_independence_axis()
    fig2_xor_shift()
    fig3_chain_uniqueness()
    fig4_structural_atlas()
    fig5_intron_sizes()
    fig6_stop_codon()
    fig7_data_provenance()
    print(f"\nAll figures saved to: {OUT}")
    print("Ready for presentation.")

if __name__ == "__main__":
    main()
