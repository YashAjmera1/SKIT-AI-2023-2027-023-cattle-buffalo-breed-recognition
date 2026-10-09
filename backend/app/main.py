"""Starter only: prediction and MongoDB are not implemented yet."""
from fastapi import FastAPI
app = FastAPI(title="Cattle & Buffalo Breed Recognition API", version="0.1.0", description="Starter API; prediction and MongoDB integration are not implemented yet.")
@app.get("/")
def root():
    return {"project": "Image-Based Breed Recognition System", "status": "starter", "message": "Prediction and database functionality are not implemented yet."}
@app.get("/health")
def health():
    return {"status": "ok"}
