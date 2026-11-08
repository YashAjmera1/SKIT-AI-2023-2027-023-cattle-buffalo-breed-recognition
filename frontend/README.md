# BreedWise Frontend · Indian Livestock Recognition

**Member:** Yash Ajmera (Frontend Development & UI/UX Lead)  
**Session:** 2026-27  
**Department:** Computer Science & Engineering (AI), SKIT Jaipur  
**Project ID:** SKIT/AI/2023-2027/023

---

## Overview
A modern, responsive Single-Page Application (SPA) built with React 19 and Vite for image-based identification of indigenous Indian cattle and buffalo breeds using an EfficientNet-B0 transfer learning backbone.

## Key Features
- **UI/UX Design System:** Custom agricultural palette (Emerald `#059669`, Earth Amber `#D97706`), clean card containers, and mobile-friendly responsive layout.
- **Animal Category Selector:** Quick toggle between Indigenous Cattle (🐄) and Indigenous Buffalo (🐃).
- **Drag-and-Drop Image Uploader:** Interactive dropzone with client-side validation (`JPEG`, `PNG`, `WEBP`; max `5.0 MB`).
- **Live Preview & Quick Samples:** Immediate preview with remove controls, plus one-click sample images for instant verification.
- **Prediction Results Display:** Dynamic confidence percentage bar, top-3 candidates probability breakdown, and detailed breed dossier (origin, daily milk yield, primary purpose, traits).
- **FastAPI Integration:** Asynchronous communication with the FastAPI backend service (`/api/v1/predict` and `/api/v1/predictions`) with automatic fallback to standalone demo mode.
- **Session History Table:** Chronological log of analyzed livestock images with confidence scores.

## Sprints Completed (Member 2 — Yash Ajmera)
- **Sprint 1 (10/08/2026 - 31/08/2026):** UI/UX Design & Figma wireframes (`docs/sprints/Sprint-1_UI-UX-Design_...`).
- **Sprint 2 (01/09/2026 - 30/09/2026):** Frontend setup, React 19 + Vite architecture, and core components (`Navbar`, `Hero`, `Footer`).
- **Sprint 3 (01/10/2026 - 31/10/2026):** Drag-and-drop image upload, validation banners, and sample selectors (`ImageUpload.jsx`).
- **Sprint 4 (01/11/2026 - 30/11/2026):** Results interface, confidence score gauges, breed metadata cards, and API service (`ResultCard.jsx`, `api.js`).

## Running the Frontend Locally

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.
