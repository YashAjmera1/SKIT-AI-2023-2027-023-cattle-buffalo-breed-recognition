"""
Stratified Dataset Splitting Script (70% Train, 15% Val, 15% Test).
Member: Rajnish Kumar Patel (Data & QA Lead)
"""
import argparse
import os
import random
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RAW_DIR = os.path.join(BASE_DIR, "raw")
DEFAULT_PROCESSED_DIR = os.path.join(BASE_DIR, "processed")


def split_dataset(input_dir=DEFAULT_RAW_DIR, output_dir=DEFAULT_PROCESSED_DIR,
                  train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, seed=42):
    random.seed(seed)
    print(f"Executing stratified dataset split from {input_dir} into {output_dir}...")

    # Ensure target directory structures exist
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(output_dir, split), exist_ok=True)

    supported_exts = {".jpg", ".jpeg", ".png", ".webp"}
    total_split = {"train": 0, "val": 0, "test": 0}

    for root, _, files in os.walk(input_dir):
        img_files = [f for f in files if os.path.splitext(f)[1].lower() in supported_exts]
        if not img_files:
            continue

        breed = os.path.basename(root)
        random.shuffle(img_files)

        n_total = len(img_files)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)

        splits = {
            "train": img_files[:n_train],
            "val": img_files[n_train:n_train + n_val],
            "test": img_files[n_train + n_val:]
        }

        for split_name, split_files in splits.items():
            dest_dir = os.path.join(output_dir, split_name, breed)
            os.makedirs(dest_dir, exist_ok=True)
            for f in split_files:
                src = os.path.join(root, f)
                dst = os.path.join(dest_dir, f)
                shutil.copy2(src, dst)
            total_split[split_name] += len(split_files)

        print(f"[{breed:<16}] Total: {n_total:<3} -> Train: {len(splits['train'])}, Val: {len(splits['val'])}, Test: {len(splits['test'])}")

    print("-" * 60)
    print(f"SPLIT COMPLETE: Train={total_split['train']}, Val={total_split['val']}, Test={total_split['test']}")
    print("-" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stratified dataset splitter for cattle and buffalo breeds.")
    parser.add_argument("--input-dir", default=DEFAULT_RAW_DIR, help="Path to raw image directory")
    parser.add_argument("--output-dir", default=DEFAULT_PROCESSED_DIR, help="Path to processed split directory")
    parser.add_argument("--train-ratio", type=float, default=0.70, help="Train split ratio (default: 0.70)")
    parser.add_argument("--val-ratio", type=float, default=0.15, help="Validation split ratio (default: 0.15)")
    parser.add_argument("--test-ratio", type=float, default=0.15, help="Test split ratio (default: 0.15)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    split_dataset(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        seed=args.seed
    )
