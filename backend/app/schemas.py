from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BreedBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    species: str = Field(pattern="^(cattle|buffalo)$")
    origin: str | None = None
    description: str | None = None
    milk_yield_litres_per_day: float | None = Field(default=None, ge=0)
    primary_use: str | None = None


class BreedCreate(BreedBase):
    pass


class BreedUpdate(BaseModel):
    origin: str | None = None
    description: str | None = None
    milk_yield_litres_per_day: float | None = Field(default=None, ge=0)
    primary_use: str | None = None


class BreedOut(BreedBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TopPrediction(BaseModel):
    breed: str
    confidence: float


class PredictionOut(BaseModel):
    id: int
    filename: str
    predicted_breed: str
    confidence: float
    top_predictions: list[TopPrediction]
    breed_info: BreedOut | None = None
    created_at: datetime


class PredictionHistory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    filename: str
    predicted_label: str
    confidence: float
    created_at: datetime
