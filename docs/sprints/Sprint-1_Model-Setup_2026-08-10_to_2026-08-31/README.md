# Sprint 1: Model Setup

**Member:** Vishal Gour (AI/ML Model Development)  
**Duration:** 10/08/2026 to 31/08/2026  
**Role:** Team Lead — Model Architecture & AI/ML Coordination (CSE-AI, Roll: 23ESKCA121)

## Task
Configured TensorFlow, installed required libraries, loaded the EfficientNet-B0 pretrained model and verified the model environment.

## Files for this sprint
- `docs/sprints/Sprint-1_Model-Setup_2026-08-10_to_2026-08-31/README.md`
- `ml/config.py`
- `ml/model.py`

## Work done
- Configured deep learning environment supporting TensorFlow and Keras.
- Defined target taxonomy covering 14 indigenous Indian breeds (8 Cattle + 6 Buffalo).
- Loaded pretrained EfficientNet-B0 convolutional neural network architecture with ImageNet weights.
- Designed custom dense classification head with GlobalAveragePooling2D, BatchNormalization, Dense(256), Dropout(0.3), and 14-way Softmax output.

## How to verify
```bash
python -m ml.model
```

