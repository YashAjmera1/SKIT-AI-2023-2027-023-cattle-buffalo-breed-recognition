# Backend Service · BreedWise

**Member:** Kunal Rana (Backend & Database Lead)  
**Session:** 2026-27  
**Department:** Computer Science & Engineering, SKIT Jaipur  
**Project ID:** SKIT/AI/2023-2027/023

---

## Overview
Asynchronous REST API service powered by **FastAPI** for Indian Cattle & Buffalo Breed Recognition. Serves image-based predictions, breed encyclopedic profiles, and session prediction histories.

## Tech Stack
- **Framework:** FastAPI 0.115+
- **ASGI Server:** Uvicorn
- **ORM / Database:** SQLAlchemy 2.0 (SQLite default zero-dependency / PostgreSQL support via `DATABASE_URL`)
- **Validation:** Pydantic v2 + Pillow
- **Testing:** Pytest + HTTPX

## Implemented Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API status and documentation link |
| `GET` | `/health` | Health probe (model mode: `mock` / `trained-model`) |
| `POST` | `/api/v1/predict` | Upload image (`JPEG/PNG/WEBP`, max 5MB) for breed prediction |
| `GET` | `/api/v1/predictions` | Query recent prediction history |
| `GET` | `/api/v1/breeds` | List indigenous breeds with optional `?species=cattle|buffalo` filter |
| `GET` | `/api/v1/breeds/{id}` | Detailed breed characteristics by ID |

## Sprints Completed (Member 1 — Kunal Rana)
- **Sprint 1 (10/08/2026 - 31/08/2026):** Database schema design, `Breed` and `Prediction` relational tables, SQLite/PostgreSQL configuration.
- **Sprint 2 (01/09/2026 - 30/09/2026):** FastAPI project setup, CORS middleware for React frontend, router architecture, health check.
- **Sprint 3 (01/10/2026 - 31/10/2026):** Prediction and Breed endpoints (`predict.py`, `breeds.py`), Pydantic schemas, and CRUD operations.
- **Sprint 4 (01/11/2026 - 30/11/2026):** Input validation (MIME types, 5MB limit, corrupt image checks with HTTP 400/413/415/422 status codes), model inference service, and test suite.

## Running the Backend

```powershell
cd backend

# Install dependencies
pip install -r requirements.txt

# Seed the 14 indigenous breeds
python -m scripts.seed_breeds

# Run automated tests
python -m pytest -v

# Start FastAPI server
python -m uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive Swagger documentation.
