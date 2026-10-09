# Image-Based Breed Recognition System for Cattle and Buffalo in India

**Status: starter scaffold only.** No trained model, dataset pipeline, prediction endpoint, frontend, or database integration is implemented yet.

## Planned stack
- AI/ML: TensorFlow/Keras, EfficientNet-B0 transfer learning
- Image processing: OpenCV
- Backend: Python + FastAPI
- Database: MongoDB (per Form 1)
- Frontend: React + Tailwind CSS; UI/UX: Figma
- Tools: VS Code, Google Colab, GitHub

## Team roles
- Vishal Gour — AI/ML and model training
- Yash Ajmera — frontend and UI/UX
- Kunal Rana — backend, FastAPI and MongoDB
- Rajnish Kumar Patel — dataset, QA and documentation

## Run starter backend (Windows PowerShell)
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/health and http://127.0.0.1:8000/docs.

Keep the repository private. Invite only the verified mentor account. Do not commit datasets, model weights, `.env`, virtual environments, API keys, or personal data. Never backdate commits or claim unfinished work is complete.