from sqlalchemy.orm import Session
from app import models, schemas


# Breed CRUD
def get_breed(db: Session, breed_id: int) -> models.Breed | None:
    return db.query(models.Breed).filter(models.Breed.id == breed_id).first()


def get_breed_by_name(db: Session, name: str) -> models.Breed | None:
    return db.query(models.Breed).filter(models.Breed.name.ilike(name.strip())).first()


def list_breeds(
    db: Session, species: str | None = None, skip: int = 0, limit: int = 100
) -> list[models.Breed]:
    query = db.query(models.Breed)
    if species:
        query = query.filter(models.Breed.species == species.lower())
    return query.offset(skip).limit(limit).all()


def create_breed(db: Session, data: schemas.BreedCreate) -> models.Breed:
    breed = models.Breed(
        name=data.name.strip(),
        species=data.species.lower(),
        origin=data.origin,
        description=data.description,
        milk_yield_litres_per_day=data.milk_yield_litres_per_day,
        primary_use=data.primary_use,
    )
    db.add(breed)
    db.commit()
    db.refresh(breed)
    return breed


def update_breed(
    db: Session, breed: models.Breed, data: schemas.BreedUpdate
) -> models.Breed:
    update_data = data.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(breed, field, val)
    db.commit()
    db.refresh(breed)
    return breed


def delete_breed(db: Session, breed: models.Breed) -> None:
    db.delete(breed)
    db.commit()


# Prediction CRUD
def save_prediction(
    db: Session, filename: str, predicted_label: str, confidence: float
) -> models.Prediction:
    # Attempt to associate with matching breed metadata
    breed = get_breed_by_name(db, predicted_label)
    prediction = models.Prediction(
        filename=filename,
        predicted_label=predicted_label,
        confidence=confidence,
        breed_id=breed.id if breed else None,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def list_predictions(
    db: Session, skip: int = 0, limit: int = 50
) -> list[models.Prediction]:
    return (
        db.query(models.Prediction)
        .order_by(models.Prediction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

