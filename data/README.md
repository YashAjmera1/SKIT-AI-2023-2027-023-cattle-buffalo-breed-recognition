# Indian Cattle and Buffalo Breed Recognition — Dataset & QA Module

**Module Lead:** Rajnish Kumar Patel (CSE-AI, Roll: 23ESKCA087)  
**Role:** Dataset & QA Lead (Data Acquisition, Preprocessing, Stratification, Quality Assurance)  
**Academic Project:** *Image-Based Breed Recognition System for Cattle and Buffalo in India*  
**Department:** Computer Science & Engineering (Artificial Intelligence), SKIT Jaipur  
**Project ID:** `SKIT/AI/2023-2027/023` (Session 2026–27)

---

## 1. Module Overview

The `data/` module houses the dataset catalog, metadata schemas, cleaning pipelines, stratified train/validation/test split generators, and automated quality assurance test suites. It manages 14 ICAR-NBAGR recognized indigenous breeds across cattle and buffalo:

### Supported Taxonomy (14 Breeds)
| Species | Common Breed Name | NBAGR Accession Code | Native Geographic Distribution |
| :--- | :--- | :--- | :--- |
| **Cattle** (*Bos indicus*) | Gir | INDIA_CATTLE_0400_GIR_03003 | Saurashtra, Gujarat |
| **Cattle** (*Bos indicus*) | Hariana | INDIA_CATTLE_0500_HARIANA_03004 | Rohtak, Jind, Hisar, Haryana |
| **Cattle** (*Bos indicus*) | Kankrej | INDIA_CATTLE_0400_KANKREJ_03005 | Rann of Kutch, Banaskantha, Gujarat |
| **Cattle** (*Bos indicus*) | Ongole | INDIA_CATTLE_0100_ONGOLE_03008 | Prakasam, Guntur, Andhra Pradesh |
| **Cattle** (*Bos indicus*) | Rathi | INDIA_CATTLE_1700_RATHI_03011 | Bikaner, Ganganagar, Rajasthan |
| **Cattle** (*Bos indicus*) | Red Sindhi | INDIA_CATTLE_0000_REDSINDHI_03012 | Sind / Western Border regions |
| **Cattle** (*Bos indicus*) | Sahiwal | INDIA_CATTLE_0000_SAHIWAL_03013 | Montgomery / Punjab & Rajasthan border |
| **Cattle** (*Bos indicus*) | Tharparkar | INDIA_CATTLE_1700_THARPARKAR_03014 | Barmer, Jodhpur, Thar Desert, Rajasthan |
| **Buffalo** (*Bubalus bubalis*) | Banni | INDIA_BUFFALO_0400_BANNI_01011 | Kutch, Gujarat |
| **Buffalo** (*Bubalus bubalis*) | Jaffarabadi | INDIA_BUFFALO_0400_JAFFARABADI_01002 | Gir forest, Saurashtra, Gujarat |
| **Buffalo** (*Bubalus bubalis*) | Mehsana | INDIA_BUFFALO_0400_MEHSANA_01004 | Mehsana, Banaskantha, Gujarat |
| **Buffalo** (*Bubalus bubalis*) | Murrah | INDIA_BUFFALO_0500_MURRAH_01005 | Rohtak, Jind, Hisar, Haryana & Punjab |
| **Buffalo** (*Bubalus bubalis*) | Nili-Ravi | INDIA_BUFFALO_1600_NILIRAVI_01006 | Ferozepur, Punjab |
| **Buffalo** (*Bubalus bubalis*) | Surti | INDIA_BUFFALO_0400_SURTI_01008 | Kaira, Baroda, Gujarat |

---

## 2. Directory Hierarchy

```
data/
├── DATASET_SPECIFICATION.md   # Detailed morphological, taxonomy & inclusion criteria
├── README.md                  # This file: pipeline, scripts, usage instructions
├── raw/                       # Raw downloaded images organized by category and breed
│   ├── cattle/
│   │   ├── gir/ (.gitkeep)
│   │   ├── hariana/ (.gitkeep)
│   │   ├── kankrej/ (.gitkeep)
│   │   ├── ongole/ (.gitkeep)
│   │   ├── rathi/ (.gitkeep)
│   │   ├── red_sindhi/ (.gitkeep)
│   │   ├── sahiwal/ (.gitkeep)
│   │   └── tharparkar/ (.gitkeep)
│   └── buffalo/
│       ├── banni/ (.gitkeep)
│       ├── jaffarabadi/ (.gitkeep)
│       ├── mehsana/ (.gitkeep)
│       ├── murrah/ (.gitkeep)
│       ├── nili_ravi/ (.gitkeep)
│       └── surti/ (.gitkeep)
├── processed/                 # Partitioned dataset outputs (train/val/test)
│   ├── train/
│   ├── val/
│   └── test/
├── scripts/                   # Data processing and maintenance scripts
│   ├── collect_metadata.py    # Extracts image EXIF, dimensions, MD5, and builds CSV
│   ├── dataset_stats.py       # Computes breed counts, dimensions, and balance ratio
│   ├── clean_dataset.py       # MD5 deduplication, corrupted file removal, dimension checks
│   └── split_dataset.py       # Stratified 70/15/15 train/val/test splitting
└── tests/                     # Automated QA test suite
    └── test_dataset_quality.py# Tests for zero data leakage, class completeness, format validity
```

> [!NOTE]
> Large raw binary image sets are excluded from Git tracking via `.gitignore` to maintain repository lightweight integrity. Directory structures and empty partitions are preserved using `.gitkeep`.

---

## 3. Data Processing Scripts

### 3.1 Metadata Cataloging (`data/scripts/collect_metadata.py`)
Scans `data/raw/`, inspects each image header via Pillow, generates unique MD5 checksums, and outputs `data/metadata.csv`.
```bash
python -m data.scripts.collect_metadata --data-dir data/raw --output data/metadata.csv
```
Attributes tracked per image:
- `filename`: Relative file path
- `breed`: Target class name (e.g., `gir`, `murrah`)
- `species`: Category (`cattle` or `buffalo`)
- `file_size_bytes`: Raw byte footprint
- `width`, `height`, `aspect_ratio`: Spatial resolution
- `format`: Encoding format (JPEG, PNG, WEBP)
- `md5_hash`: Cryptographic checksum for duplicate prevention

### 3.2 Dataset Statistics (`data/scripts/dataset_stats.py`)
Analyzes class distribution and balance ratios across the 14 breeds.
```bash
python -m data.scripts.dataset_stats --data-dir data/raw
```

### 3.3 Image Cleaning & Deduplication (`data/scripts/clean_dataset.py`)
Verifies image headers, purges truncated files, eliminates exact byte-level duplicates (MD5 collision check), and filters out thumbnails under 150x150 pixels.
```bash
# Preview cleaning actions safely (dry-run):
python -m data.scripts.clean_dataset --data-dir data/raw --dry-run

# Execute cleaning:
python -m data.scripts.clean_dataset --data-dir data/raw --min-dim 150
```

### 3.4 Stratified Splitting (`data/scripts/split_dataset.py`)
Partitions cleaned images into 70% Train, 15% Validation, and 15% Test splits with balanced per-class stratification and reproducible seeding (seed=42). Emits `data/splits_manifest.json`.
```bash
python -m data.scripts.split_dataset --input-dir data/raw --output-dir data/processed --train-ratio 0.70 --val-ratio 0.15 --test-ratio 0.15 --seed 42
```

---

## 4. Automated Quality Assurance

QA tests are implemented in `data/tests/test_dataset_quality.py` using `pytest`. They guarantee:
1. **Class Completeness:** All 14 target breeds are present in the directory structure.
2. **Zero Data Leakage:** Mathematical verification that `MD5(train) ∩ MD5(val) ∩ MD5(test) = ∅`.
3. **Format Integrity:** Decodability and minimum dimension requirements (`width >= 150`, `height >= 150`).

Run the automated QA test suite:
```bash
python -m pytest data/tests/test_dataset_quality.py -v
```

---

## 5. Compliance & Ethics

- **Open Access & Fair Use:** Data collection complies with educational research standards.
- **Accreditation:** Breed markers, terminology, and reference characteristics adhere to the **National Bureau of Animal Genetic Resources (NBAGR)** guidelines, Karnal, India.
