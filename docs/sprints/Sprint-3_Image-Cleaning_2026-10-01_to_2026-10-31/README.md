# Sprint 3: Image Cleaning & Integrity Verification

**Member:** Rajnish Kumar Patel (Dataset & QA Lead)  
**Duration:** 01/10/2026 to 31/10/2026  
**Role:** Dataset & QA Lead — Data Acquisition & Quality Assurance (CSE-AI, Roll: 23ESKCA087)

## Task
Develop automated image cleaning, integrity verification, and deduplication pipeline to eliminate corrupted files, duplicate images, and substandard resolutions.

## Files for this sprint
- `docs/sprints/Sprint-3_Image-Cleaning_2026-10-01_to_2026-10-31/README.md`
- `data/scripts/clean_dataset.py`

## Work done
- Built `data/scripts/clean_dataset.py` with multi-stage verification:
  - **Integrity Validation:** Uses Pillow `Image.verify()` and full decode `Image.load()` to catch truncated, unreadable, or malformed JPEG/PNG files.
  - **MD5 Deduplication:** Computes 128-bit MD5 hashes of raw image bytes to identify and purge exact duplicates across and within breed directories.
  - **Dimension Filtering:** Enforces strict minimum bounding constraints (default: 150x150 pixels) to reject low-resolution thumbnails.
  - **Color Mode Normalization:** Detects CMYK or grayscale images and flags/converts them for standard RGB color space compatibility.
  - **Dry-run Mode:** Supports `--dry-run` flag to preview deletions and logs actions safely before filesystem execution.

## How to verify
```bash
python -m data.scripts.clean_dataset --help
python -m data.scripts.clean_dataset --dry-run
```

