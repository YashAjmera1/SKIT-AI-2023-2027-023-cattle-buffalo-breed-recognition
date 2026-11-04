from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/v1/breeds", tags=["Breeds"])


@router.get("", response_model=list[schemas.BreedOut])
def list_breeds(
    species: str | None = Query(None, pattern="^(cattle|buffalo)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.list_breeds(db, species, skip, limit)


@router.get("/{breed_id}", response_model=schemas.BreedOut)
def get_breed(breed_id: int, db: Session = Depends(get_db)):
    breed = crud.get_breed(db, breed_id)
    if not breed:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Breed not found.")
    return breed


@router.post("", response_model=schemas.BreedOut, status_code=status.HTTP_201_CREATED)
def create_breed(data: schemas.BreedCreate, db: Session = Depends(get_db)):
    if crud.get_breed_by_name(db, data.name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Breed already exists.")
    return crud.create_breed(db, data)


@router.put("/{breed_id}", response_model=schemas.BreedOut)
def update_breed(breed_id: int, data: schemas.BreedUpdate, db: Session = Depends(get_db)):
    breed = crud.get_breed(db, breed_id)
    if not breed:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Breed not found.")
    return crud.update_breed(db, breed, data)


@router.delete("/{breed_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_breed(breed_id: int, db: Session = Depends(get_db)):
    breed = crud.get_breed(db, breed_id)
    if not breed:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Breed not found.")
    crud.delete_breed(db, breed)
