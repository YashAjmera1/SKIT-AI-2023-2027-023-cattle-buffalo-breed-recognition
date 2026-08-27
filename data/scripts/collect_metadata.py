"""
Metadata Collection & Cataloging Script.
Member: Rajnish Kumar Patel (Data & QA Lead)
"""
import os
import csv
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")
METADATA_CSV = os.path.join(BASE_DIR, "metadata.csv")


def collect_metadata(data_dir=RAW_DIR, output_csv=METADATA_CSV):
    print(f"Scanning raw dataset under: {data_dir}")
    records = []
    supported_exts = {".jpg", ".jpeg", ".png", ".webp"}

    for root, _, files in os.walk(data_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in supported_exts:
                file_path = os.path.join(root, f)
                rel_path = os.path.relpath(file_path, BASE_DIR)
                breed_name = os.path.basename(root)
                animal_type = "buffalo" if "buffalo" in root.lower() else "cattle"
                file_size_kb = os.path.getsize(file_path) / 1024

                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        channels = len(img.getbands())
                        color_mode = img.mode
                except Exception:
                    width, height, channels, color_mode = -1, -1, -1, "corrupt"

                records.append({
                    "relative_path": rel_path,
                    "filename": f,
                    "species": animal_type,
                    "breed": breed_name,
                    "width": width,
                    "height": height,
                    "channels": channels,
                    "color_mode": color_mode,
                    "size_kb": round(file_size_kb, 2)
                })

    # Write metadata CSV
    fieldnames = ["relative_path", "filename", "species", "breed", "width", "height", "channels", "color_mode", "size_kb"]
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Collected metadata for {len(records)} images. Saved to {output_csv}")
    return records


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Collect image metadata for dataset catalog.")
    parser.add_argument("--data-dir", default=RAW_DIR, help="Path to raw image directory")
    parser.add_argument("--output", default=METADATA_CSV, help="Output metadata CSV path")
    args = parser.parse_args()
    collect_metadata(data_dir=args.data_dir, output_csv=args.output)
