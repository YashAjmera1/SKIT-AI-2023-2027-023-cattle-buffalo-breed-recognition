# Sprint 2: Backend Setup

**Member:** Kunal Rana (Backend and Database Development)
**Duration:** 01/09/2026 to 30/09/2026

## Task
Configure the FastAPI project structure, create application modules and implement basic request and response handling.

## Files for this sprint
- `backend/app/main.py`

## Work done
- FastAPI app with CORS for the React frontend
- `/` and `/health` endpoints
- Router modules registered; tables auto-created on startup

## How to verify
```bash
cd backend
uvicorn app.main:app --reload
# open http://localhost:8000/health
```
