"""
Model Training Script for Indian Cattle & Buffalo Breed Recognition.
Member: Vishal Gour (AI/ML Lead)
"""
import os
from ml.config import (
    CHECKPOINT_DIR, LOG_DIR, INITIAL_EPOCHS, FINE_TUNE_EPOCHS,
    INITIAL_LEARNING_RATE, FINE_TUNE_LEARNING_RATE, BATCH_SIZE
)
from ml.model import build_model, TF_AVAILABLE
from ml.dataset import create_dataset_pipeline


def train():
    if not TF_AVAILABLE:
        print("TensorFlow not installed. Skipping live training execution.")
        return

    import tensorflow as tf

    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    print("Building datasets...")
    train_ds = create_dataset_pipeline(split="train")
    val_ds = create_dataset_pipeline(split="val")

    if train_ds is None or val_ds is None:
        print("Dataset splits not found. Please run data preparation scripts first.")
        return

    print("Building EfficientNet-B0 transfer learning model...")
    model = build_model(fine_tune=False)

    checkpoint_path = os.path.join(CHECKPOINT_DIR, "best_model.keras")
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            checkpoint_path,
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        ),
        tf.keras.callbacks.CSVLogger(
            os.path.join(LOG_DIR, "training_history.csv")
        )
    ]

    print(f"--- Phase 1: Training Classification Head ({INITIAL_EPOCHS} epochs) ---")
    history_phase1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=INITIAL_EPOCHS,
        callbacks=callbacks
    )

    print(f"--- Phase 2: Fine-Tuning Top Convolutional Layers ({FINE_TUNE_EPOCHS} epochs) ---")
    # Unfreeze top layers
    for layer in model.layers[-30:]:
        if not isinstance(layer, tf.keras.layers.BatchNormalization):
            layer.trainable = True

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=FINE_TUNE_LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top_3_accuracy")]
    )

    history_phase2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=INITIAL_EPOCHS + FINE_TUNE_EPOCHS,
        initial_epoch=INITIAL_EPOCHS,
        callbacks=callbacks
    )

    print(f"Training completed successfully. Best checkpoint saved to {checkpoint_path}")


if __name__ == "__main__":
    train()

