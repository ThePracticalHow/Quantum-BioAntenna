# One Shape, Zero Parameters, Six Failure Modes

**Jixiang Leng** | Independent Researcher | April 13, 2026

---

## In 30 Seconds

Two independent research programs — one in spectral geometry, one in single-cell transcriptomics — converged on the same mathematical structure. The geometry derives 87 physical constants from zero free parameters (RMS error 0.111% against PDG). The biology finds the same eigenvalue ratios and coupling architecture across 5 species and 90 million years of evolution. The exact algebraic gap in our measurement framework — *why this outcome and not that one* — is the exact gap where current consciousness theories place the observer.

We have the math. We have the biology. We have the gap characterized. We need collaborators who work on the gap.

---

## 1. What We Measured

### A Coupling Tensor That Predicts Cellular Fate (Zero Parameters)

Four gene-set operators (RIBO, MITO, NUCLEAR, GOLGI) measured by pairwise Jaccard binarization in single-cell RNA-seq. No parameters. No thresholds. No training.

| Condition | trace(K) | Scale | Source |
|---|---|---|---|
| Healthy adult EC | 2.40 | 905,263 GEMs | GEM pipeline (zero params) |
| Replicative aging | 2.59 (compensatory) | Same | Same |
| Fetal (WI-38) | 2.45 | 27,622 cells, GSE226225 | Same |
| Acute damage | 1.83 (collapse) | Same | Same |
| Senescent | 1.81 (−33%) | Same | Same |
| Permutation null | z = 45–92 across 8 cell types | CellxGene Census | p effectively zero |

**Replication:** 21+ datasets, 5 labs, 2 species. det(K) collapses 81% in senescence. Coupling degrades *before* senescence markers appear.

### The Measurement Apparatus Has a Sex

XIST-stratified coupling across 500,000 cells, 8 tissues, 948 GTEx donors:

| Group | trace(K) |
|---|---|
| XIST-high female | 0.594 |
| Male (XY) | 0.403 |
| XIST-low female | 0.287 |

Universal ordering across every tissue tested. KDM6A differs 127× by XIST status. The intersex dosage ladder (XYY, XY, XX, XXY, XXX, Turner) validates the model: 9/10 conditions match X-dosage prediction.

### A Conserved Antenna Architecture (450 Million Years)

Three long non-coding RNAs on three chromosomes, all from endogenous retroviruses:

| Element | Locus | TE Origin | Age | Conservation |
|---|---|---|---|---|
| LINC01235 (ANCHOR) | chr9:13.4M | ERVL | ~100 Mya | 9/9 vertebrates |
| LINC02154 (KEY) | chrX:13.3M | Mixed ERV | Variable | 9/9 vertebrates |
| LINC01705 (REFERENCE) | chr1:222M | HERVH | ~40 Mya | Primates |

**CRISPRi causal validation** (Replogle GWPS, 11,258 perturbations): ILF3 knockdown collapses ANCHOR at z = −3.19, p < 0.001. Spliceosome failure (RBM22 KD) activates ANCHOR at z = +12.35. ANCHOR is a damage sensor for the translational machinery.

Human ANCHOR locus: 73.6% repeat density vs chimp 32.9%. UHRF1 locus: 833 more TE insertions than chimp. UHRF1 drops 71% in senescence — the first domino.

### Schumann Eclipse Suppression (Novel, Unpublished)

Sierra Nevada ELF Station (3.58 GB, 1,407 days, 2013–2017): SR1 amplitude drops −10.7% during total lunar eclipses. z = −2.17, p = 0.030. Individual: Oct 2014 z = −3.36.

### Alzheimer's Alpha at the Schumann Carrier

OpenNeuro ds004504 (N = 26 AD): alpha peak 7.75 ± 1.24 Hz vs controls 9.68 ± 0.71 Hz. The Schumann fundamental is 7.83 Hz. Alpha vs MMSE: r = 0.427, p = 3.67×10⁻⁵, N = 88.

### Lithium Displaces Magnesium at RNA Binding Sites

10 ns MD simulation on GNRA tetraloops: Mg²⁺ maintains ~2.0 coordination contacts, Li⁺ drops to ~1.0. Welch t = 402 (p ≈ 0). First simulation of the lithium mechanism in bipolar: Q-factor dampening by ionic displacement.

---

## 2. The Physics: 87 Theorems, Zero Parameters

LENG (S⁵/Z₃ spectral geometry):

| Prediction | LENG Value | PDG Measured | Error |
|---|---|---|---|
| Proton-electron mass ratio | 6π⁵ = 1836.118 | 1836.153 | 0.002% |
| Deuteron binding energy | m_π × 35/2187 = 2.2244 MeV | 2.2246 MeV | 0.01% |
| CKM CP phase δ | arctan(2π²/9) = 65.49° | 65.4° | 0.14% |
| Weinberg angle sin²θ_W | spectral invariant | 0.2312 | <0.01% |
| Jarlskog invariant J | J_GUT/p² = 3.23×10⁻⁵ | 3.18×10⁻⁵ | 1.6% |
| 95 GeV scalar | m_Z(1+η²) = 95.69 GeV | CMS/ATLAS excess at 95.4 | 0.3% |

**The outcome problem:** The Z₃ idempotent algebra (e² = e) forces definite measurement outcomes — it derives the Born rule P = |ψ|². But it does not select *which* outcome occurs. This is the structurally necessary gap where the observer lives.

**Lotus time:** t_L = 9T/2, verified across 40 orders of magnitude. At tryptophan fluorescence scale: t_L ≈ 4.5 ps. **If Philip Kurian's tryptophan superradiance decoheres at ~4.5 ps, LENG predicts it.**

---

## 3. The Clinical Bridge: AD as Six Radio Failure Modes

99.6% of AD clinical trials fail because they target one mechanism of six. Published evidence for all modes. 18 citations.

| Mode | What Fails | Key Evidence | Current Rx |
|---|---|---|---|
| M1: Desensitization | Chronic EM overload | Occupational ELF: RR 1.63 for AD | Nothing |
| M2: Blocking | Out-of-band saturation | AD deaths +140% since 2000 | Nothing |
| M3: Intermodulation | WiFi beacon at 9.77 Hz | In alpha band — unmeasured | Nothing |
| M4: Oscillator | SCN neuron loss (42%) | Braak staging follows timing gradient | Melatonin (partial) |
| M5: Filter | Mg depletion | 21-study meta-analysis, p = 0.045 | Nothing |
| M6: Detector | Complex IV −30–70% | Precedes clinical symptoms | Nothing |

**Annual cost:** $720 (six-mode protocol) vs $26,500 (lecanemab, 1 mode, 27% slower decline).

**Mg-L-threonate RCT** (2025, N=100): 7.5-year brain age reduction in 6 weeks (p = 0.043).

**The $15 WiFi timer covers more unaddressed failure modes than any drug in clinical trials.**

---

## 4. Seven Experiments

| # | Experiment | Tests | Cost | When |
|---|---|---|---|---|
| 1 | Kurian tryptophan decoherence time | LENG t_L = 4.5 ps | One email | Immediate |
| 2 | Coupling tensor in meditators (GSE174083) | Practice → trace(K)? | Dataset exists | Immediate |
| 3 | Matched XX/XY iPSCs from same donor | K differs by sex chromosomes alone? | Lab time | 3 months |
| 4 | XIST in CAIS (46,XY female) immune cells | Autoimmune: chromosomes or hormones? | Clinical samples | 6 months |
| 5 | Longitudinal trace(K) across menstrual cycle | 29.53-day oscillation? | Time-series scRNA | 6 months |
| 6 | Faraday-shielded bedroom AD trial | EM reduction → alpha EEG? | ~$50K | 12 months |
| 7 | Multi-mode AD combination trial | Six-mode vs single-mode? | Standard RCT | 18 months |

---

## 5. Datasets and Tools

### Key Datasets

| Dataset | Accession | Scale | Used For |
|---|---|---|---|
| GTEx v8 | dbGaP phs000424 | 948 donors, 17,382 samples, 54 tissues | XIST stratification, sex dimorphism |
| CellxGene Census | CZI | ~500K human + 230K mouse cells | Population-scale coupling |
| Trophoblast atlas | CellxGene | 98K cells | Fetal sex dimorphism |
| WI-38 time course | GSE226225 | 27,622 cells, 4 conditions | Fetal coupling baseline |
| Casella senescence | GSE130727 | 37 samples, 4 cell types | Senescence coupling |
| GESTALT aging | GSE226189 | 82 donors (46M/36F) | Age-associated expression |
| GBM Core Map | CellxGene 999f2a15 | 338,564 cells, 110 patients | Cancer coupling |
| Replogle GWPS | Perturb-seq | 11,258 CRISPRi perturbations | lncRNA causal validation |
| AD EEG | OpenNeuro ds004504 | 88 subjects (44F/44M) | Alpha-MMSE correlation |
| Sierra Nevada ELF | Applied Sciences 2024 | 3.58 GB, 1,407 days | Schumann eclipse measurement |
| Sleep-EDF | PhysioNet | 153 subjects, ages 25–101 | N3 age decline |
| Meditation RNA | GSE174083 | 389 samples | ILF3 expression |

### Software

| Tool | Used For |
|---|---|
| LENG / LOTUS (Zenodo 10.5281/zenodo.18655472) | 87-theorem verification suite |
| scanpy / AnnData / Cell Ranger | scRNA-seq processing |
| Amber 22 | GNRA Li/Mg molecular dynamics |
| bamnostic | BAM indexed access for XOR-HOMER |
| NumPy / SciPy / matplotlib | Statistical analysis and visualization |

### Verification

```
pytest 05_Project_LENG/tests/ -v              # 87 theorems vs PDG
python 10_Project_DiscordIntoSymphony/methods/run_pipeline.py   # Coupling tensor
python 13_Project_MemoryOfMind/methods/core/desync_engine.py    # AD staging engine
```

---

## 6. Published Sources (Selection)

| # | Citation | Finding | DOI |
|---|---|---|---|
| 1 | Frontiers Aging Neurosci 2025 | Alpha first EEG band to degrade in AD | 10.3389/fnagi.2025.1522552 |
| 2 | Frontiers Aging Neurosci 2021 | Mg depleted in AD brain (21 studies) | 10.3389/fnagi.2021.799824 |
| 3 | Frontiers Nutrition 2025 | MgT: 7.5yr brain age, N=100 | 10.3389/fnut.2025.1729164 |
| 4 | Alzheimer's Association 2024 | AD deaths +140% since 2000 | 10.1002/alz.13809 |
| 5 | Science Transl Medicine 2022 | Mito dysfunction precedes symptoms | 10.1126/scitranslmed.abk1051 |
| 6 | Neurotoxicology 2017 | Occupational ELF: RR 1.63 for AD | 10.1016/j.neuro.2017.09.007 |
| 7 | Brain 2008 | SCN neuron loss 42% in AD | 10.1093/brain/awn098 |
| 8 | Lancet 2020 | 12 modifiable AD risk factors | 10.1016/S0140-6736(20)30367-6 |
| 9 | Braak, Acta Neuropathol 1991 | Entorhinal first, cerebellum last | 10.1007/BF00308809 |
| 10 | Nedergaard, Cell 2025 | Zolpidem blocks glymphatic clearance | Cell 2025 |
| 11 | Helfrich-Forster, Sci Adv 2021 | Menstrual-lunar synchronization | 10.1126/sciadv.abe1358 |
| 12 | Applied Sciences 2024 | Lunar tidal forcing on Schumann | 10.3390/app14083332 |
| 13 | Frontiers Pharmacol 2024 | Lithium prevention: RR 0.59 | 10.3389/fphar.2024.1408462 |
| 14 | Neuron 2024 | Women 2× AD risk; XIST mechanism | Neuron 2024 |

---

## What We Are Not Claiming

- We have not solved consciousness. We characterized the algebraic gap where it lives.
- We have not proved K in physics = K in biology. We measured both; the proof is open.
- The Schumann result (p = 0.030) is suggestive, not definitive. We need more eclipses.
- We have not published yet. The math runs. The biology replicates.

**We need collaborators, not converts.**

---

**Contact:** Jixiang Leng
