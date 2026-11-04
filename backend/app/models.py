from datetime import datetime, timezone
from sqlalchemy import String, Text, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Breed(Base):
    __tablename__ = "breeds"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    species: Mapped[str] = mapped_column(String(20))  # cattle / buffalo
    origin: Mapped[str | None] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text)
    milk_yield_litres_per_day: Mapped[float | None] = mapped_column(Float)
    primary_use: Mapped[str | None] = mapped_column(String(100))

    predictions: Mapped[list["Prediction"]] = relationship(back_populates="breed")


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    predicted_label: Mapped[str] = mapped_column(String(100))
    confidence: Mapped[float] = mapped_column(Float)
    breed_id: Mapped[int | None] = mapped_column(ForeignKey("breeds.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    breed: Mapped[Breed | None] = relationship(back_populates="predictions")
