import os
import json
import numpy as np
from PIL import Image
from app.config import MODEL_PATH, CLASS_NAMES_PATH, IMAGE_SIZE
from app.services.vision_engine import (
    classify_livestock_image,
    verify_bovine_presence,
    extract_morphological_vector,
    BREED_MORPHOLOGY_PROFILES
)

DEFAULT_BREEDS = [
    "Gir",
    "Sahiwal",
    "Red Sindhi",
    "Tharparkar",
    "Rathi",
    "Kankrej",
    "Hariana",
    "Ongole",
    "Murrah",
    "Jaffarabadi",
    "Mehsana",
    "Surti",
    "Nili-Ravi",
    "Banni",
]


class BreedModelService:
    def __init__(self):
        self.model = None
        self.class_names = DEFAULT_BREEDS
        self.mock = False
        self.mode = "morphological_cv_engine"

        self._load_class_names()
        self._load_model()

    def _resolve_path(self, path: str) -> str:
        if os.path.exists(path):
            return path
        # Try relative to backend dir
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        rel = os.path.join(backend_dir, path)
        if os.path.exists(rel):
            return rel
        return path

    def _load_class_names(self):
        resolved = self._resolve_path(CLASS_NAMES_PATH)
        if os.path.exists(resolved):
            try:
                with open(resolved, "r", encoding="utf-8") as f:
                    self.class_names = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load class names from {resolved}: {e}")

    def _load_model(self):
        resolved_keras = self._resolve_path(MODEL_PATH)
        if os.path.exists(resolved_keras):
            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(resolved_keras)
                self.mode = "efficientnet_deep_learning"
                print(f"Loaded trained EfficientNet-B0 model from {resolved_keras}")
                return
            except Exception as e:
                print(f"Warning: Neural network at {resolved_keras} failed to load: {e}")

        # Check for trained feature classifier (joblib)
        model_dir = os.path.dirname(resolved_keras)
        joblib_path = os.path.join(model_dir, "breed_classifier.joblib")
        if os.path.exists(joblib_path):
            try:
                import joblib
                self.model = joblib.load(joblib_path)
                self.mode = "trained_feature_classifier"
                print(f"Loaded trained feature classifier from {joblib_path}")
            except Exception as e:
                print(f"Warning: Could not load joblib model: {e}")

    def predict_details(self, image: Image.Image, raw_bytes: bytes, top_k: int = 3) -> dict:
        """
        Runs complete professional inference:
        1. Bovine Domain Gatekeeper
        2. Real Forward Inference (via trained ML weights or CV Engine)
        3. Explainable AI (XAI) morphological reasoning & agronomics
        """
        img_rgb = np.array(image.convert("RGB"))

        # Step 1: Bovine Domain Gatekeeper
        is_bovine, bovine_conf, gate_reason = verify_bovine_presence(img_rgb)
        if not is_bovine:
            return {
                "verified_bovine": False,
                "bovine_confidence": bovine_conf,
                "message": gate_reason,
                "predictions": [
                    {
                        "breed": "Uncertain / Non-Bovine",
                        "confidence": round(1.0 - bovine_conf, 4),
                        "species": "unknown",
                        "reasoning": gate_reason
                    }
                ],
                "top_breed": None
            }

        # Step 2: Inference via Trained Feature Classifier (joblib)
        if self.mode == "trained_feature_classifier" and self.model is not None and hasattr(self.model, "predict_proba"):
            try:
                feat_vec = extract_morphological_vector(img_rgb).reshape(1, -1)
                raw_probs = self.model.predict_proba(feat_vec)[0]

                # Temperature scaling and smoothing to avoid artificial 100% / 0% spikes
                smoothed = np.power(raw_probs + 0.05, 0.75)
                smoothed /= smoothed.sum()

                top_indices = smoothed.argsort()[-top_k:][::-1]
                predictions = []
                for idx in top_indices:
                    breed_name = self.class_names[idx] if idx < len(self.class_names) else f"Breed_{idx}"
                    prof = BREED_MORPHOLOGY_PROFILES.get(breed_name, {})
                    predictions.append({
                        "breed": breed_name,
                        "confidence": round(float(smoothed[idx]), 4),
                        "species": prof.get("species", "bovine"),
                        "native_region": prof.get("native", "India"),
                        "milk_yield": prof.get("milk_yield", "1,800 - 3,200 kg / lactation"),
                        "morphological_features": f"{prof.get('horns', '')}; {prof.get('head', '')}",
                        "reasoning": f"{prof.get('head', '')}. {prof.get('horns', '')}."
                    })

                return {
                    "verified_bovine": True,
                    "bovine_confidence": bovine_conf,
                    "message": "Animal morphology authenticated as Indian Bovine.",
                    "predictions": predictions,
                    "top_breed": predictions[0]["breed"]
                }
            except Exception as e:
                print(f"Joblib inference error: {e}. Falling back to CV Vision Engine.")

        # Step 3: Inference via Computer Vision & Morphological Feature Engine
        return classify_livestock_image(image, top_k=top_k)

    def predict(self, image: Image.Image, raw_bytes: bytes, top_k: int = 3) -> list[dict]:
        """
        Compatibility method returning list of top predictions.
        """
        details = self.predict_details(image, raw_bytes, top_k=top_k)
        return details["predictions"]


_service_instance: BreedModelService | None = None


def get_model() -> BreedModelService:
    global _service_instance
    if _service_instance is None:
        _service_instance = BreedModelService()
    return _service_instance
