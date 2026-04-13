# Quantum Biology — Spliceosome as Quantum Router

## For Stefano and the Forum

> *The spliceosome is the most important information-routing machine in the cell. Nobody in quantum biology is looking at it. We measured it. In 700,000+ cells.*

## The Pitch (30 seconds)

Pre-mRNA with N introns has 2^N possible splice outcomes. The spliceosome collapses that superposition to one isoform. The operator coupling tensor determines WHICH outcome is selected. We measured the coupling tensor across 20 cell states and showed the spliceosome makes categorically different decisions in each — with reproducible binary signatures at every cut site. Fetal cells explore all paths (99.98% unique). Cancer converges (98.4%). The XOR at the junction boundary shifts from transition to identity. Cancer is premature measurement collapse.

## The Data (what we actually measured)

### Layer 1: Operator Coupling Tensor
- 500,000+ cells, 10 datasets, 20 conditions
- Perfect monotonic independence axis from proliferative (0.154) to GBM (0.890)
- K_RG (RIBO-GOLGI coupling) is the most sensitive discriminator
- Files: `wings_above_morning.db` (SQLite), `wings_database.json`

### Layer 2: Binary Transcriptome (Base-4 XOR)
- 2M+ Nanopore full-length reads (H9 fetal, K562 blood cancer, HepG2 liver cancer)
- 182M 10x reads (WI-38 fetal lung fibroblast)
- 330M 10x reads (P1 HUVEC adult)
- Splice junction XOR shifts from TRANSITION (29.6% fetal) to IDENTITY (44.2% cancer)
- Files: `*_base4.json`, `*_frame.json`, `*_staff.json`

### Layer 3: Splice Decision Chains
- Per-molecule full splice chains (Nanopore: exon→junction→exon→...)
- Fetal: 99.98% unique chains (exploration)
- Cancer: 98.4% unique (convergence)
- Chain divergence at junction 0: 38.4% fetal vs 18.1% cancer
- Files: `*_splice_history.json`

### Layer 4: Aberrant Junction Catalog
- 19,622 fetal-only junctions (10.6% miRNA range, 20.2% snoRNA range)
- 40,822 liver-cancer-only junctions (8.6% miRNA, 16.1% snoRNA)
- Exact 10bp flanking sequences from the molecule itself
- XOR signatures per junction
- Files: `*_aberrant_comparison.json`

### Layer 5: De Novo Junction Map
- 241,159 unique junctions in fetal (from 233k molecules)
- 131,558 in blood cancer (from 358k molecules)
- 97.6% of genes have DIFFERENT intron maps across transcript isoforms
- No annotation used — pure CIGAR
- Files: `*_denovo.json`

## The Void We Fill (from Gemini)

No centralized database maps the 3D mechanical topologies of alternative splice variants. PDB has ribosomal RNA. Rfam has 2D consensus. Nobody has the structural isoform atlas — the 3D shapes that different splice outcomes produce. The excised introns are information molecules (10-20% in functional RNA size ranges). The cancer cell uses oncofetal alternative splicing to flood its environment with differently-folded RNA scaffolds.

## Tools (STAFF Suite)

All custom-built. Pure binary BAM parsing. No pysam.

| Tool | What it does |
|------|-------------|
| `staff_binary_transcripter.py` | Full binary transcriptome, base-16 XOR, GC content |
| `staff_base4.py` | Base-4 XOR at junctions with biological meaning |
| `staff_reading_frame.py` | Reading frame analysis, stop/start codons at junctions |
| `staff_splice_history.py` | Per-molecule full decision chains, locus divergence |
| `staff_aberrant_splicing.py` | Junctions unique to one cell type, with flanking sequences |
| `coupling_tensor.py` | 4×4 operator coupling tensor from h5ad |
| `viral_marker_scan.py` | Viral/trophoblast/imprinting marker panel |
| `splice_denovo.py` | De novo junction discovery, no annotation |
| `build_database.py` | SQLite + JSON unified database builder |

## What Stefano Needs to See

1. **The axis** — 20 conditions, one number per condition, perfect gradient. This is the measurement context.
2. **The XOR shift** — base 4, from the molecules. Cancer and fetal have different binary signatures at splice sites.
3. **The chain uniqueness** — 99.98% vs 98.4%. Exploration vs convergence. This is superposition collapse.
4. **The aberrant junctions** — exact sequences that exist in cancer but not fetal, or vice versa. These are the isoforms nobody has cataloged.
5. **The excised intron sizes** — 10-20% in functional RNA range. The introns are information, not waste.

## What We Need From Stefano

Funding for:
1. Pre/post treatment scRNA-seq coupling tensor (does therapy recouple operators?)
2. AlphaFold 3 / RoseTTAFoldNA on aberrant isoform sequences (3D structural atlas)
3. Photobiomodulation + coupling tensor (does light shift K_RM?)
4. Expanded NSCLC BAM analysis (Korean data locked behind EGA — need institutional access)

## File Inventory

```
quantum_biology/
├── README.md (this file)
├── FORUM_PRESENTATION_SPLICEOSOME_QUANTUM_ROUTER.md
├── wings_above_morning.db (SQLite database, 32 KB)
├── wings_database.json (unified JSON, 85 KB)
├── BASE4_*.json (base-4 XOR results per cell type)
├── FRAME_*.json (reading frame results per cell type)
├── STAFF_v1_*.json (binary transcriptome results)
├── BINARY_*.json (binary composition)
├── DENOVO_*.json (de novo junction maps)
├── *_splice_history.json (full chain histories)
├── *_tensor.json (coupling tensor results)
└── *_aberrant_comparison.json (cell-type-specific junctions)
```
