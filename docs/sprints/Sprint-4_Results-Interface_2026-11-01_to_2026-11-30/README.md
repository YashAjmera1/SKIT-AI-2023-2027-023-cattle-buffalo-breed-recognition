# Sprint 4: Results Interface

**Member:** Yash Ajmera (Frontend Development and API Integration)  
**Duration:** 01/11/2026 to 30/11/2026  
**Role:** Frontend Lead & UI/UX Designer (CSE-AI, Roll: 23ESKCA125)

## Task
Develop the prediction-results page displaying breed names, confidence scores and available breed information.

## Files for this sprint
- `docs/sprints/Sprint-4_Results-Interface_2026-11-01_to_2026-11-30/README.md`
- `frontend/src/services/api.js`
- `frontend/src/components/ResultCard.jsx`
- `frontend/src/components/PredictionHistory.jsx`
- `frontend/src/App.jsx`

## Work done
- Developed comprehensive prediction results interface featuring:
  - High-visibility predicted breed title and species identification badge.
  - Dynamic animated confidence score gauge and percentage meter.
  - Top-3 candidate ranking distribution displaying comparative softmax probabilities.
  - Detailed breed dossier matrix covering origin geography, expected daily milk yield, primary usage (Dairy, Draught, Dual-purpose), and physical characteristics.
- Created `PredictionHistory.jsx` component displaying chronological log of analyzed images.
- Implemented `api.js` client layer communicating with FastAPI backend endpoints (`/api/v1/predict` and `/api/v1/predictions`).
- Engineered seamless standalone fallback mode with accurate livestock metadata for all 14 recognized Indian breeds, ensuring seamless demonstration even when the inference server is offline.

## How to verify
```bash
cd frontend
npm run dev
# open http://localhost:5173
```
Upload an image or select a quick sample, click **Identify Breed**, and observe the instantaneous results, confidence distribution, and breed profile card.
