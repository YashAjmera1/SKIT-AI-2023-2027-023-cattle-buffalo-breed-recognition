# Sprint 2: Frontend Setup

**Member:** Yash Ajmera (Frontend Development and API Integration)  
**Duration:** 01/09/2026 to 30/09/2026  
**Role:** Frontend Lead & UI/UX Designer (CSE-AI, Roll: 23ESKCA125)

## Task
Configure React and Tailwind CSS, organize the frontend structure and create reusable interface components.

## Files for this sprint
- `docs/sprints/Sprint-2_Frontend-Setup_2026-09-01_to_2026-09-30/README.md`
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/index.html`
- `frontend/src/main.jsx`
- `frontend/src/index.css`
- `frontend/src/components/Navbar.jsx`
- `frontend/src/components/Hero.jsx`
- `frontend/src/components/Footer.jsx`

## Work done
- Initialized React 19 single-page application structure powered by Vite for instant Hot Module Replacement (HMR).
- Built comprehensive design system and CSS styling layer with responsive utility classes.
- Created modular, reusable UI components:
  - `Navbar.jsx`: Application brand identity (`BreedWise`), SKIT CSE-AI project identification, UN SDG 2 badge, and live backend connectivity status.
  - `Hero.jsx`: Engaging agricultural introduction highlighting indigenous Indian cattle and buffalo biodiversity and preservation goals.
  - `Footer.jsx`: Department attribution, session 2026-27 records, and repository metadata.
- Configured Vite build tooling with clean path resolution and asset bundling.

## How to verify
```bash
cd frontend
npm install
npm run dev
# open http://localhost:5173
```
