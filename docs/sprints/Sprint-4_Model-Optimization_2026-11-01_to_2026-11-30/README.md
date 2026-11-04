# Sprint 4: Model Optimization & Evaluation

**Member:** Vishal Gour (AI/ML Model Development)  
**Duration:** 01/11/2026 to 30/11/2026  
**Role:** Team Lead — Model Architecture & AI/ML Coordination (CSE-AI, Roll: 23ESKCA121)

## Task
To adjust learning rate and training parameters, compare validation results and analyze incorrectly classified images.

## Files for this sprint
- `docs/sprints/Sprint-4_Model-Optimization_2026-11-01_to_2026-11-30/README.md`
- `ml/evaluate.py`
- `ml/export.py`
- `ml/README.md`

## Work done
- Evaluated classification performance using precision, recall, weighted F1-score, and confusion matrix.
- Analyzed common misclassification patterns (e.g. Sahiwal vs Red Sindhi coat similarities, Murrah vs Mehsana horn variations).
- Implemented `export.py` to serialize class names (`backend/models/class_names.json`) and package trained model weights for seamless FastAPI integration.
- Documented model architecture, hyperparameter selections, and deployment instructions in `ml/README.md`.

## How to verify
```bash
python -m ml.evaluate
python -m ml.export
```

