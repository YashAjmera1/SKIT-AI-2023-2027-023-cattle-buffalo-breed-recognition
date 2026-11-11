# SWAMI KESHVANAND INSTITUTE OF TECHNOLOGY, MANAGEMENT & GRAMOTHAN, JAIPUR
## Department of Computer Science & Engineering (Artificial Intelligence)
### FORM-1: B.TECH MAJOR PROJECT FORMULATION & SYNOPSIS

---

### Project Administrative Dossier
- **Project Reference ID:** `SKIT/AI/2023-2027/023`
- **Academic Session:** 2026–2027 (VII & VIII Semester)
- **Degree:** Bachelor of Technology in Computer Science & Engineering (Artificial Intelligence)
- **Project Title:** Image-Based Breed Recognition System for Cattle and Buffalo in India
- **Short Name / Brand:** BovineVision / BreedWise
- **Project Supervisor:** Dr. Mehul Mahrishi, Associate Professor, Department of CSE / AI

---

### Student Team Composition

| S.No | Roll No. | Student Name | Assigned Engineering Role | Core Technical Specialization |
| :---: | :---: | :--- | :--- | :--- |
| 1 | `23ESKCA125` | **Yash Ajmera** | Frontend & UI/UX Lead | React 19, Vite, WebRTC Device Camera, Responsive Ergonomics |
| 2 | `23ESKCA300` | **Kunal Rana** | Backend & Database Lead | FastAPI, YuNet Biometric Shield, YOLOv8 Gatekeeper, Security Hardening |
| 3 | `23ESKCA121` | **Vishal Gour** | AI/ML Model Lead | Multi-Modal Feature Tensors, EfficientNet-B0, Temperature Softmax |
| 4 | `23ESKCA087` | **Rajnish Kumar Patel** | Dataset & QA Lead | ICAR-NBAGR Taxonomy, Image Cleaning, OOD Benchmarking, Test Suites |

---

### 1. Problem Statement
India possesses the world's largest bovine population (193.4 million cattle and 109.8 million riverine buffaloes). However, indiscriminate cross-breeding, rural veterinary shortage, and the lack of accessible phenotypic pedigree verification tools have resulted in catastrophic genetic dilution across indigenous breeds. Traditional DNA sequencing is cost-prohibitive for rural farmers (₹2,500–₹5,000 per animal) and requires laboratory transit delays of 2–3 weeks.

Existing computer vision models for livestock classification operate strictly in closed-set environments: when a user inadvertently uploads a human face, domestic pet, document, or non-animal scene, standard models hallucinate a bovine breed classification (e.g. classifying a human selfie as "Sahiwal").

### 2. Project Objectives
1. **Target Taxonomy:** Classify the 14 foremost economically critical indigenous Indian livestock breeds accredited by the Indian Council of Agricultural Research – National Bureau of Animal Genetic Resources (ICAR-NBAGR):
   - **8 Cattle Breeds (*Bos indicus*):** Gir, Sahiwal, Red Sindhi, Tharparkar, Rathi, Kankrej, Hariana, Ongole.
   - **6 Buffalo Breeds (*Bubalus bubalis*):** Murrah, Jaffrabadi, Mehsana, Surti, Nili-Ravi, Banni.
2. **Tier-1 Out-of-Distribution (OOD) Domain Gatekeeper:**
   - Deep learning human biometric shield via OpenCV YuNet ONNX face landmark detector.
   - Real-time deep object discrimination via YOLOv8 nano (Cows vs Humans vs Other Animals vs Inanimate Objects).
   - Biological hide chromaticity and Laplacian focus entropy audits to reject blank pages, documents, and screenshots.
3. **Tier-2 Morphological Classification & Explainability:**
   - 198-dimensional multi-modal feature extraction (HSV 3D histograms, spatial 3×3 grid moments, Sobel edge orientations).
   - Temperature-scaled Softmax ($T = 0.18$) yielding dynamic, organic confidence distributions.
   - Full breed profile dossiers (native tract, lactation milk yield, A2 β-casein richness, visual morphological traits).
4. **Enterprise Security & Hack-Proof Hardening:**
   - Magic-byte raw binary validation blocking disguised executables.
   - Decompression bomb defense limiting image buffers to 25,000,000 pixels.
   - Enterprise HTTP headers (HSTS, nosniff, DENY, CSP).
5. **Deployment:** Production-grade responsive web interface supporting real-time camera capture, drag-and-drop uploads, and printable veterinary diagnostic slips.

---

### 3. System Architecture & Methodology

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER (React 19 + Vite)                  │
│   WebRTC Live Camera ──► Drag-and-Drop Dropzone ──► Magic-Byte Guard   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP Multipart / Encrypted
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               TIER-1 BIOMETRIC DOMAIN GATEKEEPER (FastAPI)              │
│  YuNet Face Shield   YOLOv8 Gatekeeper   Document Audit   Hide Chroma  │
│  (Rejects Humans)    (Cow vs Animals)    (Rejects Paper)  (Rejects Sky)│
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │ Approved Bovine                │ Rejected OOD
                    ▼                                ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│ TIER-2 MORPHOLOGICAL FEATURE TENSORS │  │ 🚫 BIOMETRIC REJECTION ALERT │
│ HSV Histograms + Spatial Grid + Sobel│  │ Diagnostic reason displayed  │
│ Temperature-Scaled Softmax (T=0.18)  │  │ Non-bovine classes rejected  │
└───────────────────┬──────────────────┘  └──────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               EXPLAINABLE AI DIAGNOSTIC DOSSIER & REPORT               │
│ Top-3 Probabilities | ICAR Accession Code | Milk Yield | Printable Slip │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 4. Hardware & Software Requirements

- **Software Stack:** Python 3.11+, FastAPI 0.115+, OpenCV 4.10+ / 5.0+, PyTorch / ONNX Runtime, React 19, Vite, Tailwind CSS, ReportLab 4.4+.
- **Pretrained Weights:** OpenCV YuNet ONNX (`face_detection_yunet.onnx`), Ultralytics YOLOv8 nano (`yolov8n.onnx`), Calibrated Ensemble (`breed_classifier.joblib`).
- **Hardware Minimum:** Quad-core x86_64 CPU, 8 GB RAM, 2 GB disk storage, standard USB webcam or mobile camera.

---

### 5. Alignment with National Missions & UN SDGs
- **Rashtriya Gokul Mission (Govt. of India):** Preservation and genetic upgradation of indigenous bovine germplasm.
- **UN Sustainable Development Goal 2 (Zero Hunger):** Enhancing dairy productivity and smallholder farmer livelihoods.
- **UN Sustainable Development Goal 15 (Life on Land):** Halting loss of biological diversity and indigenous livestock genetic resources.

---

### Endorsement & Approval

```
____________________________                    ____________________________
Yash Ajmera (Team Lead)                         Dr. Mehul Mahrishi (Project Supervisor)
Roll No: 23ESKCA125                             Associate Professor, Dept. of CSE/AI

____________________________                    ____________________________
Project Coordinator                             Head of Department (CSE / AI)
SKIT Jaipur                                     SKIT Jaipur
```

