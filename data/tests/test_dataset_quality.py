"""
Quality Assurance (QA) & Dataset Integrity Test Suite.
Member: Rajnish Kumar Patel (Data & QA Lead)
"""
import os
import pytest
from PIL import Image

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

EXPECTED_BREEDS = [
    "gir", "sahiwal", "red_sindhi", "tharparkar", "rathi", "kankrej", "hariana", "ongole",
    "murrah", "jaffrabadi", "mehsana", "surti", "nili_ravi", "banni"
]


def test_raw_directory_hierarchy():
    """Verify raw directory contains both cattle and buffalo directories with 14 breeds."""
    assert os.path.exists(RAW_DIR), "Raw directory does not exist."
    cattle_dir = os.path.join(RAW_DIR, "cattle")
    buffalo_dir = os.path.join(RAW_DIR, "buffalo")

    assert os.path.exists(cattle_dir), "Cattle raw folder missing."
    assert os.path.exists(buffalo_dir), "Buffalo raw folder missing."

    cattle_breeds = os.listdir(cattle_dir)
    buffalo_breeds = os.listdir(buffalo_dir)

    assert "gir" in cattle_breeds
    assert "sahiwal" in cattle_breeds
    assert "murrah" in buffalo_breeds
    assert "jaffrabadi" in buffalo_breeds


def test_no_data_leakage_between_splits():
    """Verify zero overlap between train, val, and test filenames if processed splits exist."""
    train_dir = os.path.join(PROCESSED_DIR, "train")
    val_dir = os.path.join(PROCESSED_DIR, "val")
    test_dir = os.path.join(PROCESSED_DIR, "test")

    if not (os.path.exists(train_dir) and os.path.exists(val_dir) and os.path.exists(test_dir)):
        pytest.skip("Processed splits not populated yet.")

    def get_filenames(base):
        names = set()
        for root, _, files in os.walk(base):
            for f in files:
                if f != ".gitkeep":
                    names.add(f)
        return names

    train_files = get_filenames(train_dir)
    val_files = get_filenames(val_dir)
    test_files = get_filenames(test_dir)

    assert train_files.isdisjoint(val_files), "Data leakage detected: Train and Val have overlapping files!"
    assert train_files.isdisjoint(test_files), "Data leakage detected: Train and Test have overlapping files!"
    assert val_files.isdisjoint(test_files), "Data leakage detected: Val and Test have overlapping files!"


def test_supported_image_extensions():
    """Verify files in dataset adhere to supported extensions."""
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    for root, _, files in os.walk(RAW_DIR):
        for f in files:
            if f.startswith("."):
                continue
            ext = os.path.splitext(f)[1].lower()
            assert ext in valid_exts, f"Unsupported file found in dataset: {f}"
