# Sprint 5: Dual-Tier Domain Gatekeeper & Inference Engine

**Member:** Kunal Rana (Backend Development and System Integration)  
**Duration:** 01/12/2026 to 31/12/2026  
**Role:** Backend & Database Lead (CSE-AI, Roll: 23ESKCA300)

## Task
Engineered high-throughput OpenCV YuNet deep facial landmark suppression and YOLOv8 nano object gatekeeper.

## Files for this sprint
- `docs/sprints/Sprint-5_Inference-Optimization_2026-12-01_to_2026-12-31/README.md`
- `backend/app/services/vision_engine.py`
- `backend/app/routers/predict.py`
- `backend/app/schemas.py`

## Work done
- Integrated OpenCV YuNet face detection model (face_detection_yunet.onnx) to eliminate human portrait misclassifications.
- Embedded YOLOv8 nano ONNX object detector to classify cow/buffalo vs non-bovine animals and inanimate objects.
- Added biological hide chromaticity filters and Laplacian sharpness verification to reject documents, screenshots, and textures.
- Achieved sub-120ms total inference latency on CPU using OpenCV DNN module.

## How to verify
python -m pytest backend/tests -v and curl -X POST /api/v1/predict with test images.
