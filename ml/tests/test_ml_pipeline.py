"""
Unit Tests for AI/ML Pipeline & Taxonomy Specifications.
SKIT Jaipur - 4th Year B.Tech Major Project (SKIT/AI/2023-2027/023)
Author: Vishal Gour (CSE-AI, Roll: 23ESKCA121)
"""
import os
import tempfile
import pytest
from PIL import Image
from ml.config import BREED_CLASSES, NUM_CLASSES, IMAGE_SIZE, INPUT_SHAPE
from ml.preprocessing import BreedLabelEncoder, preprocess_image


def test_taxonomy_completeness():
    """Verify that exactly 14 indigenous breeds are recognized (8 cattle, 6 buffalo)."""
    assert len(BREED_CLASSES) == 14
    assert NUM_CLASSES == 14
    
    # 8 Cattle breeds
    cattle_expected = ["Gir", "Sahiwal", "Red Sindhi", "Tharparkar", "Rathi", "Kankrej", "Hariana", "Ongole"]
    for breed in cattle_expected:
        assert breed in BREED_CLASSES, f"Expected cattle breed {breed} missing from taxonomy."
        
    # 6 Buffalo breeds
    buffalo_expected = ["Murrah", "Jaffrabadi", "Mehsana", "Surti", "Nili-Ravi", "Banni"]
    for breed in buffalo_expected:
        assert breed in BREED_CLASSES, f"Expected buffalo breed {breed} missing from taxonomy."


def test_input_dimension_specifications():
    """Verify input dimensions match EfficientNet-B0 standards."""
    assert IMAGE_SIZE == (224, 224)
    assert INPUT_SHAPE == (224, 224, 3)


def test_breed_label_encoder_bijective_mapping():
    """Verify encoding and decoding consistency for all 14 breeds."""
    encoder = BreedLabelEncoder()
    for idx, breed in enumerate(BREED_CLASSES):
        assert encoder.encode(breed) == idx
        assert encoder.decode(idx) == breed
        
        # Test one-hot encoding
        one_hot = encoder.to_one_hot(idx)
        assert len(one_hot) == 14
        assert one_hot[idx] == 1.0
        assert sum(one_hot) == 1.0

    # Test unknown breed
    assert encoder.encode("NonExistentBreed") == -1
    assert encoder.decode(999) == "Unknown"


def test_preprocess_image_pipeline():
    """Verify image loading and resizing function."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name
        img = Image.new("RGB", (320, 240), color=(180, 100, 50))
        img.save(tmp_path, "JPEG")

    try:
        pixels = preprocess_image(tmp_path, target_size=(224, 224))
        assert len(pixels) == 224 * 224
        assert len(pixels[0]) == 3
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
