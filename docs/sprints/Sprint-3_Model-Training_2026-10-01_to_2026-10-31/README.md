# Sprint 3: Model Training

**Member:** Vishal Gour (AI/ML Model Development)  
**Duration:** 01/10/2026 to 31/10/2026  
**Role:** Team Lead — Model Architecture & AI/ML Coordination (CSE-AI, Roll: 23ESKCA121)

## Task
To train the classification model, configure epochs and batch size, monitor training loss and save model checkpoints.

## Files for this sprint
- `docs/sprints/Sprint-3_Model-Training_2026-10-01_to_2026-10-31/README.md`
- `ml/train.py`

## Work done
- Configured two-stage transfer learning training routine:
  - **Phase 1 (20 epochs):** Frozen backbone, training only classification head using Adam optimizer (LR=1e-3).
  - **Phase 2 (15 epochs):** Fine-tuning top 30 convolutional layers at reduced learning rate (LR=1e-5).
- Integrated `ModelCheckpoint` to persist best validation accuracy weights.
- Implemented `EarlyStopping` (patience=5) and `ReduceLROnPlateau` (factor=0.2) to prevent overfitting.
- Configured `CSVLogger` to log training and validation loss and accuracy curves per epoch.

## How to verify
```bash
python -m ml.train
```

