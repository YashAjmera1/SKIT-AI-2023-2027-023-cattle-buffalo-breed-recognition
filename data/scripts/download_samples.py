"""
Automated reference image downloader from Wikimedia Commons for Indian cattle and buffalo breeds.
Lead: Rajnish Kumar Patel (Dataset & QA Lead)
"""

import os
import io
import json
import urllib.request
import urllib.parse
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")

BREED_QUERIES = {
    # Cattle
    ("cattle", "gir"): ["Gir cattle cow", "Gir cow India", "Brazilian Gyr Cattle"],
    ("cattle", "sahiwal"): ["Sahiwal cattle cow", "Sahiwal cow", "Sahiwal bull"],
    ("cattle", "red_sindhi"): ["Red Sindhi cattle", "Red Sindhi cow"],
    ("cattle", "tharparkar"): ["Tharparkar cattle cow", "Thari cattle"],
    ("cattle", "rathi"): ["Rathi cattle cow Rajasthan", "Rathi cow"],
    ("cattle", "kankrej"): ["Kankrej cattle cow", "Kankarej Cow Gujarat"],
    ("cattle", "hariana"): ["Hariana cattle cow", "Haryana cow bull"],
    ("cattle", "ongole"): ["Ongole cattle bull", "Ongole cow India"],
    # Buffalo
    ("buffalo", "murrah"): ["Murrah buffalo India", "Murrah water buffalo"],
    ("buffalo", "jaffarabadi"): ["Jaffarabadi buffalo", "Jafarabadi buffalo Gujarat"],
    ("buffalo", "mehsana"): ["Mehsana buffalo", "Mehsani buffalo Gujarat"],
    ("buffalo", "surti"): ["Surti buffalo Gujarat", "Surti water buffalo"],
    ("buffalo", "nili_ravi"): ["Nili-Ravi buffalo Punjab", "Niliravi water buffalo"],
    ("buffalo", "banni"): ["Banni buffalo Kutch", "Kundi buffalo Banni"],
}


def search_wikimedia(query, limit=5):
    encoded = urllib.parse.quote(query)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrsearch={encoded}&gsrnamespace=6&prop=imageinfo&iiprop=url|size&gsrlimit={limit}"
    headers = {"User-Agent": "AntigravityLivestockBot/1.0 (academic research; skit.ac.in)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            results = []
            for pid, page in pages.items():
                imginfo = page.get("imageinfo", [{}])[0]
                img_url = imginfo.get("url")
                if img_url and (img_url.lower().endswith(".jpg") or img_url.lower().endswith(".jpeg") or img_url.lower().endswith(".png")):
                    results.append((page.get("title"), img_url))
            return results
    except Exception as e:
        print(f"Error querying Wikimedia for '{query}': {e}")
        return []


def download_and_save_image(url, target_path, max_dim=800):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw_bytes = resp.read()
            with Image.open(io.BytesIO(raw_bytes)) as img:
                img = img.convert("RGB")
                img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                img.save(target_path, "JPEG", quality=90)
                return True
    except Exception as e:
        print(f"Failed to download/process {url}: {e}")
        return False


def populate_reference_dataset(images_per_breed=3):
    print("=" * 65)
    print("FETCHING AUTHENTIC REFERENCE IMAGES FROM WIKIMEDIA COMMONS")
    print("=" * 65)

    downloaded_total = 0
    for (species, breed), queries in BREED_QUERIES.items():
        breed_dir = os.path.join(RAW_DIR, species, breed)
        os.makedirs(breed_dir, exist_ok=True)

        existing = [f for f in os.listdir(breed_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        if len(existing) >= images_per_breed:
            print(f"[{species.upper()}: {breed}] Already has {len(existing)} images. Skipping.")
            continue

        print(f"\nSearching images for {species} -> {breed}...")
        count = len(existing)
        for q in queries:
            if count >= images_per_breed:
                break
            results = search_wikimedia(q, limit=5)
            for title, img_url in results:
                if count >= images_per_breed:
                    break
                dest_file = os.path.join(breed_dir, f"{breed}_{count + 1}.jpg")
                if os.path.exists(dest_file):
                    continue

                print(f"  Downloading: {title} ...", end=" ")
                if download_and_save_image(img_url, dest_file):
                    print("[OK]")
                    count += 1
                    downloaded_total += 1
                else:
                    print("[FAIL]")

        print(f"[{species.upper()}: {breed}] Total: {count} reference images.")

    print("\n" + "=" * 65)
    print(f"DOWNLOAD COMPLETE: {downloaded_total} new reference images downloaded.")
    print("=" * 65)


if __name__ == "__main__":
    populate_reference_dataset(images_per_breed=3)

