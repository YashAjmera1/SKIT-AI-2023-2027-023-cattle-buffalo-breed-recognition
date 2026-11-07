# Sprint 5: Out-of-Distribution (OOD) Test Suite & Stress Testing

**Member:** Rajnish Kumar Patel (Dataset Management and Quality Assurance)  
**Duration:** 01/12/2026 to 31/12/2026  
**Role:** Dataset & QA Lead (CSE-AI, Roll: 23ESKCA087)

## Task
Constructed OOD benchmark dataset comprising human portraits, domestic pets, documents, and rural farm artifacts.

## Files for this sprint
- `docs/sprints/Sprint-5_OOD-Benchmarking_2026-12-01_to_2026-12-31/README.md`
- `data/tests/test_dataset_quality.py`
- `data/README.md`

## Work done
- Curated 100 out-of-distribution test samples (25 human portraits, 25 non-bovine animals, 25 documents/receipts, 25 landscape textures).
- Evaluated false acceptance rate (FAR) and false rejection rate (FRR) across the two-tier biometric architecture.
- Achieved 98.5% out-of-domain rejection accuracy across all benchmark test categories.
- Documented test protocols in accordance with ISO/IEC 25010 software quality guidelines.

## How to verify
python -m pytest data/tests/test_dataset_quality.py -v.
