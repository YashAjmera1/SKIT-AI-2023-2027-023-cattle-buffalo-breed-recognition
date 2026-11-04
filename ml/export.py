"""
Model Export & Serialization Utility.
Prepares model weights and class mappings for FastAPI backend inference.
Member: Vishal Gour (AI/ML Lead)
"""
import os
import json
import shutil
from ml.config import (
    CHECKPOINT_DIR, EXPORT_MODEL_DIR, MODEL_EXPORT_PATH,
    CLASS_NAMES_EXPORT_PATH, BREED_CLASSES
)


def export_model_and_metadata():
    os.makedirs(EXPORT_MODEL_DIR, exist_ok=True)

    # 1. Export class names mapping
    print(f"Exporting {len(BREED_CLASSES)} breed class names...")
    with open(CLASS_NAMES_EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(BREED_CLASSES, f, indent=2)
    print(f"Exported class names to {CLASS_NAMES_EXPORT_PATH}")

    # 2. Export best model weights if present
    best_checkpoint = os.path.join(CHECKPOINT_DIR, "best_model.keras")
    if os.path.exists(best_checkpoint):
        shutil.copy2(best_checkpoint, MODEL_EXPORT_PATH)
        print(f"Successfully copied best checkpoint to {MODEL_EXPORT_PATH}")
    else:
        print(f"No checkpoint found at {best_checkpoint}. Backend will operate in validated prototype mode.")


if __name__ == "__main__":
    export_model_and_metadata()

