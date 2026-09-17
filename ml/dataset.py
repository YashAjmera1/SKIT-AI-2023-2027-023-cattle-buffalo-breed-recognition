"""
Dataset Loader & Pipeline for Indian Cattle & Buffalo Breeds.
Member: Vishal Gour (AI/ML Lead)
"""
import os
from ml.config import DATA_DIR, BATCH_SIZE, IMAGE_SIZE, BREED_CLASSES

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


def create_dataset_pipeline(data_dir: str = DATA_DIR, split: str = "train", batch_size: int = BATCH_SIZE):
    """
    Creates an optimized tf.data.Dataset pipeline with prefetching and caching.
    """
    split_path = os.path.join(data_dir, split)
    if not os.path.exists(split_path):
        print(f"Directory {split_path} not found. Returning empty dataset placeholder.")
        return None

    if not TF_AVAILABLE:
        print("TensorFlow not installed. Dataset pipeline returning specification definition.")
        return None

    dataset = tf.keras.utils.image_dataset_from_directory(
        split_path,
        labels="categorical",
        label_mode="categorical",
        class_names=BREED_CLASSES,
        batch_size=batch_size,
        image_size=IMAGE_SIZE,
        shuffle=(split == "train"),
        seed=42
    )

    AUTOTUNE = tf.data.AUTOTUNE
    if split == "train":
        dataset = dataset.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    else:
        dataset = dataset.cache().prefetch(buffer_size=AUTOTUNE)

    return dataset

