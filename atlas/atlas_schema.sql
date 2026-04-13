-- Binary Atlas Schema v0.1
-- The cell is the atom. Everything else is a property of the cell.
-- Coupling tensor is a VIEW computed from any grouping of cells.

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ============================================================
-- LAYER 0: The Cell (the atom of the atlas)
-- ============================================================

CREATE TABLE IF NOT EXISTS cells (
    cell_id         TEXT PRIMARY KEY,   -- globally unique: {accession}_{barcode} or {accession}_{index}
    accession       TEXT NOT NULL,      -- GEO/SRA/CellxGene accession
    donor_id        TEXT,               -- donor/patient ID within study
    barcode         TEXT,               -- cell barcode (10x) or read name (Nanopore)

    -- Metadata (searchable)
    tissue          TEXT NOT NULL,
    species         TEXT NOT NULL DEFAULT 'human',
    age_group       TEXT,               -- fetal, pediatric, adult, elderly
    age_years       REAL,               -- exact age if known
    sex             TEXT,               -- M, F, unknown
    disease         TEXT DEFAULT 'healthy',
    treatment       TEXT,
    timepoint       TEXT,
    cell_type       TEXT,               -- annotated cell type if available

    -- Provenance
    lab             TEXT,
    country         TEXT,
    platform        TEXT,               -- 10x_chromium, nanopore_directRNA, smartseq2, etc.
    date_ingested   TEXT DEFAULT (date('now')),

    -- Binary transcript (Layer 0)
    -- Base-4 encoded: A=00, T=01, C=10, G=11
    -- Stored as JSON dict: {gene_symbol: binary_string}
    -- NULL for h5ad-only ingests (count matrix only)
    binary_transcript TEXT,

    -- Count-level summary (always available)
    n_genes_detected INTEGER,
    total_umi       INTEGER
);

CREATE INDEX IF NOT EXISTS idx_cells_tissue ON cells(tissue);
CREATE INDEX IF NOT EXISTS idx_cells_disease ON cells(disease);
CREATE INDEX IF NOT EXISTS idx_cells_species ON cells(species);
CREATE INDEX IF NOT EXISTS idx_cells_accession ON cells(accession);
CREATE INDEX IF NOT EXISTS idx_cells_age ON cells(age_group);
CREATE INDEX IF NOT EXISTS idx_cells_sex ON cells(sex);
CREATE INDEX IF NOT EXISTS idx_cells_treatment ON cells(treatment);
CREATE INDEX IF NOT EXISTS idx_cells_cell_type ON cells(cell_type);

-- ============================================================
-- LAYER 1: Operator Totals (per cell)
-- ============================================================

CREATE TABLE IF NOT EXISTS operators (
    cell_id         TEXT PRIMARY KEY REFERENCES cells(cell_id),
    ribo_total      INTEGER NOT NULL,   -- sum of RPS* + RPL* UMI counts
    mito_total      INTEGER NOT NULL,   -- sum of MT-* counts
    golgi_total     INTEGER NOT NULL,   -- sum of GOLGA/B + SEC61 + COPA/B + MAN1 + MGAT + GORASP
    nuclear_total   INTEGER NOT NULL,   -- total - ribo - mito - golgi
    total           INTEGER NOT NULL
);

-- ============================================================
-- LAYER 2: Coupling Tensor (per condition -- COMPUTED VIEW)
-- Conditions are ad-hoc groupings. The tensor is recomputed
-- from operator totals for any set of cells you query.
-- This table caches pre-computed tensors for known groupings.
-- ============================================================

CREATE TABLE IF NOT EXISTS conditions (
    condition_id    TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    tissue          TEXT,
    disease         TEXT,
    accession       TEXT,
    n_cells         INTEGER,
    description     TEXT
);

CREATE TABLE IF NOT EXISTS coupling_tensor (
    condition_id    TEXT PRIMARY KEY REFERENCES conditions(condition_id),
    n_cells         INTEGER,
    ribo_indep      REAL,
    det_k           REAL,
    trace_k         REAL,
    k_rm            REAL,       -- RIBO-MITO Spearman
    k_rn            REAL,       -- RIBO-NUCLEAR
    k_rg            REAL,       -- RIBO-GOLGI
    k_mn            REAL,       -- MITO-NUCLEAR
    k_mg            REAL,       -- MITO-GOLGI
    k_ng            REAL        -- NUCLEAR-GOLGI
);

-- ============================================================
-- LAYER 3: Junctions (per junction per cell -- BAM/Nanopore only)
-- ============================================================

CREATE TABLE IF NOT EXISTS junctions (
    junction_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    cell_id         TEXT REFERENCES cells(cell_id),
    chrom           TEXT NOT NULL,
    start_pos       INTEGER NOT NULL,
    end_pos         INTEGER NOT NULL,
    xor_code        INTEGER,            -- 0=identity, 1=complement, 2=transversion, 3=transition
    left_base       TEXT,               -- last exonic base before cut
    right_base      TEXT,               -- first exonic base after cut
    intron_size     INTEGER,
    frame_intact    INTEGER             -- 1 if intron_size % 3 == 0
);

CREATE INDEX IF NOT EXISTS idx_junctions_cell ON junctions(cell_id);
CREATE INDEX IF NOT EXISTS idx_junctions_locus ON junctions(chrom, start_pos, end_pos);

-- ============================================================
-- LAYER 4: Splice Chains (per molecule -- Nanopore only)
-- ============================================================

CREATE TABLE IF NOT EXISTS chains (
    molecule_id     TEXT PRIMARY KEY,   -- read name
    cell_id         TEXT REFERENCES cells(cell_id),
    chain_hash      TEXT,               -- hash of the full exon-junction sequence
    n_junctions     INTEGER,
    n_exons         INTEGER,
    chain_json      TEXT                -- full chain as JSON array
);

CREATE INDEX IF NOT EXISTS idx_chains_cell ON chains(cell_id);
CREATE INDEX IF NOT EXISTS idx_chains_hash ON chains(chain_hash);

-- ============================================================
-- LAYER 5: Structural (per excised intron)
-- ============================================================

CREATE TABLE IF NOT EXISTS structural (
    intron_id       TEXT PRIMARY KEY,
    condition_id    TEXT REFERENCES conditions(condition_id),
    chrom           TEXT,
    start_pos       INTEGER,
    end_pos         INTEGER,
    size            INTEGER,
    sequence        TEXT,               -- full nucleotide sequence
    gc_pct          REAL,
    mfe             REAL,               -- kcal/mol (ViennaRNA)
    mfe_per_nt      REAL,
    pct_paired      REAL,
    stems           INTEGER,
    dot_bracket     TEXT                -- secondary structure
);

-- ============================================================
-- LAYER 6: Proteins (future -- base64 amino acid encoding)
-- ============================================================

CREATE TABLE IF NOT EXISTS proteins (
    protein_id      TEXT PRIMARY KEY,
    cell_id         TEXT REFERENCES cells(cell_id),
    gene            TEXT,
    sequence_b64    TEXT,               -- base64-encoded amino acid sequence
    length_aa       INTEGER,
    fold_state      TEXT                -- predicted fold if available
);

-- ============================================================
-- AGGREGATE VIEWS (computed from cells + operators)
-- ============================================================

-- Per-condition XOR summary (cached from STAFF base4 runs)
CREATE TABLE IF NOT EXISTS base4_xor (
    condition_id    TEXT PRIMARY KEY REFERENCES conditions(condition_id),
    identity_pct    REAL,
    complement_pct  REAL,
    transversion_pct REAL,
    transition_pct  REAL,
    gc_pct          REAL,
    n_junctions     INTEGER,
    platform        TEXT
);

-- Per-condition reading frame summary
CREATE TABLE IF NOT EXISTS reading_frame (
    condition_id    TEXT PRIMARY KEY REFERENCES conditions(condition_id),
    frame0_pct      REAL,
    stop_split_pct  REAL,
    atg_near_pct    REAL,
    stop_near_pct   REAL,
    start_near_pct  REAL,
    stop_density    REAL
);

-- Per-condition splice chain summary
CREATE TABLE IF NOT EXISTS splice_chains (
    condition_id    TEXT PRIMARY KEY REFERENCES conditions(condition_id),
    uniqueness_pct  REAL,
    j0_divergence_pct REAL,
    mean_chain_length REAL,
    n_molecules     INTEGER
);

-- ============================================================
-- METADATA
-- ============================================================

CREATE TABLE IF NOT EXISTS atlas_meta (
    key             TEXT PRIMARY KEY,
    value           TEXT
);

INSERT OR REPLACE INTO atlas_meta VALUES ('schema_version', '0.1');
INSERT OR REPLACE INTO atlas_meta VALUES ('created', date('now'));
INSERT OR REPLACE INTO atlas_meta VALUES ('description', 'Binary Atlas: the cell is the atom. Everything else is a property of the cell.');
