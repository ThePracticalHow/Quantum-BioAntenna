# coding: utf-8
"""
Build unified binary transcriptome + coupling tensor database.
All results from the April 9-12 2026 session.
"""
import json, os, sqlite3, glob

DB_PATH = os.path.join(os.path.dirname(__file__), 'wings_above_morning.db')
RESULTS_DIR = r'c:\tmp\binary_results'

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def build():
    # Collect all results
    files = glob.glob(os.path.join(RESULTS_DIR, '*.json'))
    print(f'Found {len(files)} result files')

    # Build SQLite database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Table: cell_types (master catalog)
    c.execute('''CREATE TABLE IF NOT EXISTS cell_types (
        id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        tissue TEXT,
        dataset TEXT,
        n_cells INTEGER,
        n_reads INTEGER,
        platform TEXT
    )''')

    # Table: coupling_tensor
    c.execute('''CREATE TABLE IF NOT EXISTS coupling_tensor (
        cell_type_id TEXT,
        condition TEXT,
        n_cells INTEGER,
        ribo_indep REAL,
        det_k REAL,
        k_rm REAL, k_rn REAL, k_rg REAL,
        k_mn REAL, k_mg REAL, k_ng REAL,
        FOREIGN KEY (cell_type_id) REFERENCES cell_types(id)
    )''')

    # Table: base4_xor
    c.execute('''CREATE TABLE IF NOT EXISTS base4_xor (
        cell_type_id TEXT,
        xor_identity REAL,
        xor_complement REAL,
        xor_transversion REAL,
        xor_transition REAL,
        gc_content REAL,
        n_junctions INTEGER,
        platform TEXT,
        FOREIGN KEY (cell_type_id) REFERENCES cell_types(id)
    )''')

    # Table: reading_frame
    c.execute('''CREATE TABLE IF NOT EXISTS reading_frame (
        cell_type_id TEXT,
        frame_preserving_pct REAL,
        stop_at_split_pct REAL,
        atg_near_junction_pct REAL,
        stop_near_junction_pct REAL,
        lys_before_junction_pct REAL,
        leu_after_junction_pct REAL,
        FOREIGN KEY (cell_type_id) REFERENCES cell_types(id)
    )''')

    # Table: splice_history
    c.execute('''CREATE TABLE IF NOT EXISTS splice_history (
        cell_type_id TEXT,
        n_spliced INTEGER,
        unique_chains INTEGER,
        chain_uniqueness_pct REAL,
        unique_introns INTEGER,
        total_excisions INTEGER,
        median_intron_size INTEGER,
        mirna_range_pct REAL,
        snorna_range_pct REAL,
        FOREIGN KEY (cell_type_id) REFERENCES cell_types(id)
    )''')

    # Table: de_novo_junctions
    c.execute('''CREATE TABLE IF NOT EXISTS denovo_junctions (
        cell_type_id TEXT,
        unique_junctions INTEGER,
        unique_splice_sigs INTEGER,
        rare_junction_pct REAL,
        median_junction_size INTEGER,
        FOREIGN KEY (cell_type_id) REFERENCES cell_types(id)
    )''')

    # Insert cell types
    cell_types = [
        ('h9_nanopore', 'H9 Embryonic Stem', 'fetal', 'embryo', 'SGNex', 0, 337364, 'nanopore_directRNA'),
        ('k562_nanopore', 'K562 Blood Cancer (CML)', 'cancer', 'blood', 'SGNex', 0, 554250, 'nanopore_directRNA'),
        ('hepg2_nanopore', 'HepG2 Liver Cancer', 'cancer', 'liver', 'SGNex', 0, 1095654, 'nanopore_directRNA'),
        ('k562_illumina', 'K562 Blood Cancer (Illumina)', 'cancer', 'blood', 'SGNex', 0, 0, 'illumina'),
        # Lab coculture data removed (see IP_FIREWALL.md)
        ('wi38_10x', 'WI-38 Fetal Lung Fibroblast', 'fetal', 'lung', 'GSE226225_SRA', 0, 158780246, '10x_chromium'),
        ('nsclc_tumor', 'Korean NSCLC Primary Tumor', 'cancer', 'lung', 'GSE131907', 45149, 0, '10x_chromium'),
        ('nsclc_normal', 'Korean NSCLC Normal Lung', 'normal', 'lung', 'GSE131907', 42995, 0, '10x_chromium'),
        ('nsclc_ln', 'Korean NSCLC Lymph Node', 'metastatic', 'lymph_node', 'GSE131907', 37446, 0, '10x_chromium'),
        ('nsclc_effusion', 'Korean NSCLC Effusion', 'metastatic', 'pleural', 'GSE131907', 20304, 0, '10x_chromium'),
        ('nsclc_stroma', 'Korean NSCLC Normal Stroma', 'normal', 'lung_stroma', 'GSE131907', 29060, 0, '10x_chromium'),
        ('nsclc_ebus', 'Korean NSCLC EBUS Biopsy', 'transition', 'lung_biopsy', 'GSE131907', 27561, 0, '10x_chromium'),
        ('nsclc_broncho', 'Korean NSCLC Bronchoscopy', 'field_effect', 'airway', 'GSE131907', 5991, 0, '10x_chromium'),
        ('normal_adult_lung', 'Normal Adult Lung', 'normal', 'lung', 'GSE150247', 22427, 0, '10x_chromium'),
        ('gse250041_prolif', 'Proliferating Cells', 'proliferative', 'culture', 'GSE250041', 8664, 0, '10x_chromium'),
        ('gse250041_senes', 'Senescent Cells', 'senescent', 'culture', 'GSE250041', 4949, 0, '10x_chromium'),
        ('gbm_all', 'GBM All Tumors', 'cancer', 'brain', 'GSE131928', 7930, 0, 'smartseq2'),
        ('wi38_ctrl', 'WI-38 Control PDL24', 'fetal', 'lung', 'GSE226225', 5608, 0, '10x_chromium'),
        ('wi38_eto', 'WI-38 Etoposide Senescent', 'senescent', 'lung', 'GSE226225', 7732, 0, '10x_chromium'),
        ('wi38_ir', 'WI-38 Radiation Senescent', 'senescent', 'lung', 'GSE226225', 8692, 0, '10x_chromium'),
        ('wi38_rs', 'WI-38 Replicative Senescent', 'senescent', 'lung', 'GSE226225', 5590, 0, '10x_chromium'),
        # D01 cell types removed (NIH lab data, see IP_FIREWALL.md)
    ]
    c.executemany('INSERT OR REPLACE INTO cell_types VALUES (?,?,?,?,?,?,?,?)', cell_types)

    # Insert coupling tensor data
    tensor_entries = [
        ('nsclc_tumor', 'TUMOR', 45149, 0.310, 0.058, 0.686, 0.741, 0.642, 0.733, 0.672, 0.827),
        ('nsclc_normal', 'NORMAL', 42995, 0.220, 0.018, 0.772, 0.839, 0.730, 0.874, 0.777, 0.853),
        ('nsclc_ln', 'LYMPH_NODE', 37446, 0.508, 0.278, 0.492, 0.652, 0.331, 0.551, 0.300, 0.523),
        ('nsclc_effusion', 'EFFUSION', 20304, 0.416, 0.125, 0.655, 0.673, 0.425, 0.698, 0.510, 0.696),
        ('nsclc_stroma', 'NORMAL_STROMA', 29060, 0.206, 0.017, 0.726, 0.848, 0.809, 0.796, 0.789, 0.900),
        ('nsclc_ebus', 'EBUS', 27561, 0.284, 0.036, 0.716, 0.757, 0.675, 0.775, 0.716, 0.874),
        ('nsclc_broncho', 'BRONCHO', 5991, 0.387, 0.113, 0.668, 0.681, 0.489, 0.642, 0.482, 0.753),
        ('normal_adult_lung', 'ALL', 22427, 0.295, 0.072, 0.664, 0.000, 0.642, 0.000, 0.000, 0.000),
        ('gse250041_prolif', 'Proliferating', 8664, 0.154, 0.003, 0.650, 0.000, 0.931, 0.000, 0.000, 0.000),
        ('gse250041_senes', 'Senescent', 4949, 0.276, 0.017, 0.445, 0.000, 0.836, 0.000, 0.000, 0.000),
        ('gbm_all', 'ALL_GBM', 7930, 0.890, 0.000, 0.000, 0.000, 0.139, 0.000, 0.000, 0.000),
        # D01 tensor entries removed (NIH lab data)
        ('wi38_ctrl', 'CTRL_2', 5608, 0.345, 0.050, 0.406, 0.000, 0.761, 0.000, 0.000, 0.000),
        ('wi38_eto', 'ETO', 7732, 0.396, 0.000, -0.028, 0.000, 0.855, 0.000, 0.000, 0.000),
        ('wi38_ir', 'IR', 8692, 0.373, 0.000, 0.049, 0.000, 0.890, 0.000, 0.000, 0.000),
        ('wi38_rs', 'RS', 5590, 0.340, 0.000, 0.000, 0.000, 0.895, 0.000, 0.000, 0.000),
    ]
    c.executemany('INSERT OR REPLACE INTO coupling_tensor VALUES (?,?,?,?,?,?,?,?,?,?,?)', tensor_entries)

    # Insert base4 XOR data
    base4_entries = [
        ('h9_nanopore', 36.74, 15.35, 18.34, 29.56, 47.47, 1287041, 'nanopore'),
        ('k562_nanopore', 44.16, 15.80, 14.31, 25.72, 48.55, 1677665, 'nanopore'),
        ('hepg2_nanopore', 43.71, 15.67, 14.74, 25.87, 48.71, 0, 'nanopore'),
        ('wi38_10x', 48.75, 16.55, 12.03, 22.67, 0, 35880514, '10x'),
        # Lab data removed (see IP_FIREWALL.md)
    ]
    c.executemany('INSERT OR REPLACE INTO base4_xor VALUES (?,?,?,?,?,?,?,?)', base4_entries)

    # Insert reading frame data
    frame_entries = [
        ('h9_nanopore', 33.0, 2.33, 20.0, 52.9, 9.1, 27.5),
        ('k562_nanopore', 32.2, 1.84, 24.1, 47.9, 11.3, 30.1),
        ('hepg2_nanopore', 31.9, 1.77, 0, 0, 0, 0),
        ('wi38_10x', 32.9, 1.66, 24.5, 47.9, 14.3, 28.6),
    ]
    c.executemany('INSERT OR REPLACE INTO reading_frame VALUES (?,?,?,?,?,?,?)', frame_entries)

    # Insert splice history data
    splice_entries = [
        ('h9_nanopore', 233258, 233207, 99.98, 241159, 1287041, 972, 14.0, 24.9),
        ('k562_nanopore', 357597, 354011, 99.0, 131558, 1677665, 740, 15.9, 29.4),
        ('hepg2_nanopore', 782326, 769766, 98.4, 182929, 4477127, 874, 12.9, 24.8),
    ]
    c.executemany('INSERT OR REPLACE INTO splice_history VALUES (?,?,?,?,?,?,?,?,?)', splice_entries)

    conn.commit()

    # Verify
    c.execute('SELECT COUNT(*) FROM cell_types')
    print(f'Cell types: {c.fetchone()[0]}')
    c.execute('SELECT COUNT(*) FROM coupling_tensor')
    print(f'Tensor entries: {c.fetchone()[0]}')
    c.execute('SELECT COUNT(*) FROM base4_xor')
    print(f'Base4 entries: {c.fetchone()[0]}')
    c.execute('SELECT COUNT(*) FROM reading_frame')
    print(f'Frame entries: {c.fetchone()[0]}')
    c.execute('SELECT COUNT(*) FROM splice_history')
    print(f'Splice history entries: {c.fetchone()[0]}')

    # Print the full independence axis
    print('\n=== THE INDEPENDENCE AXIS ===')
    c.execute('SELECT ct.name, ct.category, ct.tissue, t.ribo_indep, t.k_rg, t.n_cells FROM coupling_tensor t JOIN cell_types ct ON t.cell_type_id = ct.id ORDER BY t.ribo_indep')
    for row in c.fetchall():
        print(f'  {row[3]:.3f}  {row[0]:40s}  {row[1]:15s}  {row[2]:15s}  K_RG={row[4]:.3f}  n={row[5]:,}')

    conn.close()

    # Also save as unified JSON
    unified = {
        'version': '1.0',
        'created': '2026-04-12',
        'project': '27_Project_WingsAboveMorning',
        'description': 'Binary transcriptome + coupling tensor database',
        'total_cells_analyzed': 500000,
        'total_reads_analyzed': 500000000,
        'datasets': 10,
        'cell_types': len(cell_types),
    }

    # Load all JSON results
    for f in files:
        key = os.path.basename(f).replace('.json', '')
        unified[key] = load_json(f)

    unified_path = os.path.join(os.path.dirname(__file__), 'wings_database.json')
    with open(unified_path, 'w') as f:
        json.dump(unified, f, indent=2)
    print(f'\nSaved: {unified_path}')

    db_size = os.path.getsize(DB_PATH)
    json_size = os.path.getsize(unified_path)
    print(f'SQLite: {DB_PATH} ({db_size/1024:.1f} KB)')
    print(f'JSON: {unified_path} ({json_size/1024:.1f} KB)')
    print('DONE')

if __name__ == '__main__':
    build()
