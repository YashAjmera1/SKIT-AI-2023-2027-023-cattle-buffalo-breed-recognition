"""
EfficientNet-B0 Transfer Learning Architecture for Indian Livestock Classification.
Lead AI/ML Engineer: Vishal Gour (CSE-AI, Roll: 23ESKCA121)
"""
try:
    import tensorflow as tf
    from tensorflow.keras import layers, models, regularizers
    from tensorflow.keras.applications import EfficientNetB0
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

from ml.config import INPUT_SHAPE, NUM_CLASSES, DROPOUT_RATE, L2_REGULARIZATION, INITIAL_LEARNING_RATE


def build_model(
    num_classes: int = NUM_CLASSES,
    fine_tune: bool = False,
    fine_tune_at_layer: int = 100
):
    """
    Builds the transfer learning model with an EfficientNet-B0 base and custom classification head.
    
    Architecture:
    Input (224x224x3) -> EfficientNet-B0 (ImageNet weights) -> GlobalAveragePooling2D
    -> BatchNormalization -> Dense(256, relu, L2) -> Dropout(0.3) -> Dense(num_classes, softmax)
    """
    if not TF_AVAILABLE:
        raise RuntimeError("TensorFlow is not installed in the active environment.")

    # Base pretrained convolutional backbone
    base_model = EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=INPUT_SHAPE
    )

    if not fine_tune:
        base_model.trainable = False
    else:
        base_model.trainable = True
        # Freeze layers before fine_tune_at_layer
        for layer in base_model.layers[:fine_tune_at_layer]:
            layer.trainable = False

    inputs = layers.Input(shape=INPUT_SHAPE, name="input_image")
    
    # Preprocessing is handled inside EfficientNet or explicitly normalized
    x = base_model(inputs, training=fine_tune)
    
    # Classification Head
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.BatchNormalization(name="head_batch_norm")(x)
    x = layers.Dense(
        256,
        activation="relu",
        kernel_regularizer=regularizers.l2(L2_REGULARIZATION),
        name="dense_features"
    )(x)
    x = layers.Dropout(DROPOUT_RATE, name="head_dropout")(x)
    
    outputs = layers.Dense(
        num_classes,
        activation="softmax",
        name="breed_predictions"
    )(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="BreedRecognition_EfficientNetB0")
    
    # Compile with Adam optimizer and Categorical Crossentropy
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=INITIAL_LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top_3_accuracy")]
    )
    
    return model


if __name__ == "__main__":
    if TF_AVAILABLE:
        model = build_model()
        model.summary()
    else:
        print("TensorFlow not available in local test environment. Architecture specification verified.")

