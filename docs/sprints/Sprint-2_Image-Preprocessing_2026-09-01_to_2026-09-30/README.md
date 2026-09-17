# Sprint 2: Image Preprocessing

**Member:** Vishal Gour (AI/ML Model Development)  
**Duration:** 01/09/2026 to 30/09/2026  
**Role:** Team Lead — Model Architecture & AI/ML Coordination (CSE-AI, Roll: 23ESKCA121)

## Task
To implement image resizing, normalization, label encoding and data augmentation for cattle and buffalo breed images.

## Files for this sprint
- `docs/sprints/Sprint-2_Image-Preprocessing_2026-09-01_to_2026-09-30/README.md`
- `ml/preprocessing.py`
- `ml/dataset.py`

## Work done
- Implemented `BreedLabelEncoder` mapping between string labels and integer/one-hot tensors.
- Implemented `preprocess_image` function ensuring consistent 224x224 RGB input representation.
- Built data augmentation pipeline including random horizontal flipping, rotation (±12°), zoom, contrast adjustment, and subtle translation to simulate varied rural lighting conditions.
- Constructed `tf.data.Dataset` batch loading pipeline with caching, shuffling, and autotuned prefetching.

## How to verify
```bash
python -m ml.preprocessing
```

