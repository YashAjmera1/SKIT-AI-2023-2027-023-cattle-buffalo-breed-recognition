"""
Dataset Cleaning, Integrity Verification & Duplicate Removal.
Member: Rajnish Kumar Patel (Data & QA Lead)
"""
import os
import hashlib
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")
MIN_RESOLUTION = (150, 150)


def get_file_hash(filepath: str) -> str:
    """Computes MD5 hash of image content to detect exact duplicates."""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()


def clean_dataset(dry_run: bool = False):
    print(f"Starting dataset integrity cleaning on {RAW_DIR} (dry_run={dry_run})...")

    corrupted_count = 0
    duplicate_count = 0
    low_res_count = 0
    valid_count = 0

    seen_hashes = {}
    supported_exts = {".jpg", ".jpeg", ".png", ".webp"}

    for root, _, files in os.walk(RAW_DIR):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in supported_exts:
                continue

            filepath = os.path.join(root, f)

            # Check 1: Corruption check
            try:
                with Image.open(filepath) as img:
                    img.verify()
                # Reopen to check dimensions and color bands
                with Image.open(filepath) as img:
                    w, h = img.size
                    if w < MIN_RESOLUTION[0] or h < MIN_RESOLUTION[1]:
                        print(f"[Low Resolution] {f} ({w}x{h}) < {MIN_RESOLUTION}")
                        low_res_count += 1
                        if not dry_run:
                            os.remove(filepath)
                        continue
            except Exception as e:
                print(f"[Corrupted Image] {f}: {e}")
                corrupted_count += 1
                if not dry_run:
                    os.remove(filepath)
                continue

            # Check 2: Duplicate check via MD5
            file_hash = get_file_hash(filepath)
            if file_hash in seen_hashes:
                print(f"[Duplicate Detected] {f} duplicates {seen_hashes[file_hash]}")
                duplicate_count += 1
                if not dry_run:
                    os.remove(filepath)
                continue
            else:
                seen_hashes[file_hash] = f

            valid_count += 1

    print("-" * 50)
    print("CLEANING AUDIT SUMMARY:")
    print(f"  • Valid & Verified Images: {valid_count}")
    print(f"  • Corrupted Files Removed: {corrupted_count}")
    print(f"  • Duplicate Files Removed: {duplicate_count}")
    print(f"  • Low-Resolution Removed: {low_res_count}")
    print("-" * 50)


if __name__ == "__main__":
    clean_dataset(dry_run=True)

