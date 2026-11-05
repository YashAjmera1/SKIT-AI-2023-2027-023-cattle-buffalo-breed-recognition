import os
import json
from PIL import Image
from app.config import MODEL_PATH, CLASS_NAMES_PATH, IMAGE_SIZE

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
    "Jaffrabadi",
    "Mehsana",
    "Surti",
    "Nili-Ravi",
    "Banni",
]


class BreedModelService:
    def __init__(self):
        self.model = None
        self.class_names = DEFAULT_BREEDS
        self.mock = True

        self._load_class_names()
        self._load_model()

    def _load_class_names(self):
        if os.path.exists(CLASS_NAMES_PATH):
            try:
                with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
                    self.class_names = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load class names from {CLASS_NAMES_PATH}: {e}")

    def _load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(MODEL_PATH)
                self.mock = False
                print(f"Loaded trained EfficientNet-B0 model from {MODEL_PATH}")
            except Exception as e:
                print(f"Warning: Model found at {MODEL_PATH} but failed to load: {e}. Running in prototype mode.")
                self.mock = True
        else:
            self.mock = True

    def predict(self, image: Image.Image, raw_bytes: bytes, top_k: int = 3) -> list[dict]:
        if not self.mock and self.model is not None:
            import numpy as np
            resized = image.resize(IMAGE_SIZE)
            img_array = np.array(resized, dtype=np.float32) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            predictions = self.model.predict(img_array)[0]

            top_indices = predictions.argsort()[-top_k:][::-1]
            return [
                {
                    "breed": self.class_names[idx] if idx < len(self.class_names) else f"Breed_{idx}",
                    "confidence": round(float(predictions[idx]), 4),
                }
                for idx in top_indices
            ]

        # Prototype / mock mode simulation
        # Heuristic determination based on dominant image luminance
        # Darker animals (e.g. Buffalo - Murrah/Jaffrabadi) vs lighter animals (Cattle - Gir/Sahiwal)
        gray = image.convert("L").resize((64, 64))
        pixels = list(gray.getdata())
        avg_brightness = sum(pixels) / len(pixels)

        if avg_brightness < 110:  # Darker coat -> typically Buffalo (Murrah/Jaffrabadi)
            candidates = [
                ("Murrah", 0.942),
                ("Jaffrabadi", 0.038),
                ("Mehsana", 0.012),
            ]
        elif avg_brightness < 155:  # Reddish / Dun coat -> Sahiwal / Red Sindhi
            candidates = [
                ("Gir", 0.935),
                ("Sahiwal", 0.045),
                ("Red Sindhi", 0.015),
            ]
        else:  # Light grey / white coat -> Tharparkar / Kankrej / Ongole
            candidates = [
                ("Tharparkar", 0.921),
                ("Kankrej", 0.054),
                ("Hariana", 0.018),
            ]

        return [
            {"breed": breed, "confidence": round(conf, 4)}
            for breed, conf in candidates[:top_k]
        ]


_service_instance: BreedModelService | None = None


def get_model() -> BreedModelService:
    global _service_instance
    if _service_instance is None:
        _service_instance = BreedModelService()
    return _service_instance

