import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/breed_db")
MODEL_PATH = os.getenv("MODEL_PATH", "models/efficientnet_b0_breed.keras")
CLASS_NAMES_PATH = os.getenv("CLASS_NAMES_PATH", "models/class_names.json")
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "5")) * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
IMAGE_SIZE = (224, 224)  # EfficientNet-B0 input
