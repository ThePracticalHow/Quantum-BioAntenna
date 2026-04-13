# Quantum Biology — Spliceosome as Quantum Router

## For Stefano: Email Package

**Attach these two PDFs. Nothing else needed.**

| File | What it is |
|---|---|
| `email_package/Spliceosome_Quantum_Router_Leng_2026.pdf` | The main document. 14 pages. 7 figures. Spliceosome data + why light works + why sound works + AD six-mode model + 6 collaboration proposals. |
| `email_package/Unclarity_Map_Alzheimers_Six_Failure_Modes.pdf` | Clinical companion. AD as 6 radio failure modes. 18 published sources. $60/month vs $26,500/year. |

## Answers to Stefano's Papers (From Stefano/)

Stefano sent three papers asking why light and sound do what they do:

- **Tummo meditation** -- Monks generate internal heat through breath and visualization. Framework answer: sustained conscious measurement events recouple K_RM through metabolic + respiratory + attentional channels simultaneously.
- **Vibration and gene expression** -- Mechanical vibration changes gene expression. Framework answer: cytoskeleton is piezoelectric (collagen d ~ 0.2-2.0 pC/N). Vibration produces local electric fields = measurement events on GOLGI/NUCLEAR operators. Changes in expression are the CONSEQUENCE of operator recoupling.
- **Vibronic principles** -- Vibration-assisted electronic transitions. Framework answer: this IS the phonon antenna (Plenio 2012). Our reframe: the antenna bandwidth (>16 THz for 60 fs decoherence) means the receiver reads FASTER than decoherence destroys. Fast decoherence is the spec, not the limitation.

## Project Structure

```
quantum_biology/
├── email_package/          2 PDFs — ATTACH THESE
├── forum_figures/          7 PNGs — slides if needed
├── tools/                  9 STAFF Python scripts
├── ipclean_md/             Mg/Li MD results (personal laptop, OpenMM)
├── From Stefano/           3 papers he sent us
├── _archive/               Superseded docs + raw data JSONs
│   ├── superseded_docs/    11 fused documents
│   └── raw_data/           38 data files + 5 FASTAs
│
├── FOR_STEFANO.md          Canonical master brief (378 lines)
├── HOSTILE_REVIEWER_PROOF.md  Every claim, every number, every source
├── GLOBAL_SOURCE_MAP.md    9 claims x international literature
├── IP_FIREWALL.md          What's NIH vs what's yours
├── korean_nsclc_tensor.json   Primary GREEN dataset result
├── structural_atlas_results.json  11 folded introns (ViennaRNA)
├── wings_database.json     Unified JSON database (85 KB)
├── wings_above_morning.db  SQLite database (32 KB)
│
├── build_email_package.py     Regenerate the main PDF
├── generate_forum_figures.py  Regenerate all 7 figures
├── fold_isoforms.py           ViennaRNA intron folding
└── replicate_md_ipclean.py    IP-clean Mg/Li MD (OpenMM)
```

## Quick Commands

```bash
python build_email_package.py      # Rebuild the main PDF
python generate_forum_figures.py   # Rebuild all 7 figures
python fold_isoforms.py            # Re-fold 11 introns
python replicate_md_ipclean.py --mode all --metal Mg --steps 50000
python replicate_md_ipclean.py --mode all --metal Li --steps 50000
```
