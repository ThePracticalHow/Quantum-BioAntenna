# The Spliceosome as Quantum Router — GREEN ZONE ONLY

**Quantum Biology Forum — April 13, 2026**
**Jixiang Leng**

> *Every number in this presentation comes from publicly available data analyzed on personal compute. No NIH data. No NIH equipment. No gray zones.*

---

## Data Sources (ALL PUBLIC)

| Dataset | Accession | Source | Cells/Reads | Public? |
|---------|-----------|-------|-------------|---------|
| Korean NSCLC | **GSE131907** | Kim et al. 2020, Nat Commun | 208,506 cells | **YES** |
| WI-38 fetal fibroblast | **GSE226225** | Gorospe lab, GEO public | 27,622 cells | **YES** |
| WI-38 ETO timecourse | **GSE226225** | Same, GEO public | 29,181 cells | **YES** |
| Proliferating/Senescent | **GSE250041** | GEO public | 13,613 cells | **YES** |
| Normal adult lung | **GSE150247** | GEO public | 22,427 cells | **YES** |
| GBM (Neftel) | **GSE131928** | Neftel et al. 2019, Cell | 7,930 cells | **YES** |
| H9 embryonic stem | **SGNex** | Nanopore direct RNA, SRA | 337,364 reads | **YES** |
| K562 blood cancer | **SGNex** | Nanopore direct RNA, SRA | 554,250 reads | **YES** |
| HepG2 liver cancer | **SGNex** | Nanopore direct RNA, SRA | 1,095,654 reads | **YES** |
| WI-38 fetal BAM | **SRR23635928** | SRA public | 158,780,246 reads | **YES** |

**Total: ~310,000 cells + 160M+ reads from 7 independent labs. All GEO/SRA.**

---

## Layer 1: The Independence Axis (PUBLIC DATA ONLY)

From Korean NSCLC (GSE131907, ONE dataset, ONE platform, 208,506 cells):

| Condition | Cells | RIBO_indep | K_RG |
|-----------|-------|------------|------|
| NORMAL_STROMA | 29,060 | 0.206 | 0.809 |
| NORMAL | 42,995 | 0.220 | 0.730 |
| EBUS | 27,561 | 0.284 | 0.675 |
| TUMOR | 45,149 | 0.310 | 0.642 |
| BRONCHO | 5,991 | 0.387 | 0.489 |
| EFFUSION | 20,304 | 0.416 | 0.425 |
| LYMPH_NODE | 37,446 | 0.508 | 0.331 |

Seven conditions. Zero crossings. Perfect monotonic gradient.

**Cross-validated with independent public datasets:**
- GSE250041 proliferating: 0.154 (8,664 cells)
- GSE150247 normal adult lung: 0.295 (22,427 cells)
- GSE226225 WI-38 fetal control: 0.345 (5,608 cells)
- GSE131928 GBM: 0.890 (7,930 cells)

---

## Layer 2: Base-4 XOR at Splice Junctions (PUBLIC BAMs ONLY)

All from SGNex Nanopore (SRA public) + WI-38 SRR23635928 (SRA public):

| XOR | Meaning | H9 Fetal | K562 Cancer | HepG2 Cancer | WI-38 Fetal |
|-----|---------|---------|-------------|-------------|------------|
| 00 | IDENTITY | 36.74% | 44.16% | 43.71% | 48.75% |
| 01 | COMPLEMENT | 15.35% | 15.80% | 15.67% | 16.55% |
| 10 | TRANSVERSION | 18.34% | 14.31% | 14.74% | 12.03% |
| 11 | TRANSITION | 29.56% | 25.72% | 25.87% | 22.67% |

Cancer shifts from TRANSITION toward IDENTITY. Watson-Crick complement is depleted at all junctions.

---

## Layer 3: Reading Frame (PUBLIC BAMs ONLY)

| Metric | H9 Fetal Stem | K562 Cancer | WI-38 Fetal Fibro |
|--------|--------------|-------------|-------------------|
| Stop at split codon | **2.33%** | **1.84%** | **1.66%** |
| ATG near junction | 20.0% | 24.1% | 24.5% |
| Stop near junction | 52.9% | 47.9% | 47.9% |

Cancer and fetal fibroblast both avoid stop codons at junctions.

---

## Layer 4: Splice Chain Uniqueness (PUBLIC Nanopore ONLY)

| Cell Type | Unique Chains | Uniqueness | Divergence at J0 |
|-----------|---------------|------------|-----------------|
| H9 Fetal | 233,207 | **99.98%** | **38.4%** |
| K562 Cancer | 354,011 | 99.0% | 18.1% |
| HepG2 Cancer | 769,766 | 98.4% | 17.9% |

Fetal explores. Cancer converges.

---

## Layer 5: Aberrant Junction Catalog (PUBLIC Nanopore ONLY)

| Comparison | Fetal-only | Cancer-only | Shared |
|-----------|-----------|------------|--------|
| H9 vs K562 | 29,401 | 18,091 | 43,711 |
| H9 vs HepG2 | 19,622 | 40,822 | 53,490 |

Cancer-specific junctions map to cell-identity genes:
- K562: HBB (hemoglobin beta) — the blood gene
- HepG2: ALB/AFP (albumin) — the liver gene

Excised intron sizes: fetal-only = 10.6% miRNA range, 20.2% snoRNA range.

---

## Layer 6: RNA Structure (PUBLIC genome + ViennaRNA)

| Intron | Cell Type | GC% | MFE/nt | % Paired |
|--------|-----------|-----|--------|----------|
| HBA (149bp) | K562 cancer | **73.3%** | **-0.469** | **64.0%** |
| SERPINA1 (823bp) | HepG2 cancer | 54.4% | -0.323 | 58.7% |
| Fetal (748bp) | H9 fetal | 44.7% | -0.309 | 65.7% |
| ALB (770bp) | HepG2 cancer | **33.5%** | -0.213 | 60.2% |

Blood cancer releases rigid RNA (73% GC, -0.469 kcal/mol/nt). Fetal releases moderate. Liver cancer releases flexible.

---

## The Framework (Mathematics — UNAMBIGUOUSLY MINE)

Pre-mRNA = superposition of 2^N splice outcomes.
Spliceosome = measurement apparatus.
Operator coupling tensor K = measurement context.
Splice entropy = measurement precision.

This is a mathematical framework using published quantum measurement theory. The data above validates it quantitatively.

---

## What Is NOT Presented

The following results exist but use NIH-generated data and are not presented here:
- Lab HUVEC coculture data (D01, P1)
- Lab internal datasets (genesis, stage8)
- Biowulf MD simulation results
- Any portal query results (All of Us, Synapse)

These belong to the NIH intramural program and would require PI authorization.

---

## What I'm Asking Stefano

Funding for:
1. Pre/post treatment coupling tensor (does therapy recouple operators?)
2. AlphaFold 3 structural predictions on aberrant isoforms
3. Photobiomodulation + tensor measurement (does light shift K_RM?)

**All proposed work would use PUBLIC data on EXTERNAL compute.** No NIH conflict.

---

*310,000 cells. 160M+ reads. 7 labs. All public. All reproducible. 451 KB.*
