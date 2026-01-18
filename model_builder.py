"""
Model Builder Module using Transfer Learning
Builds a CNN model using MobileNetV2 pre-trained on ImageNet for fault detection.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam


def build_transfer_learning_model(num_classes=3, image_size=(224, 224, 3), learning_rate=0.0001):
    """
    Builds a transfer learning model using MobileNetV2 architecture.
    
    The model uses:
    - MobileNetV2 base model pre-trained on ImageNet (frozen)
    - Custom head layers with GlobalAveragePooling2D
    - Dense layer with ReLU activation and Dropout
    - Output layer with Softmax for multi-class classification
    
    Parameters:
    -----------
    num_classes : int
        Number of output classes (default: 3 for Normal, Rusty_Tower, Damaged_Insulator)
    image_size : tuple
        Input image shape (height, width, channels). Default: (224, 224, 3)
    learning_rate : float
        Learning rate for Adam optimizer. Default: 0.0001
    
    Returns:
    --------
    model : keras.Model
        Compiled Keras model ready for training
    
    Example:
    --------
    >>> model = build_transfer_learning_model(num_classes=3)
    >>> model.summary()
    """
    
    # Load pre-trained MobileNetV2 model (without top classification layer)
    base_model = MobileNetV2(
        input_shape=image_size,
        include_top=False,           # Remove the default classification head
        weights='imagenet'           # Use ImageNet pre-trained weights
    )
    
    # Freeze the base model layers to preserve pre-trained weights
    base_model.trainable = False
    
    # Build custom head on top of the base model
    model = models.Sequential([
        # Input layer
        layers.Input(shape=image_size),
        
        # MobileNetV2 base model
        base_model,
        
        # Global Average Pooling to reduce spatial dimensions
        layers.GlobalAveragePooling2D(),
        
        # Dropout layer (50% dropout rate for regularization)
        layers.Dropout(0.5),
        
        # Dense layer with 128 units and ReLU activation
        layers.Dense(128, activation='relu', name='dense_128'),
        
        # Dropout layer before output
        layers.Dropout(0.3),
        
        # Output layer with Softmax for multi-class classification
        layers.Dense(num_classes, activation='softmax', name='output')
    ])
    
    # Compile the model with Adam optimizer and Categorical Crossentropy loss
    optimizer = Adam(learning_rate=learning_rate)
    
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy', 
                 tf.keras.metrics.Precision(name='precision'),
                 tf.keras.metrics.Recall(name='recall')]
    )
    
    return model


def build_model_with_fine_tuning(num_classes=3, image_size=(224, 224, 3), 
                                  learning_rate=0.0001, unfreeze_layers=50):
    """
    Builds a model with fine-tuning capability (unfreezes some base layers for training).
    
    Parameters:
    -----------
    num_classes : int
        Number of output classes
    image_size : tuple
        Input image shape
    learning_rate : float
        Learning rate for optimizer
    unfreeze_layers : int
        Number of base model layers to unfreeze from the end
    
    Returns:
    --------
    model : keras.Model
        Compiled model with fine-tuning enabled
    """
    
    # Build initial model with frozen base
    model = build_transfer_learning_model(num_classes, image_size, learning_rate)
    
    # Get the base model (first layer in sequential model)
    base_model = model.layers[0]
    
    # Unfreeze the last 'unfreeze_layers' layers for fine-tuning
    for layer in base_model.layers[-unfreeze_layers:]:
        layer.trainable = True
    
    # Recompile with lower learning rate for fine-tuning
    fine_tune_lr = learning_rate / 10  # Use lower learning rate for fine-tuning
    optimizer = Adam(learning_rate=fine_tune_lr)
    
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


if __name__ == "__main__":
    # Example usage
    print("Building Transfer Learning Model...")
    model = build_transfer_learning_model(num_classes=3)
    
    print("\n✓ Model built successfully!")
    print(f"\nModel Summary:")
    model.summary()
    
    print(f"\nTotal Parameters: {model.count_params():,}")
    print(f"Trainable Parameters: {sum([tf.keras.backend.count_params(w) for w in model.trainable_weights]):,}")
