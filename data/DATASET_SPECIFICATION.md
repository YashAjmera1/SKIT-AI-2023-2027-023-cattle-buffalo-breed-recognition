# Dataset Specification & Taxonomy
**Project:** Image-Based Breed Recognition System for Cattle & Buffalo in India  
**Project ID:** SKIT/AI/2023-2027/023  
**Data & QA Lead:** Rajnish Kumar Patel (CSE-AI, Roll: 23ESKCA087)  
**Date:** September 2026

---

## 1. Scope & Taxonomy
The dataset contains annotated imagery of **14 indigenous Indian bovine breeds** recognized by the Indian Council of Agricultural Research (ICAR) and the National Bureau of Animal Genetic Resources (NBAGR).

### Target Classes (14 Breeds)
| Species | Breed Name | Primary Breeding Tract | Distinctive Morphological Markers |
| :--- | :--- | :--- | :--- |
| **Cattle** | **Gir** | Saurashtra / Gir Hills, Gujarat | Convex forehead, long leaf-like pendulous ears, red/speckled coat |
| **Cattle** | **Sahiwal** | Montgomery tract, Punjab border | Reddish-dun coat, heavy dewlap, loose skin |
| **Cattle** | **Red Sindhi** | Western Rajasthan border / Sindh | Deep red coloration, compact frame, medium horns |
| **Cattle** | **Tharparkar** | Thar desert, Western Rajasthan | White/light-grey heat-reflective coat, lyrical horns |
| **Cattle** | **Rathi** | Bikaner & Ganganagar, Rajasthan | Brown with white patches, medium build |
| **Cattle** | **Kankrej** | Rann of Kutch, Gujarat / Rajasthan | Majestic lyre-shaped horns, silver-grey coat, Sawai chal gait |
| **Cattle** | **Hariana** | Rohtak & Hisar, Haryana | Light grey/white coat, compact body, prominent forehead |
| **Cattle** | **Ongole** | Prakasam district, Andhra Pradesh | Muscular frame, large hump, short stumpy horns |
| **Buffalo** | **Murrah** | Rohtak & Jind, Haryana | Jet black coat, tightly curled spiral horns ("Black Gold") |
| **Buffalo** | **Jaffrabadi** | Saurashtra peninsula, Gujarat | Heaviest breed, massive drooping horns, prominent forehead |
| **Buffalo** | **Mehsana** | Mehsana, Gujarat | Murrah × Surti cross, docile, persistent lactation |
| **Buffalo** | **Surti** | Baroda & Kaira, Gujarat | Sickle-shaped flat horns, two white collars on brisket |
| **Buffalo** | **Nili-Ravi** | Sutlej & Ravi valleys, Punjab | "Panj Kalyan" markings (5 white points), wall eyes |
| **Buffalo** | **Banni** | Banni grasslands, Kutch | High heat/saline tolerance, nocturnal grazing adaptation |

---

## 2. Inclusion & Exclusion Criteria
- **Inclusion:**
  - Clear visibility of morphological markers (head, horns, coat color, hump, dewlap).
  - Varied natural farm environments (open pasture, sheds, unpaved ground).
  - Natural lighting (morning, noon, overcast conditions).
- **Exclusion:**
  - Extreme blur, severe occlusion (>50%), or non-bovine subjects.
  - Image resolutions below `150 × 150` pixels.
  - Exact or near-identical duplicate frames.

---

## 3. Data Split Strategy
- **Training Set (70%):** Model parameter optimization.
- **Validation Set (15%):** Hyperparameter tuning, early stopping, checkpoint selection.
- **Testing Set (15%):** Unbiased final evaluation on completely unseen livestock.

