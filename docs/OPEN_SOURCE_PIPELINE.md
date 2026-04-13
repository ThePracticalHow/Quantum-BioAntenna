# Open-Source Pipeline: No Bureaucracy Required

> Everything below is free, open source, and runs on a personal machine. No institutional allocation, no PI approval, no HPC ticket.

---

## RNA 3D Structure Prediction

| Tool | What It Does | Input | Speed | Source |
|---|---|---|---|---|
| **DRfold2** (Feb 2026) | Best standalone RNA folder. Pre-trained language model + denoising structure module. | Single sequence | ~40 min for <200 nt | Open source |
| **RhoFold+** | Deep learning, single-sequence, no MSA needed. Good for global folds. | Single sequence | Fast | `ml4bio/RhoFold` (GitHub) |
| **SimRNA** | Physics-based coarse-grained MD. Models ion effects implicitly. | Sequence + constraints | Slower (hours) | Free academic |
| **OpenComplex** | Open-source AlphaFold2 architecture for protein, RNA, and complexes. | Sequence(s) | Moderate | Open source |

## Ion Effects

| Tool | What It Does | Why It Matters |
|---|---|---|
| **TiRNA** (2026) | Temperature AND ion concentration as input variables affecting fold. | Directly tests Mg vs Li at GNRA sites |
| **MetalionRNA** | Predicts WHERE Mg/Na/K bind in a given RNA 3D structure. | Maps ion binding sites in folded structures |
| **AlphaFold 3 Server** | Free non-commercial. Models RNA + ions + ligands. | Web-based, no install, paste sequence |

## The Pipeline

```
1. Take divergent splice variants (cancer vs adult vs fetal)
   — same gene, different isoforms from public scRNA-seq

2. Fold each variant locally
   — DRfold2 or RhoFold+ on laptop (~40 min per fold)

3. Add ion context
   — TiRNA: fold with Mg2+ vs Li+ vs depleted conditions

4. Predict ion binding sites
   — MetalionRNA: where does Mg bind in each fold?

5. Compare 3D structures
   — Adult vs Fetal vs Cancer variants of THE SAME GENE
   — If shapes are categorically different → first entries
     in the Structural Isoform Atlas
```

## Data Sources (All Public, No Institutional Access Required)

| Dataset | Access | What It Provides |
|---|---|---|
| GTEx v8 | dbGaP phs000424 (open tier) | 948 donors, 54 tissues, expression + splicing |
| CellxGene Census | cellxgene.cziscience.com | ~500K human cells, downloadable h5ad |
| GEO (all GSE accessions) | ncbi.nlm.nih.gov/geo | Public scRNA-seq datasets |
| OpenNeuro ds004504 | openneuro.org | AD EEG, 88 subjects |
| PhysioNet Sleep-EDF | physionet.org | 153 subjects, polysomnography |
| Sierra Nevada ELF | Published (Applied Sciences 2024) | Schumann resonance, 1407 days |
| Replogle GWPS | Public Perturb-seq | 11,258 CRISPRi perturbations |
| Ensembl REST | rest.ensembl.org | Genome annotations, cross-species |
| RepeatMasker | repeatmasker.org | TE annotations |
| PDG (Particle Data Group) | pdg.lbl.gov | Measured physical constants |

## First Target Gene

Pick ONE gene with known cancer/adult/fetal splice variants. Fold three ways. Compare.

**Candidates from vault data:**
- **LINC01235 (ANCHOR)** — present in adult, absent in fetal, destroyed in cancer
- **UHRF1** — 71% drop in senescence, 833 human-specific TEs
- **XIST** — sex-dependent gain control, dosage-variable

Start with ANCHOR. Three isoforms. Three folds. One night.

---

*No allocation ticket. No PI approval. Your laptop. Tonight.*
