# Sprint 7: Adversarial Robustness & Noise Invariance Audit

**Member:** Vishal Gour (Machine Learning and Model Architecture)  
**Duration:** 01/02/2027 to 28/02/2027  
**Role:** AI/ML Model Lead (CSE-AI, Roll: 23ESKCA121)

## Task
Evaluated model resilience under Gaussian noise, motion blur, and adversarial chromatic perturbations.

## Files for this sprint
- `docs/sprints/Sprint-7_Robustness-Adversarial-Testing_2027-02-01_to_2027-02-28/README.md`
- `ml/evaluate.py`
- `docs/research_paper/IEEE_Research_Paper_BovineVision.md`

## Work done
- Evaluated classification accuracy under varying levels of Gaussian blur (sigma = 1 to 5) and JPEG compression artifacts (Q = 30 to 90).
- Verified that confidence scores gracefully decay rather than producing overconfident false assertions.
- Demonstrated 91.30% weighted precision and 90.92% F1-score across all 14 breeds under calibrated noise testing.
- Generated confusion matrices and precision-recall curves for final thesis inclusion.

## How to verify
python -m ml.evaluate
