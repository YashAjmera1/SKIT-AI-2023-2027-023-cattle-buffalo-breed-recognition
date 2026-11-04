"""Run once:  python -m scripts.seed_breeds"""
from app.database import Base, SessionLocal, engine
from app import models

BREEDS = [
    ("Gir", "cattle", "Gujarat", 10, "Dairy"),
    ("Sahiwal", "cattle", "Punjab", 12, "Dairy"),
    ("Red Sindhi", "cattle", "Sindh region", 10, "Dairy"),
    ("Tharparkar", "cattle", "Rajasthan", 9, "Dairy / Draught"),
    ("Rathi", "cattle", "Rajasthan", 8, "Dairy"),
    ("Kankrej", "cattle", "Gujarat / Rajasthan", 6, "Dual purpose"),
    ("Hariana", "cattle", "Haryana", 6, "Dual purpose"),
    ("Ongole", "cattle", "Andhra Pradesh", 5, "Draught"),
    ("Murrah", "buffalo", "Haryana", 15, "Dairy"),
    ("Jaffrabadi", "buffalo", "Gujarat", 12, "Dairy"),
    ("Mehsana", "buffalo", "Gujarat", 10, "Dairy"),
    ("Surti", "buffalo", "Gujarat", 8, "Dairy"),
    ("Nili-Ravi", "buffalo", "Punjab", 12, "Dairy"),
    ("Banni", "buffalo", "Kutch, Gujarat", 11, "Dairy"),
]  # NOTE: yield values are approximate placeholders - verify before final report.

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    for name, species, origin, milk, use in BREEDS:
        if not db.query(models.Breed).filter_by(name=name).first():
            db.add(models.Breed(name=name, species=species, origin=origin,
                                milk_yield_litres_per_day=milk, primary_use=use))
    db.commit()
print("Seeded breeds.")
