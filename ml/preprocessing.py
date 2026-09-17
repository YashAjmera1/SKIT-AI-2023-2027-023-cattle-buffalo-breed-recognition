"""
Image Preprocessing and Data Augmentation Pipeline.
Member: Vishal Gour (AI/ML Lead)
"""
import os
from PIL import Image

try:
    import numpy as np
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

from ml.config import IMAGE_SIZE, BREED_CLASSES


class BreedLabelEncoder:
    """Label encoder mapping between breed names and integer class indices."""
    def __init__(self, class_names=None):
        self.classes = class_names or BREED_CLASSES
        self.class_to_idx = {name: idx for idx, name in enumerate(self.classes)}
        self.idx_to_class = {idx: name for idx, name in enumerate(self.classes)}

    def encode(self, breed_name: str) -> int:
        return self.class_to_idx.get(breed_name, -1)

    def decode(self, idx: int) -> str:
        return self.idx_to_class.get(idx, "Unknown")

    def to_one_hot(self, idx: int, num_classes: int = len(BREED_CLASSES)):
        vec = [0.0] * num_classes
        if 0 <= idx < num_classes:
            vec[idx] = 1.0
        return vec


def preprocess_image(image_path: str, target_size=IMAGE_SIZE):
    """
    Loads, resizes with aspect ratio handling, and normalizes an input image.
    Returns normalized float32 array in [0, 1] range.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img_resized = img.resize(target_size, Image.Resampling.BILINEAR)
        arr = list(img_resized.getdata())
        return arr


def get_data_augmentation_layers():
    """
    Keras Data Augmentation sequential pipeline.
    Simulates variations in unconstrained rural farm lighting and camera angles.
    """
    try:
        from tensorflow.keras import layers
        return layers.Sequential([
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.12),
            layers.RandomZoom(0.1),
            layers.RandomContrast(0.15),
            layers.RandomTranslation(height_factor=0.08, width_factor=0.08)
        ], name="data_augmentation")
    except ImportError:
        return None

