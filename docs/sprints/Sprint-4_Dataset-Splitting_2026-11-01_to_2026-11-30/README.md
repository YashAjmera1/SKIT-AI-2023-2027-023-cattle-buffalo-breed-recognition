# Sprint 4: Stratified Dataset Splitting & Quality Assurance

**Member:** Rajnish Kumar Patel (Dataset & QA Lead)  
**Duration:** 01/11/2026 to 30/11/2026  
**Role:** Dataset & QA Lead — Data Acquisition & Quality Assurance (CSE-AI, Roll: 23ESKCA087)

## Task
Implement stratified 70/15/15 dataset partitioning into train/validation/test splits, verify zero data leakage, and establish automated dataset quality testing suite.

## Files for this sprint
- `docs/sprints/Sprint-4_Dataset-Splitting_2026-11-01_to_2026-11-30/README.md`
- `data/scripts/split_dataset.py`
- `data/tests/test_dataset_quality.py`
- `data/README.md`

## Work done
- Developed `data/scripts/split_dataset.py` implementing stratified train (70%), validation (15%), and test (15%) partitioning:
  - Generates partitioned outputs under `data/processed/{train,val,test}/{breed}/` via copying or symlinks.
  - Generates `data/splits_manifest.json` recording every image's assigned partition and MD5 hash.
  - Reproducible splitting via configurable random seed (default: 42).
- Authored automated QA test suite in `data/tests/test_dataset_quality.py`:
  - Validates all 14 expected breed classes are present.
  - Enforces zero data leakage (verifies empty intersection of MD5 hashes between train, val, and test partitions).
  - Asserts that all images meet minimum resolution specifications (>= 150px) and valid image headers.
- Authored comprehensive documentation in `data/README.md` explaining pipeline usage, directory hierarchy, and quality standards.

## How to verify
```bash
python -m data.scripts.split_dataset --help
python -m pytest data/tests/test_dataset_quality.py -v
```

