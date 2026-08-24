"""
AI/ML Configuration for Indian Cattle & Buffalo Breed Recognition System.
Defines hyperparameters, breed classes, image dimensions, and training paths.
"""
import os

# Target Breeds Taxonomy (8 Cattle + 6 Buffalo = 14 Indigenous Breeds)
BREED_CLASSES = [
    # Cattle Breeds (Bos indicus)
    "Gir",
    "Sahiwal",
    "Red Sindhi",
    "Tharparkar",
    "Rathi",
    "Kankrej",
    "Hariana",
    "Ongole",
    # Buffalo Breeds (Bubalus bubalis)
    "Murrah",
    "Jaffrabadi",
    "Mehsana",
    "Surti",
    "Nili-Ravi",
    "Banni"
]

NUM_CLASSES = len(BREED_CLASSES)

# Input image specifications for EfficientNet-B0 backbone
IMAGE_SIZE = (224, 224)
INPUT_SHAPE = (224, 224, 3)

# Training Hyperparameters
BATCH_SIZE = 32
INITIAL_EPOCHS = 20
FINE_TUNE_EPOCHS = 15
TOTAL_EPOCHS = INITIAL_EPOCHS + FINE_TUNE_EPOCHS

INITIAL_LEARNING_RATE = 1e-3
FINE_TUNE_LEARNING_RATE = 1e-5

DROPOUT_RATE = 0.3
L2_REGULARIZATION = 1e-4

# Directories and Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
CHECKPOINT_DIR = os.path.join(BASE_DIR, "ml", "checkpoints")
EXPORT_MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")
LOG_DIR = os.path.join(BASE_DIR, "ml", "logs")

MODEL_EXPORT_PATH = os.path.join(EXPORT_MODEL_DIR, "efficientnet_b0_breed.keras")
CLASS_NAMES_EXPORT_PATH = os.path.join(EXPORT_MODEL_DIR, "class_names.json")

