# Sprint 3: Image Upload

**Member:** Yash Ajmera (Frontend Development and API Integration)  
**Duration:** 01/10/2026 to 31/10/2026  
**Role:** Frontend Lead & UI/UX Designer (CSE-AI, Roll: 23ESKCA125)

## Task
Implement image selection, preview, upload controls, file validation and invalid-file messages.

## Files for this sprint
- `docs/sprints/Sprint-3_Image-Upload_2026-10-01_to_2026-10-31/README.md`
- `frontend/src/components/ImageUpload.jsx`

## Work done
- Built high-performance drag-and-drop file upload zone with visual hover feedback.
- Implemented robust client-side validation:
  - Allowed MIME types: `image/jpeg`, `image/png`, `image/webp`.
  - Enforced file size limit of 5.0 MB matching the FastAPI backend validation rules.
  - Added descriptive error banners for invalid extensions and oversized files.
- Added live image preview with memory-managed object URLs (`URL.createObjectURL` and cleanup).
- Integrated animal category selection (`Cattle 🐄` vs `Buffalo 🐃`).
- Embedded interactive sample breed selectors for quick validation without requiring manual local photo selection.
- Created responsive action controls for clearing and rescanning images.

## How to verify
1. Run frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```
2. Test uploading valid images (JPEG/PNG) and verify instant preview.
3. Test uploading invalid file types or oversized files to verify inline validation alerts.
