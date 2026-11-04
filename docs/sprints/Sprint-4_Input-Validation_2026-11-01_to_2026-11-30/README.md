# Sprint 4: Input Validation

**Member:** Kunal Rana (Backend and Database Development)
**Duration:** 01/11/2026 to 30/11/2026

## Task
Validate file formats, handle missing or invalid images and implement exception handling with suitable HTTP status codes.

## Files for this sprint
- `backend/app/services/validation.py`

## Work done
- Allowed: JPEG, PNG, WEBP; max 5 MB
- 400 missing/empty, 413 too large, 415 wrong type, 422 corrupt image
- Global handlers for validation and unexpected errors

## How to verify
```bash
cd backend
pytest -v -k predict
```
