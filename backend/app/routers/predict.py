from fastapi import APIRouter, Depends, File, UploadFile, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services.model_service import get_model
from app.services.validation import read_and_validate_image

router = APIRouter(prefix="/api/v1", tags=["Prediction"])


@router.post("/predict", response_model=schemas.PredictionOut)
async def predict_breed(
    file: UploadFile = File(..., description="Cattle or buffalo image (JPEG/PNG/WEBP)"),
    db: Session = Depends(get_db),
):
    data, image = await read_and_validate_image(file)
    top = get_model().predict(image, data, top_k=3)
    best = top[0]

    saved = crud.save_prediction(db, file.filename, best["breed"], best["confidence"])
    return schemas.PredictionOut(
        id=saved.id,
        filename=saved.filename,
        predicted_breed=best["breed"],
        confidence=best["confidence"],
        top_predictions=top,
        breed_info=saved.breed,
        created_at=saved.created_at,
    )


@router.get("/predictions", response_model=list[schemas.PredictionHistory])
def prediction_history(
    skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)
):
    return crud.list_predictions(db, skip, limit)
