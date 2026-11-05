# Sprint 4: Input Validation & Backend Integration

**Member:** Kunal Rana (Backend and Database Development)  
**Duration:** 01/11/2026 to 30/11/2026  
**Role:** Backend Lead & Database Architect (CSE, Roll: 23ESKCA300)

## Task
Validate file formats, handle missing or invalid images, implement exception handling with suitable HTTP status codes, and complete end-to-end model and database integration.

## Files for this sprint
- `backend/app/services/validation.py`
- `backend/app/crud.py`
- `backend/app/services/model_service.py`
- `backend/app/config.py`
- `backend/tests/test_api.py`

## Work done
- Validated incoming image uploads:
  - Allowed formats: `image/jpeg`, `image/png`, `image/webp`.
  - Max file size: 5.0 MB.
  - Returns HTTP 400 for empty or missing payloads.
  - Returns HTTP 413 for oversized files.
  - Returns HTTP 415 for unsupported media types.
  - Returns HTTP 422 for corrupted or unidentifiable image bytes.
- Implemented `app/crud.py` providing all database query and persistence methods for breeds and prediction histories.
- Implemented `app/services/model_service.py` singleton to handle inference preprocessing and prototype prediction serving.
- Seeded database with 14 indigenous cattle and buffalo breeds.
- Built comprehensive test suite in `tests/test_api.py` with 7/7 passing unit and integration tests.

## How to verify
```bash
cd backend
python -m pytest -v
# verify all 7 test cases pass
```
