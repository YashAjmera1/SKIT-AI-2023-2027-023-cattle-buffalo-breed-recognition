# Sprint 1: Data Collection & Breed Taxonomy Cataloging

**Member:** Rajnish Kumar Patel (Dataset & QA Lead)  
**Duration:** 10/08/2026 to 31/08/2026  
**Role:** Dataset & QA Lead — Data Acquisition & Quality Assurance (CSE-AI, Roll: 23ESKCA087)

## Task
Establish raw image collection structure for 14 indigenous Indian cattle and buffalo breeds, catalog metadata attributes, and implement automated metadata collection script.

## Files for this sprint
- `docs/sprints/Sprint-1_Data-Collection_2026-08-10_to_2026-08-31/README.md`
- `data/raw/cattle/` (8 breed directories with `.gitkeep`)
- `data/raw/buffalo/` (6 breed directories with `.gitkeep`)
- `data/scripts/collect_metadata.py`

## Work done
- Created organized raw directory structure supporting 14 ICAR-NBAGR recognized breeds:
  - **Cattle (8):** Gir, Hariana, Kankrej, Ongole, Rathi, Red Sindhi, Sahiwal, Tharparkar.
  - **Buffalo (6):** Banni, Jaffarabadi, Mehsana, Murrah, Nili-Ravi, Surti.
- Defined standard metadata attributes in `data/metadata.csv` (filename, breed, species, file size, width, height, aspect ratio, channels, format, MD5 hash).
- Developed `data/scripts/collect_metadata.py` to scan raw directory trees, extract EXIF/image headers via Pillow, calculate MD5 checksums, and export structured CSV records.
- Configured `.gitkeep` markers across all breed directories ensuring Git tracks empty partition directories without committing large raw binary datasets.

## How to verify
```bash
python -m data.scripts.collect_metadata --help
python -m data.scripts.collect_metadata
```

