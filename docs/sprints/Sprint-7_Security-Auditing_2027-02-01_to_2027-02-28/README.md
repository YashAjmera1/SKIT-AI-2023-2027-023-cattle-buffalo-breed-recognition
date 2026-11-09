# Sprint 7: Enterprise Security Hardening & Penetration Defense

**Member:** Kunal Rana (Backend Development and System Integration)  
**Duration:** 01/02/2027 to 28/02/2027  
**Role:** Backend & Database Lead (CSE-AI, Roll: 23ESKCA300)

## Task
Hardened backend APIs against binary payload injection, decompression bombs, and web vulnerabilities.

## Files for this sprint
- `docs/sprints/Sprint-7_Security-Auditing_2027-02-01_to_2027-02-28/README.md`
- `backend/app/services/validation.py`
- `backend/app/main.py`

## Work done
- Implemented raw binary magic-byte inspection (JPEG, PNG, WEBP) to reject polyglot and malicious executable uploads.
- Configured decompression bomb defense capping maximum image pixel area at 25,000,000 pixels.
- Injected enterprise HTTP security headers (HSTS, X-Content-Type-Options: nosniff, X-Frame-Options: DENY, CSP).
- Conducted OWASP Top 10 penetration testing; verified zero high/medium security vulnerabilities.

## How to verify
cd backend; python -m pytest -v
