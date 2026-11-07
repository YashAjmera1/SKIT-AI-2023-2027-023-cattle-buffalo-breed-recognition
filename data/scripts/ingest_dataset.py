"""
Universal Dataset Ingestion Pipeline for Indian Cattle & Buffalo Breeds.
Supports:
- Kaggle Dataset (birendranathnandi/indian-cattle-and-buffalo-breeds-dataset)
- Roboflow Universe (adiworkspace-jfchj/indian-cattle-and-buffaloes-breeds-ucsvl)
- Roboflow Universe (rakshith-r/cattle-mg7du)
- Any custom folder or .zip file containing bovine images

Lead: Rajnish Kumar Patel (Dataset & QA Lead)
"""

import argparse
import hashlib
import os
import re
import shutil
import zipfile
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")

# Canonical 14 Breeds Mapping
BREED_TAXONOMY = {
    # Cattle (8)
    "gir": ("cattle", "gir"),
    "gyr": ("cattle", "gir"),
    "sahiwal": ("cattle", "sahiwal"),
    "red_sindhi": ("cattle", "red_sindhi"),
    "redsindhi": ("cattle", "red_sindhi"),
    "sindhi": ("cattle", "red_sindhi"),
    "tharparkar": ("cattle", "tharparkar"),
    "thari": ("cattle", "tharparkar"),
    "rathi": ("cattle", "rathi"),
    "kankrej": ("cattle", "kankrej"),
    "kankarej": ("cattle", "kankrej"),
    "hariana": ("cattle", "hariana"),
    "haryana": ("cattle", "hariana"),
    "ongole": ("cattle", "ongole"),
    # Buffalo (6)
    "murrah": ("buffalo", "murrah"),
    "jaffarabadi": ("buffalo", "jaffarabadi"),
    "jafrabadi": ("buffalo", "jaffarabadi"),
    "mehsana": ("buffalo", "mehsana"),
    "surti": ("buffalo", "surti"),
    "nili_ravi": ("buffalo", "nili_ravi"),
    "niliravi": ("buffalo", "nili_ravi"),
    "nili": ("buffalo", "nili_ravi"),
    "banni": ("buffalo", "banni"),
    "kundi": ("buffalo", "banni"),
}


def normalize_folder_name(name: str) -> str:
    cleaned = re.sub(r"[_\-\s]+", "_", name.lower().strip())
    # Remove common prefixes/suffixes
    for token in ["cattle", "cow", "bull", "buffalo", "buffaloes", "dataset", "images"]:
        cleaned = re.sub(rf"(?:^|_{token}_|_{token}$|^{token}_)", "", cleaned)
    return cleaned.strip("_")


def map_to_canonical_breed(folder_name: str) -> tuple[str, str] | None:
    norm = normalize_folder_name(folder_name)
    if norm in BREED_TAXONOMY:
        return BREED_TAXONOMY[norm]

    # Partial substring search
    for key, val in BREED_TAXONOMY.items():
        if key in norm:
            return val
    return None


def calculate_md5(file_path: str) -> str:
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def ingest_from_path(source_path: str, min_dim: int = 150):
    print("=" * 65)
    print("UNIVERSAL DATASET INGESTION & NORMALIZATION PIPELINE")
    print(f"Source: {source_path}")
    print("=" * 65)

    temp_extract_dir = None

    if os.path.isfile(source_path) and zipfile.is_zipfile(source_path):
        temp_extract_dir = os.path.join(BASE_DIR, "_temp_zip_extract")
        os.makedirs(temp_extract_dir, exist_ok=True)
        print(f"Extracting zip archive into temporary workspace: {temp_extract_dir} ...")
        with zipfile.ZipFile(source_path, "r") as zf:
            zf.extractall(temp_extract_dir)
        scan_dir = temp_extract_dir
    elif os.path.isdir(source_path):
        scan_dir = source_path
    else:
        raise ValueError(f"Source path '{source_path}' is neither a directory nor a valid zip file.")

    supported_exts = {".jpg", ".jpeg", ".png", ".webp"}
    existing_hashes = set()

    # Pre-index existing images to avoid re-importing duplicates
    for root, _, files in os.walk(RAW_DIR):
        for f in files:
            if os.path.splitext(f)[1].lower() in supported_exts:
                fp = os.path.join(root, f)
                existing_hashes.add(calculate_md5(fp))

    print(f"Pre-indexed {len(existing_hashes)} existing unique image hashes in data/raw.")

    ingested_counts = {breed: 0 for _, breed in set(BREED_TAXONOMY.values())}
    skipped_duplicates = 0
    skipped_corrupted = 0
    skipped_low_res = 0

    # Scan directories
    for root, _, files in os.walk(scan_dir):
        if not files:
            continue

        folder_name = os.path.basename(root)
        canonical = map_to_canonical_breed(folder_name)
        if not canonical:
            # Check parent folder name
            parent_name = os.path.basename(os.path.dirname(root))
            canonical = map_to_canonical_breed(parent_name)

        if not canonical:
            continue

        species, breed = canonical
        dest_dir = os.path.join(RAW_DIR, species, breed)
        os.makedirs(dest_dir, exist_ok=True)

        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in supported_exts:
                continue

            src_fp = os.path.join(root, f)

            # Integrity check
            try:
                with Image.open(src_fp) as img:
                    img.verify()
                with Image.open(src_fp) as img:
                    w, h = img.size
                    if w < min_dim or h < min_dim:
                        skipped_low_res += 1
                        continue
            except Exception:
                skipped_corrupted += 1
                continue

            # Duplicate check
            file_md5 = calculate_md5(src_fp)
            if file_md5 in existing_hashes:
                skipped_duplicates += 1
                continue

            # Ingest image
            target_filename = f"{breed}_{file_md5[:10]}{ext}"
            dst_fp = os.path.join(dest_dir, target_filename)
            shutil.copy2(src_fp, dst_fp)
            existing_hashes.add(file_md5)
            ingested_counts[breed] += 1

    # Cleanup temp directory if created
    if temp_extract_dir and os.path.exists(temp_extract_dir):
        shutil.rmtree(temp_extract_dir, ignore_errors=True)

    print("\n" + "-" * 65)
    print("INGESTION AUDIT SUMMARY:")
    for breed, count in sorted(ingested_counts.items()):
        if count > 0:
            print(f"  • {breed:<15} : +{count} new images added")
    print(f"Total new images ingested   : {sum(ingested_counts.values())}")
    print(f"Duplicates eliminated (MD5) : {skipped_duplicates}")
    print(f"Corrupted images rejected   : {skipped_corrupted}")
    print(f"Low-resolution rejected     : {skipped_low_res}")
    print("-" * 65)

    # Automatically trigger split if new images were ingested
    total_new = sum(ingested_counts.values())
    if total_new > 0:
        print("\nUpdating stratified 70/15/15 train/val/test splits...")
        from data.scripts.split_dataset import split_dataset
        split_dataset(input_dir=RAW_DIR, output_dir=PROCESSED_DIR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest Kaggle/Roboflow Indian Livestock dataset into project.")
    parser.add_argument("--source", required=True, help="Path to extracted folder or .zip file of the dataset")
    parser.add_argument("--min-dim", type=int, default=150, help="Minimum image dimension (default: 150px)")
    args = parser.parse_args()

    ingest_from_path(args.source, min_dim=args.min_dim)

