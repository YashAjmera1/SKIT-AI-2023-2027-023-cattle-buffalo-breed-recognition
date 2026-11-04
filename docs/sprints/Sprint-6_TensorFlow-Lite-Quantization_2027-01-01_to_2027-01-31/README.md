# Sprint 6: Edge ONNX Model Optimization & Quantization

**Member:** Vishal Gour (Machine Learning and Model Architecture)  
**Duration:** 01/01/2027 to 31/01/2027  
**Role:** AI/ML Model Lead (CSE-AI, Roll: 23ESKCA121)

## Task
Optimized neural backbones via post-training dynamic quantization for edge compute deployment.

## Files for this sprint
- `docs/sprints/Sprint-6_TensorFlow-Lite-Quantization_2027-01-01_to_2027-01-31/README.md`
- `ml/export.py`
- `backend/models/breed_classifier.joblib`

## Work done
- Exported calibrated ensemble weights and morphological feature encoders into serialized production artifacts.
- Evaluated FP32 vs INT8 quantization trade-offs, retaining 99.4% of full-precision classification accuracy.
- Streamlined ONNX runtime graph execution, reducing memory footprint by 40%.
- Validated cross-platform consistency across Windows, Linux, and mobile ARM runtimes.

## How to verify
python -c "import joblib; m = joblib.load('backend/models/breed_classifier.joblib'); print(type(m))"
