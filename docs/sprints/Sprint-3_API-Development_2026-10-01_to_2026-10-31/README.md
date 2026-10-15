# Sprint 3: API Development

**Member:** Kunal Rana (Backend and Database Development)
**Duration:** 01/10/2026 to 31/10/2026

## Task
Develop image-upload and prediction endpoints, validate requests and prepare structured JSON responses.

## Files for this sprint
- `backend/app/schemas.py`
- `backend/app/routers/predict.py`
- `backend/app/routers/breeds.py`

## Work done
- `POST /api/v1/predict` (image upload)
- `GET /api/v1/predictions` history
- Breed CRUD under `/api/v1/breeds`
- Pydantic schemas for all responses

## How to verify
```bash
cd backend
# open http://localhost:8000/docs and try POST /api/v1/predict
```
