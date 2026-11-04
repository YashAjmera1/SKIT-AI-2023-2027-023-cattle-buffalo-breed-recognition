# Sprint 5: Multi-Modal Feature Extraction & Temperature Calibration

**Member:** Vishal Gour (Machine Learning and Model Architecture)  
**Duration:** 01/12/2026 to 31/12/2026  
**Role:** AI/ML Model Lead (CSE-AI, Roll: 23ESKCA121)

## Task
Formulated 198-dimensional morphological feature tensor and temperature-scaled Softmax ensemble.

## Files for this sprint
- `docs/sprints/Sprint-5_GradCAM-Explainability_2026-12-01_to_2026-12-31/README.md`
- `backend/app/services/vision_engine.py`
- `ml/model.py`
- `ml/evaluate.py`

## Work done
- Formulated multi-modal feature vector combining 3D HSV color histograms (128-d), 3x3 spatial grid moments (54-d), and Sobel edge orientations (16-d).
- Implemented temperature scaling (T = 0.18) on Softmax logits to ensure organic, dynamic confidence distributions.
- Mapped top morphological discriminators (dewlap curvature, horn angles, forehead convexities) for all 14 breeds.
- Benchmarked feature stability under variable rustic sunlight and shadows.

## How to verify
python -m pytest ml/tests -v and python -m ml.evaluate.
