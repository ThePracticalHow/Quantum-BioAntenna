# Quantum-BioAntenna

### The Spliceosome as Quantum Router: Operator Coupling Determines Splice Outcome

[![Zenodo Version DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19555738.svg)](https://doi.org/10.5281/zenodo.19555738)
[![Zenodo Concept DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19555737.svg)](https://doi.org/10.5281/zenodo.19555737)
[![LENG DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18712638.svg)](https://doi.org/10.5281/zenodo.18712638)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE_CODE.md)
[![License: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](LICENSE_DATA.md)

---

> **700,000+ cells. 500M+ reads. 10 datasets. 7+ countries. 13 tools. All public data. All open source.**

A zero-parameter measurement framework showing that the spliceosome -- the cell's central information router -- makes categorically different decisions depending on cellular state, and that light, sound, and meditation measurably recouple the operators that aging and disease have decoupled.

---

## Key Findings

| Finding | Number | Source |
|---------|--------|--------|
| Operator coupling axis | 20 conditions, zero crossings | 500K+ cells, GSE131907 (208K, Korea) |
| Splice junction XOR shift | +7.4% identity (fetal to cancer) | 7M+ junctions, SGNex Nanopore |
| Fetal exploration vs cancer convergence | 99.98% vs 98.4% unique chains | Per-molecule, Nanopore |
| Cancer stop codon avoidance | 1.66-1.84% vs 2.33% fetal | Reading frame analysis |
| Excised introns in functional RNA range | 10-20% in miRNA/snoRNA sizes | Cell-type-specific |
| Meditation recouples operators | K_RM +40%, RIBO independence -10% | GSE174083, PNAS 2021, 388 samples |
| Mg vs Li at GNRA tetraloops | 1,297 kJ/mol difference, 1.34 A RMSD | OpenMM MD, PDB 1ZIF |

## Why Light and Sound Work

| Intervention | Target Operator | Mechanism | Predicted Readout |
|---|---|---|---|
| **Red/NIR light (PBM)** | MITO (CcO) | Photon displaces NO, restores electron flow | K_RM increases |
| **Sound / 40 Hz** | GOLGI, NUCLEAR (cytoskeleton) | Piezoelectric vibration, local E-fields | K_RG increases |
| **Molecular jackhammers** | Membrane (GOLGI output) | Vibronic-driven mechanical rupture | Selectively kills low-K_RG |
| **Meditation** | All operators | Breath (MITO) + attention (NUC) + posture | **Measured: K_RM +40% at 3 months** |

Pulsed light outperforms continuous because the anti-Zeno to Zeno transition requires intermittent measurement. The coupling tensor is the readout that tells you whether it worked.

## Alzheimer's: Six Radio Failure Modes

Current drugs target 1 of 6 modes. Trial failure rate: 99.6%. A multi-mode protocol costs ~$60/month vs $26,500/year for lecanemab. Full analysis: [`docs/Unclarity_Map_Alzheimers_Six_Failure_Modes.pdf`](docs/Unclarity_Map_Alzheimers_Six_Failure_Modes.pdf)

## Repository Structure

```
data/           22 files — coupling tensors, XOR results, splice chains, databases
tools/          13 scripts — STAFF suite, coupling tensor, ViennaRNA folding, OpenMM MD
sequences/      5 FASTA — cancer and fetal excised introns
figures/        7 PNG — publication-quality charts
docs/           briefs, reviewer proof, global source map, clinical PDFs
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

# Fold excised introns (pip install ViennaRNA)
python tools/fold_isoforms.py

# Mg/Li MD (pip install openmm mdtraj pdbfixer)
python tools/replicate_md_ipclean.py --mode all --metal Mg --steps 50000
```

## Data Provenance

| Dataset | Accession | Scale | Country |
|---------|-----------|-------|---------|
| NSCLC scRNA-seq | GSE131907 | 208,506 cells, 44 patients | South Korea |
| GBM scRNA-seq | GSE131928 | 7,930 cells, 28 tumors | Israel / USA |
| SGNex Nanopore | SRA public | 2M+ full-length reads | Singapore / Australia / Spain |
| Meditation retreat | GSE174083 | 388 samples, PNAS 2021 | USA |
| WI-38 senescence | GSE226225 | 27,622 cells | USA (public GEO) |
| Normal adult lung | GSE150247 | 22,427 cells | USA (public GEO) |
| GNRA tetraloop | PDB 1ZIF | NMR structure | Public domain |
| CellxGene Census | CZI | 500K+ human cells | Global |

## Related Work

- **LENG (The Resolved Chord):** 87 physical constants from zero free parameters. [DOI: 10.5281/zenodo.18712638](https://doi.org/10.5281/zenodo.18712638)
- **u-os.dev:** Lab API and warp interface. [https://u-os.dev](https://u-os.dev/?format=md)

## Citing

Use the **version DOI** when citing the archived `v1.0.0` release, and use the **concept DOI** when referring to the repository across versions.

```text
Leng, J. (2026). The Spliceosome as Quantum Router: Operator Coupling Determines Splice Outcome (Version v1.0.0) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.19555738
```

All-version concept DOI: `10.5281/zenodo.19555737`

## License

- **Code** (`tools/`): [MIT License](LICENSE_CODE.md)
- **Data and documentation**: [CC-BY 4.0](LICENSE_DATA.md)

---

*Built April 2026. The code runs. The biology replicates. We need collaborators, not converts.*
