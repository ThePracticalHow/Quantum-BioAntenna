# The Spliceosome as Quantum Router

**Operator coupling determines splice outcome. Measured across 700,000+ cells and 500M+ reads.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19554900.svg)](https://doi.org/10.5281/zenodo.19554900)

---

## What This Is

A zero-parameter measurement framework for how the spliceosome's behavior changes with cellular state. No thresholds, no training, no normalization. Raw gene counts, rank correlation, four cellular subsystems.

**Key findings:**

- A single **operator coupling axis** orders 20 conditions from proliferative (0.154) to GBM (0.890). Seven tissue compartments from one Korean NSCLC cohort (208,506 cells) show zero crossings.
- A reproducible **splice junction XOR shift** from fetal to cancer states: +7.4 percentage points toward identity, across 7 million junctions from Nanopore full-length transcripts.
- **Fetal cells explore** (99.98% unique splice chains). **Cancer converges** (98.4%). Per-molecule measurement, not population average.
- Cancer **avoids stop codons** and **seeks start codons** at splice boundaries. The spliceosome edits for survival.
- 10-20% of cell-type-specific excised introns are in **functional RNA size ranges**. Cancer releases rigid scaffolds (73% GC). Fetal releases flexible intermediates.
- **Meditation recouples operators** (GSE174083, PNAS 2021): K_RM +40%, RIBO independence -10% at 3 months post-retreat.
- Mg2+ **stabilizes RNA 1,297 kJ/mol more than Li+** at GNRA tetraloops (OpenMM MD, personal laptop, public PDB).

## Why It Matters

Light therapy works because photons recouple the mitochondrial operator (CcO/NO mechanism). Sound therapy works because vibration recouples the cytoskeletal operators (piezoelectric coupling). The coupling tensor is the readout that tells you whether it worked.

The decoherence time in FMO (60 fs) is not a disproof of quantum biology. It is the bandwidth specification for the antenna. The question was never "does coherence last long enough?" The question is "does the receiver read fast enough?"

## Data Provenance

| Dataset | Accession | Scale | Country |
|---------|-----------|-------|---------|
| NSCLC scRNA-seq | GSE131907 | 208K cells | South Korea |
| GBM scRNA-seq | GSE131928 | 7.9K cells | Israel/USA |
| SGNex Nanopore | SRA public | 2M+ reads | Singapore |
| WI-38 senescence | GSE226225 | 27K cells | USA (GEO) |
| Meditation retreat | GSE174083 | 388 samples | USA (GEO) |
| Normal adult lung | GSE150247 | 22K cells | USA (GEO) |
| GNRA tetraloop | PDB 1ZIF | NMR structure | Public domain |

All public. All reproducible. 7+ countries, 10+ labs.

## Repository Structure

```
tools/          13 Python scripts (MIT license)
data/           22 data files including SQLite + JSON databases (CC-BY 4.0)
sequences/      5 FASTA files — cancer and fetal excised introns
figures/        7 publication-quality charts
docs/           Briefs, reviewer proof, global source map, PDFs
md_results/     IP-clean Mg/Li molecular dynamics (OpenMM, PDB 1ZIF)
```

## Quick Start

```bash
# Coupling tensor on any scRNA-seq h5ad
python tools/coupling_tensor.py your_data.h5ad

# Base-4 XOR at splice junctions from any BAM
python tools/staff_base4.py your_file.bam output.json

# Per-molecule splice decision chains
python tools/staff_splice_history.py your_file.bam output.json

# Fold excised introns
pip install ViennaRNA
python tools/fold_isoforms.py

# Mg/Li molecular dynamics
pip install openmm mdtraj pdbfixer
python tools/replicate_md_ipclean.py --mode all --metal Mg --steps 50000
```

## Citing This Work

```
Leng, J. (2026). The Spliceosome as Quantum Router: Operator Coupling
Determines Splice Outcome. Zenodo. https://doi.org/10.5281/zenodo.19554900
```

## License

- **Code** (tools/): MIT License
- **Data and documentation**: CC-BY 4.0

## Contact

Jixiang Leng

---

*700,000+ cells. 500M+ reads. 10 datasets. 7+ countries. 9 tools. 4 MB. Built April 2026.*
