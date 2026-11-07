# Sprint 7: Data Integrity Verification & SHA-256 Checksums

**Member:** Rajnish Kumar Patel (Dataset Management and Quality Assurance)  
**Duration:** 01/02/2027 to 28/02/2027  
**Role:** Dataset & QA Lead (CSE-AI, Roll: 23ESKCA087)

## Task
Implemented SHA-256 integrity manifests and automated dataset validation test suites.

## Files for this sprint
- `docs/sprints/Sprint-7_Data-Integrity-Checksums_2027-02-01_to_2027-02-28/README.md`
- `data/scripts/ingest_dataset.py`
- `data/tests/test_dataset_quality.py`

## Work done
- Generated SHA-256 cryptographic checksum manifests for all processed image datasets and metadata records.
- Created automated pytest verification test suites checking file integrity, image readability, and split isolation.
- Verified zero data leakage between train, validation, and test splits.
- Archived dataset provenance and ingestion scripts in reproducible Python automation.

## How to verify
python -m pytest data/tests/test_dataset_quality.py -v
