# Sprint 2: Dataset Organization & Specification

**Member:** Rajnish Kumar Patel (Dataset & QA Lead)  
**Duration:** 01/09/2026 to 30/09/2026  
**Role:** Dataset & QA Lead — Data Acquisition & Quality Assurance (CSE-AI, Roll: 23ESKCA087)

## Task
Formalize dataset specifications, define inclusion/exclusion criteria, physical breed markers, ethical acquisition guidelines, and implement dataset statistics and class balance analyzer.

## Files for this sprint
- `docs/sprints/Sprint-2_Dataset-Organization_2026-09-01_to_2026-09-30/README.md`
- `data/DATASET_SPECIFICATION.md`
- `data/scripts/dataset_stats.py`

## Work done
- Authored comprehensive `data/DATASET_SPECIFICATION.md` detailing:
  - Scientific taxonomy (Bos indicus / Bubalus bubalis) and ICAR-NBAGR accession reference standards.
  - Distinct physical characteristics, horn curvatures, coat pigmentation, and ear morphology per breed.
  - Strict inclusion and exclusion criteria (minimum resolution 150px, single animal dominant, natural ambient light, exclusion of heavy occlusions, watermarks, and extreme blurs).
  - Ethical guidelines, open-access citation norms, and data governance.
- Developed `data/scripts/dataset_stats.py` to analyze class distribution, compute mean dimensions, calculate imbalance ratios across classes, and format terminal tables.

## How to verify
```bash
python -m data.scripts.dataset_stats --help
python -m data.scripts.dataset_stats
```

