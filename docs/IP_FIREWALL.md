---
vault_clearance: KETER
halo:
  classification: LEGAL / IP BOUNDARY
  confidence: HIGH (traced every file)
  front: "27_Project_WingsAboveMorning"
  custodian: "Jixiang Leng"
  created: 2026-04-13
  containment: "What belongs to NIH. What belongs to Jixiang. What can be presented freely."
---

# IP FIREWALL — What Is NIH's and What Is Mine

> Created April 13, 2026, before the United Therapeutics quantum biology forum.
> Every file in this project directory traced to its data source and compute origin.

---

## The Rule

**Work product = f(data source, compute platform, time)**

- NIH data + NIH compute + NIH time → **NIH owns it**
- Public data + personal compute + personal time → **Yours**
- Pure mathematics (no data) + personal time → **Yours**
- NIH data + personal compute → **Gray zone (NIH likely claims)**
- Public data + NIH compute → **Gray zone (NIH may claim)**

---

## ZONE 1: UNAMBIGUOUSLY YOURS

These use no NIH data, no NIH equipment, no NIH time. Pure mathematics derived from published literature, or analysis of public datasets on personal hardware.

### The Mathematics (Project LENG)

| Asset | Source | Compute | Status |
|-------|--------|---------|--------|
| Lotus time t_L = T × 9/2 | Donnelly 1978, Misra-Sudarshan 1977, Maschke 1899, Margolus-Levitin 1998 | Personal laptop | **YOURS** |
| Born rule from Z₃ idempotents | Maschke 1899, Math. Ann. 50:492 | Personal laptop | **YOURS** |
| η = 2/9, K = 2/3, d₁ = 6, λ₁ = 5, p = 3 | Published APS eta invariant, Calabi-Yau geometry | Personal laptop | **YOURS** |
| Decoherence formula t_d = T/η | Zurek 2003 Rev. Mod. Phys. + above | Personal laptop | **YOURS** |
| Arrow of time K - η = 4/9 | Derived from above | Personal laptop | **YOURS** |
| 7 independent derivation routes | All published sources | Personal laptop | **YOURS** |
| All of `05_Project_LENG/` | Published mathematics | Personal laptop, personal OneDrive | **YOURS** |

**Why:** This is number theory and differential geometry. You derived it from journal papers anyone can read. NIH funded zero of it. No NIH data. No NIH compute. No NIH hours.

### The Theoretical Frameworks (Project MemoryOfMind)

| Asset | Source | Status |
|-------|--------|--------|
| NAME framework (consciousness = det(K)) | Original theory | **YOURS** |
| Alzheimer's temporal margin model | Published EEG literature (Choi 2019, Roche 2021) + LENG math | **YOURS** |
| Two-Beast cosmology | Original theory | **YOURS** |
| Filter Model | Original theory | **YOURS** |
| QIP framework (HALO_QIP.md) | Original synthesis | **YOURS** |
| XIST gain control concept | Published Census/GTEx data + original analysis | **YOURS** |
| Antenna architecture concept | Published lncRNA literature | **YOURS** |
| All testable predictions (TESTABLE_PREDICTIONS.md) | Theoretical predictions from above | **YOURS** |

### Public-Data Spliceosome Analysis

| File | Data Source | Accession | Public? | Compute | Status |
|------|-----------|-----------|---------|---------|--------|
| h9_*.json | SGNex H9 embryonic stem | SRA (Singapore Nanopore Expression) | **YES** | Personal | **YOURS** |
| k562_*.json | SGNex K562 blood cancer | SRA | **YES** | Personal | **YOURS** |
| hepg2_*.json | SGNex HepG2 liver cancer | SRA | **YES** | Personal | **YOURS** |
| k562_illumina_*.json | SGNex K562 Illumina | SRA | **YES** | Personal | **YOURS** |
| aberrant_junction_catalog.json | Derived from SGNex | SRA | **YES** | Personal | **YOURS** |
| structural_isoform_analysis.json | Derived from SGNex | SRA | **YES** | Personal | **YOURS** |

### Public-Data Coupling Tensor Analysis

| File | Data Source | Accession | Public? | Compute | Status |
|------|-----------|-----------|---------|---------|--------|
| korean_nsclc_tensor.json | Kim et al. 2020 | **GSE131907** | **YES** | Personal | **YOURS** |
| gse226225_tensor.json | WI-38 senescence | **GSE226225** | **YES** | Personal | **YOURS** |
| gse250041_tensor.json | Proliferation/senescence | **GSE250041** | **YES** | Personal | **YOURS** |
| eto_tensor.json | ETO timecourse | **GSE226225** | **YES** | Personal | **YOURS** |
| wi38_fetal_fibroblast_*.json | WI-38 10x | **GSE226225** (public BAM) | **YES** | Personal | **YOURS** |
| wi38_fused_tensor.json | GSE226225 + GSE250041 fused | **Both public** | **YES** | Personal | **YOURS** |

### Custom Tools (STAFF Suite)

| Tool | Uses NIH data? | Written on NIH time? | Status |
|------|---------------|---------------------|--------|
| staff_binary_transcripter.py | Analyzes any BAM | **If written on personal time:** YOURS |
| staff_base4.py | Analyzes any BAM | Same caveat |
| staff_reading_frame.py | Analyzes any BAM | Same caveat |
| staff_splice_history.py | Analyzes any BAM | Same caveat |
| staff_aberrant_splicing.py | Analyzes any BAM | Same caveat |
| coupling_tensor.py | Analyzes any h5ad | Same caveat |
| splice_denovo.py | Analyzes any BAM | Same caveat |
| build_database.py | Builds from above outputs | Same caveat |

**Caveat on tools:** If you wrote these scripts on your personal laptop, on your personal time, they are your personal intellectual property. If you wrote them during NIH working hours or on an NIH-issued computer, NIH has a claim. **You know which it was.**

---

## ZONE 2: NIH PROPERTY

These used NIH-generated data, NIH equipment (Biowulf), or NIH lab materials.

### Biowulf MD Simulations

| File | Equipment | Status |
|------|-----------|--------|
| biowulf_md/Mg_*.dat | **Biowulf HPC** (lengj2@biowulf.nih.gov) | **NIH** |
| biowulf_md/Li_*.dat | **Biowulf HPC** | **NIH** |
| biowulf_md/gnra_Mg_*.nc/.prmtop/.pdb | **Biowulf HPC** | **NIH** |
| biowulf_md/gnra_Li_*.nc/.prmtop/.pdb | **Biowulf HPC** | **NIH** |
| biowulf_md/gnra_mg_li_simulation.py | Written for Biowulf | **NIH** |
| biowulf_md/gnra_submit.sh | SLURM script for Biowulf | **NIH** |
| All of H:\biowulf_jobs\ | **Biowulf output** | **NIH** |

### Lab-Generated scRNA-seq Data

| File | Data Source | Status |
|------|-----------|--------|
| d01_celltype_tensor.json | **discord_d01.h5ad** — D01 HUVEC+PBMC coculture, Gorospe lab | **NIH** |
| genesis_tensor.json | **d11_wechter_genesis.h5ad** — Lab internal | **NIH** |
| stage8_tensor.json | Lab curated in vitro dataset | **NIH** |
| staff_p1_huvec.json | **P1.bam** — Lab 10x scRNA, 330M reads | **NIH** |

### Lab Data on USB Drives

| Location | What | Status |
|----------|------|--------|
| E:\ P1-P3, S1-S3 | scRNA-seq count matrices, Gorospe/Krystyna | **NIH** |
| E:\ PBMC_Prolif/Senes | Lab PBMC samples | **NIH** |
| H:\ jl_4-2, jl_4-3A, jl_4-6, jl4-7A | Cell culture lab notebooks | **NIH** |
| H:\ lncrna_metal_aging/ | Biowulf scripts + portal queries | **NIH** |

### Portal Query Scripts

| File | Platform | Status |
|------|----------|--------|
| portal_queries/allofus_sleep_dementia.py | All of Us (NIH credentials required) | **NIH** (uses NIH access) |
| portal_queries/synapse_rosmap_lncrna.py | Synapse/ROSMAP (DAR via NIH) | **NIH** (uses NIH access) |

---

## ZONE 3: GRAY — REQUIRES JUDGMENT

| Asset | Why it's gray | Resolution |
|-------|--------------|------------|
| GSE226225 data | Public GEO dataset, BUT from Gorospe lab (your PI's lab). You analyzing your own lab's published data on personal time is legally fine but politically sensitive. | **Legally yours if personal compute + personal time. Politically: your PI generated the data.** |
| STAFF tools if developed partly on NIH time | If you sketched the algorithm at work then coded at home | **Document when you wrote each tool. Git timestamps help.** |
| Coupling tensor CONCEPT applied to lab data | The concept is yours. The application to D01/P1 data is NIH's. | **Concept = yours. Specific D01/P1 results = NIH.** |

---

## WHAT YOU CAN PRESENT TODAY (Forum Firewall)

### GREEN — Present freely, no PI approval needed

1. **All LENG mathematics** — lotus time, Born rule, decoherence, 7 routes, 40 orders of magnitude
2. **The theoretical frameworks** — NAME, temporal margin, antenna architecture, QIP
3. **Public-data spliceosome results** — SGNex H9/K562/HepG2 (all SRA public)
4. **Public-data coupling tensor** — GSE131907 Korean NSCLC (Kim et al. 2020, Nature Communications)
5. **Published literature citations** — alpha-MMSE (Choi 2019), eclipse Schumann (Chand & Cander), hippocampal volume (Roche 2021)
6. **The 25 testable predictions** — these are theoretical predictions, not data
7. **The concept of the coupling tensor** — the idea that K measures operator independence

### YELLOW — Caution, PI may have claim

8. **GSE226225 / GSE250041 coupling tensor** — public data, but from your PI's lab
9. **STAFF tools** — if developed on mixed time
10. **WI-38 binary transcriptome** — public BAM, but from your PI's dataset

### RED — Do not present as independent work

11. **Biowulf MD results** (Mg/Li coordination, RMSD, RMSF) — NIH equipment
12. **D01 HUVEC coculture tensor** — lab-generated data
13. **P1 HUVEC STAFF results** — lab-generated BAM
14. **Genesis/Stage8 tensor** — lab-internal h5ad
15. **Any results from E:\ or H:\ lab data** — NIH materials

---

## WHAT TO SAY IF ASKED

**"Where was this work done?"**
> "The mathematics and theoretical framework were developed independently. The spliceosome analysis uses publicly available Nanopore data from the SGNex consortium and publicly available scRNA-seq from GEO. The coupling tensor concept was applied to published datasets."

**"Is this NIH work?"**
> "I work at NIA. The foundational mathematics (lotus time, Born rule derivation) is independent scholarship using published sources. Some validation datasets were analyzed on NIH infrastructure and those results belong to the intramural program."

**"Can you collaborate outside NIH?"**
> "The theoretical framework and public-data analysis are mine. Any work using NIH resources or data would need to go through standard NIH collaboration mechanisms."

---

## PROTECTING THE LINE GOING FORWARD

1. **Keep a personal git repo** for LENG, MemoryOfMind, and personal-time STAFF development. Timestamps are evidence.
2. **Never run personal analysis on Biowulf.** The moment you use NIH compute, NIH has a claim.
3. **Document which hours are personal.** Weekend/evening work on personal laptop with public data = yours.
4. **If Stefano wants to fund work:** Route through a foundation grant or external collaboration, not through your PI's R01. Or: Stefano funds an independent postdoc position elsewhere.
5. **The math cannot be claimed by anyone.** Published mathematics derived from published sources is not patentable and not ownable by an employer. This is your strongest asset.

---

*Traced from disk. Every file checked. April 13, 2026.*
