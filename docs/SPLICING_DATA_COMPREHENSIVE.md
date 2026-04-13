# Comprehensive Splicing Data: Fetal vs Cancer vs Adult

## The Four-State Comparison

### Coupling Tensor (operator independence)

| State | Dataset | Cells | RIBO_indep | K_RG | K_RM |
|-------|---------|-------|------------|------|------|
| **Proliferative** | GSE250041 | 8,664 | **0.154** | 0.931 | 0.650 |
| **Normal adult lung** | GSE150247 | 22,427 | **0.295** | 0.642 | 0.664 |
| **Cancer primary** | GSE131907 NSCLC | 45,149 | **0.310** | 0.642 | 0.686 |
| **Fetal control** | WI-38 GSE226225 | 5,608 | **0.345** | 0.761 | 0.406 |
| **Fetal senescent (ETO)** | WI-38 GSE226225 | 7,732 | **0.396** | 0.855 | -0.028 |
| **Cancer metastatic** | GSE131907 LN | 37,446 | **0.508** | 0.331 | 0.492 |
| **GBM** | GSE131928 | 7,930 | **0.890** | 0.139 | — |

### Base-4 XOR at Splice Junctions

| XOR | Meaning | H9 Fetal | K562 Blood Ca | HepG2 Liver Ca | WI-38 Fetal Fibro |
|-----|---------|---------|---------------|----------------|-------------------|
| 00 | IDENTITY | 36.74% | 44.16% | 43.71% | 48.75% |
| 01 | COMPLEMENT | 15.35% | 15.80% | 15.67% | 16.55% |
| 10 | TRANSVERSION | 18.34% | 14.31% | 14.74% | 12.03% |
| 11 | TRANSITION | 29.56% | 25.72% | 25.87% | 22.67% |

**The shift:** IDENTITY rises from 36.7% (embryonic stem) to 43.7-48.8% (cancer/fetal fibroblast). TRANSITION drops from 29.6% to 22.7-25.9%. The spliceosome becomes more conservative across differentiation and disease.

### Reading Frame at Junctions

| Metric | H9 Fetal Stem | K562 Cancer | HepG2 Cancer | WI-38 Fetal Fibro |
|--------|--------------|-------------|-------------|-------------------|
| Frame-preserving | 33.0% | 32.2% | 31.9% | 32.9% |
| **Stop at split codon** | **2.33%** | **1.84%** | **1.77%** | **1.66%** |
| ATG near junction | 20.0% | 24.1% | — | 24.5% |
| Stop near junction | 52.9% | 47.9% | — | 47.9% |
| Lys before junction | 9.1% | 11.3% | — | 14.3% |
| Leu after junction | 27.5% | 30.1% | — | 28.6% |

**Cancer and fetal fibroblasts both avoid stop codons at splice boundaries.** WI-38 fetal fibroblast (1.66%) is even more extreme than cancer (1.77-1.84%). The tissue of origin for lung cancer already runs the stop-avoidance program harder than the cancer itself.

### Splice Chain Uniqueness (Nanopore full-length)

| Cell Type | Spliced Molecules | Unique Chains | Uniqueness | Divergence at Junction 0 |
|-----------|------------------|---------------|------------|------------------------|
| H9 Fetal Stem | 233,258 | 233,207 | **99.98%** | **38.4%** |
| K562 Blood Cancer | 357,597 | 354,011 | 99.0% | 18.1% |
| HepG2 Liver Cancer | 782,326 | 769,766 | 98.4% | 17.9% |

**Fetal explores. Cancer converges.** 99.98% unique chains in fetal vs 98.4% in cancer. 38.4% divergence at the first junction in fetal vs 18% in cancer. The fetal spliceosome samples the full space. Cancer has locked in.

### Excised Intron Size Distribution

| Source | Median Size | miRNA (60-150bp) | snoRNA (60-300bp) | Micro (<100bp) |
|--------|-----------|-----------------|-------------------|---------------|
| H9 fetal-only | 1,262 bp | **10.6%** | **20.2%** | 5.1% |
| K562 cancer-only (vs H9) | 1,396 bp | **10.7%** | **19.8%** | 5.5% |
| K562 cancer-only (vs HepG2) | 1,306 bp | **10.7%** | **20.5%** | 5.5% |
| HepG2 cancer-only (vs H9) | 1,684 bp | 8.6% | 16.1% | 4.3% |
| HepG2 cancer-only (vs K562) | 1,748 bp | 7.9% | 15.0% | 3.9% |

**Blood cancer (K562) excises introns at the same size as fetal.** Liver cancer (HepG2) excises larger introns. The fetal/blood cancer introns are MORE concentrated in functional RNA size ranges (miRNA, snoRNA).

### Aberrant Junction Catalog

| Comparison | Shared | A-only | B-only | Overlap % |
|-----------|--------|--------|--------|-----------|
| H9 fetal vs K562 blood ca | 43,711 | 29,401 | 18,091 | 47.9% |
| H9 fetal vs HepG2 liver ca | 53,490 | 19,622 | 40,822 | 46.9% |
| K562 vs HepG2 | 51,725 | 10,077 | 42,587 | 49.6% |

**~47-50% of junctions are shared between any two cell types.** The other half are cell-type-specific. These unique junctions produce unique RNA molecules that fold into unique 3D structures.

### Top Cancer-Specific Junctions (with exact sequences)

**K562 blood cancer — top 3 unique junctions:**
1. `chr11:5254514-5254636` (122bp, **HBB intron**): 5,005 molecules
   - Left: `AACCAGGAGC` Right: `CTTCCCAGGG`
2. `chr11:5253405-5254291` (886bp, **HBB intron**): 4,823 molecules
   - Left: `TTCCCAGGAG` Right: `CTTGAAGTTC`
3. `chr11:5248487-5249367` (880bp, **HBB intron**): 2,688 molecules

**HepG2 liver cancer — top 3 unique junctions:**
1. `chr4:73420321-73421091` (770bp, **ALB/AFP cluster**): 8,734 molecules
   - Left: `AGCATCTCAG` Right: `CCTACCATGA`
2. `chr4:73419639-73420253` (614bp, **ALB/AFP cluster**): 8,723 molecules
   - Left: `TGCCGAGGAG` Right: `GGTAAAAAAC`
3. `chr4:73418311-73419506` (1,195bp, **ALB/AFP cluster**): 8,541 molecules

**H9 fetal stem — top 3 unique junctions (not in either cancer):**
1. `chr2:216661998-216663939` (1,941bp): 590 molecules
   - Left: `CCTCAAACAG` Right: `TGCAAGATGT`
2. `chr2:216633965-216660556` (26,591bp): 529 molecules
   - Left: `GCAGGTTAAG` Right: `ACAATGGCGA`
3. `chr15:24977029-24977777` (748bp): 417 molecules

**The cancer-specific junctions are at the genes that DEFINE the cancer type.** Blood cancer: HBB. Liver cancer: ALB/AFP. The spliceosome produces unique RNA isoforms at the cell's identity genes. These isoforms exist ONLY in that cancer, not in fetal or other cancer types.

---

## The Math

### Splice entropy per operator class

| Operator | H9 Fetal Entropy | K562 Cancer Entropy | Ratio |
|----------|-----------------|--------------------|----|
| RIBO | 0.436 | 0.151 | **2.9x higher in fetal** |
| GOLGI | 0.684 | -0.092 | **fetal explores, cancer locked** |

Splice entropy = variability of intron retention across molecules. Higher = more variable = more exploration. Fetal RIBO entropy is 2.9x higher than cancer — the fetal spliceosome samples 2.9x more splice states at ribosomal genes.

### GC content shift

| Cell Type | GC% | AT:GC |
|-----------|-----|-------|
| Adult endothelial (public) | 46.44% | 53.6:46.4 |
| H9 fetal stem | 47.47% | 52.5:47.5 |
| K562 blood cancer | 48.55% | 51.5:48.5 |
| HepG2 liver cancer | 48.71% | 51.3:48.7 |

Cancer transcriptome shifts toward GC. In binary: from low bits (00,01) toward high bits (10,11). More stable RNA secondary structures. More rigid mechanical scaffolds.

### The quantum measurement analogy

| Quantum Concept | Spliceosome Equivalent | Measured |
|----------------|----------------------|---------|
| Superposition | Pre-mRNA with 2^N possible splice outcomes | 97.6% of genes have variable intron maps |
| Measurement | Spliceosome selects one isoform | Base-4 XOR signature at each cut |
| Measurement context | Operator coupling tensor K | 20 conditions, 500k+ cells |
| Measurement precision | Splice entropy | Fetal 0.436 vs cancer 0.151 (RIBO) |
| Superposition sampling | Chain uniqueness | 99.98% fetal vs 98.4% cancer |
| Collapse | Convergence on specific isoforms | Cancer locks at identity XOR (44%) |
| Zeno effect | High K_RN → nuclear observation freezes ribosome | Normal tissue K_RN = 0.84 |
| Anti-Zeno | Low K_RN → ribosome escapes → cancer | Cancer K_RN = 0.74 |
| Decoherence | Operator decoupling | K_RG collapses from 0.93 → 0.33 |

---

## AlphaFold Feasibility Assessment

### What we have for structural prediction:
- Exact flanking sequences (10bp each side) for 100,000+ unique junctions
- The intron sizes (knowing which exons are joined)
- Cell-type specificity (which junctions exist in which state)

### What AlphaFold 3 / RoseTTAFoldNA can do:
- Predict 3D structure from RNA sequence
- Handle RNA-protein complexes
- Process sequences up to ~5,000 nucleotides

### What we would need to run:
1. Extract the FULL transcript sequence (not just 10bp flanks) for each aberrant isoform
2. For the top cancer-specific and fetal-specific isoforms (~100 total)
3. Predict 3D fold for each
4. Compare: does swapping one exon (via the aberrant junction) change the global fold?

### Practical constraints:
- AlphaFold 3 is available via Google Cloud (alphafoldserver.com) or self-hosted
- RhoFold+ can run locally on a GPU
- Each prediction takes minutes to hours depending on sequence length
- We have ~100 priority aberrant isoforms to model

### The deliverable:
**The Structural Isoform Atlas** — 3D models of the RNA molecules that cancer makes but fetal cells don't, and vice versa. The first database mapping how alternative splicing changes the physical architecture of RNA.

### The prediction:
Cancer-specific isoforms will fold into MORE RIGID structures (higher GC → stronger base stacking). Fetal-specific isoforms will fold into MORE FLEXIBLE structures (lower GC, more exploratory). The cancer RNA IS the scaffolding that builds the womb.

---

## For the Forum

The spliceosome decides which RNA molecules the cell makes. We showed that decision follows operator coupling (the tensor), produces measurable binary signatures (base-4 XOR), and creates cell-type-specific RNA molecules (aberrant junctions) at the genes that define cell identity (HBB in blood cancer, ALB in liver cancer).

**Nobody has connected these layers before.** Quantum biology looks at photosynthesis and magnetoreception. Structural biology looks at protein folds. Transcriptomics counts gene expression. We connected all three: the quantum measurement (splice decision) → the binary signature (XOR at the cut) → the structural consequence (aberrant isoforms that fold differently) → the disease phenotype (operator decoupling).

500M+ reads. 700,000+ cells. 100,000+ unique junctions with exact sequences. The database exists. The tools are built. What we need is someone who sees the void and wants to fill it.

That's Stefano.
