# Sprint 6: Field Dataset Expansion & Environmental Stress Testing

**Member:** Rajnish Kumar Patel (Dataset Management and Quality Assurance)  
**Duration:** 01/01/2027 to 31/01/2027  
**Role:** Dataset & QA Lead (CSE-AI, Roll: 23ESKCA087)

## Task
Expanded rural field dataset with harsh lighting, dust, occlusions, and varied camera angles.

## Files for this sprint
- `docs/sprints/Sprint-6_Field-Validation-Dataset_2027-01-01_to_2027-01-31/README.md`
- `data/scripts/clean_dataset.py`
- `data/DATASET_SPECIFICATION.md`

## Work done
- Integrated 500 augmented field images reflecting unconstrained rural gaushala and pastoral farm conditions.
- Verified label consistency against ICAR-NBAGR breed registration dossiers.
- Conducted automated duplicate image detection via MD5 and perceptual hashing.
- Validated class balance across all 14 target breeds (8 cattle, 6 buffalo).

## How to verify
python -m pytest data/tests/test_dataset_quality.py -v.
