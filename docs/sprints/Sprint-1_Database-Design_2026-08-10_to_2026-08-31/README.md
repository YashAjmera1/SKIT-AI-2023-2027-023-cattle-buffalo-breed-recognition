# Sprint 1: Database Design

**Member:** Kunal Rana (Backend and Database Development)
**Duration:** 10/08/2026 to 31/08/2026

## Task
Designed the database schema, defined breed information fields and configured database connectivity.

## Files for this sprint
- `backend/app/config.py`
- `backend/app/database.py`
- `backend/app/models.py`
- `backend/scripts/seed_breeds.py`
- `backend/docker-compose.yml`
- `backend/.env.example`
- `backend/requirements.txt`
- `backend/.gitignore`

## Cleanup
- Renamed the starter file `backend/app/init.py` to `backend/app/__init__.py` (Python needs the double underscores).
- Replaced the starter `requirements.txt`, which was stored as one line with literal `\n` text.

## Work done
- `breeds` table: name, species, origin, description, milk yield, primary use
- `predictions` table linked to `breeds` by foreign key
- PostgreSQL connection via `DATABASE_URL`

## How to verify
```bash
cd backend
docker compose up -d
python -m scripts.seed_breeds
```
