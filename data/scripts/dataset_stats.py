"""
Dataset Statistics & Class Distribution Analyzer.
Member: Rajnish Kumar Patel (Data & QA Lead)
"""
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")


def compute_statistics():
    print("=" * 60)
    print("INDIAN LIVESTOCK BREED RECOGNITION - DATASET STATISTICS")
    print("=" * 60)

    # 1. Raw Dataset Statistics
    raw_stats = defaultdict(int)
    species_stats = {"cattle": 0, "buffalo": 0}

    for root, _, files in os.walk(RAW_DIR):
        img_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
        if img_files:
            breed = os.path.basename(root)
            raw_stats[breed] += len(img_files)
            if "buffalo" in root.lower():
                species_stats["buffalo"] += len(img_files)
            else:
                species_stats["cattle"] += len(img_files)

    print(f"Total Raw Classes Detected: {len(raw_stats)}")
    print(f"Species Breakdown: Cattle = {species_stats['cattle']} | Buffalo = {species_stats['buffalo']}")
    print("-" * 60)
    print(f"{'Breed':<20} | {'Image Count':<12}")
    print("-" * 60)
    for breed, count in sorted(raw_stats.items()):
        print(f"{breed:<20} | {count:<12}")

    # 2. Processed Splits Statistics (if existing)
    if os.path.exists(PROCESSED_DIR):
        print("\nProcessed Splits Breakdown:")
        for split in ["train", "val", "test"]:
            split_dir = os.path.join(PROCESSED_DIR, split)
            if os.path.exists(split_dir):
                count = sum(len(files) for _, _, files in os.walk(split_dir) if any(f.endswith((".jpg", ".png", ".jpeg")) for f in files))
                print(f"  • {split.capitalize():<10}: {count} images")

    print("=" * 60)


if __name__ == "__main__":
    compute_statistics()

