# AI/ML Model Pipeline · BreedWise

**Member:** Vishal Gour (Team Lead — AI/ML Architecture & Model Development)  
**Session:** 2026-27  
**Department:** Computer Science & Engineering (AI), SKIT Jaipur  
**Project ID:** SKIT/AI/2023-2027/023

---

## 1. Overview
The machine learning subsystem implements a lightweight transfer learning architecture based on **EfficientNet-B0** to classify **14 indigenous Indian cattle and buffalo breeds** in unconstrained agricultural farm environments.

## 2. Target Breeds Taxonomy
- **Indigenous Cattle (8 Breeds):** Gir, Sahiwal, Red Sindhi, Tharparkar, Rathi, Kankrej, Hariana, Ongole.
- **Indigenous Buffalo (6 Breeds):** Murrah, Jaffrabadi, Mehsana, Surti, Nili-Ravi, Banni.

## 3. Architecture Specification
- **Base Backbone:** EfficientNet-B0 (Pre-trained on ImageNet).
- **Input Resolution:** `224 × 224 × 3`.
- **Feature Pooling:** GlobalAveragePooling2D + BatchNormalization.
- **Projection Layer:** Dense(256, activation='relu', kernel_regularizer=L2(1e-4)).
- **Regularization:** Dropout (0.3).
- **Classification Output:** Dense(14, activation='softmax').

## 4. Sprints Completed (Team Lead — Vishal Gour)
- **Sprint 1 (10/08/2026 - 31/08/2026):** TensorFlow/Keras environment configuration, EfficientNet-B0 backbone instantiation (`ml/config.py`, `ml/model.py`).
- **Sprint 2 (01/09/2026 - 30/09/2026):** Image preprocessing, normalization, aspect ratio handling, label encoding, and data augmentation pipeline (`ml/preprocessing.py`, `ml/dataset.py`).
- **Sprint 3 (01/10/2026 - 31/10/2026):** Two-phase training loop (Head training + Top-layer fine-tuning), ModelCheckpoint, and LR scheduler (`ml/train.py`).
- **Sprint 4 (01/11/2026 - 30/11/2026):** Model evaluation metrics (Precision, Recall, F1, Confusion Matrix) and model serialization (`ml/evaluate.py`, `ml/export.py`).

## 5. Usage Commands

```bash
# Verify model architecture
python -m ml.model

# Run model evaluation metrics
python -m ml.evaluate

# Export model & class names to backend
python -m ml.export
```

