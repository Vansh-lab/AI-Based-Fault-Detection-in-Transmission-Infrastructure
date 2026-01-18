"""
Training Script for Fault Detection Model
Trains the transfer learning model with data augmentation and callbacks.
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# Import custom modules
from data_loader import get_data_generators
from model_builder import build_transfer_learning_model


def plot_training_history(history, save_path="../training_history.png"):
    """
    Plots and saves training history (accuracy and loss curves).
    
    Parameters:
    -----------
    history : keras.callbacks.History
        Training history object returned by model.fit()
    save_path : str
        Path to save the plot image
    """
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot Accuracy
    axes[0].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].set_title('Model Accuracy over Epochs', fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    # Plot Loss
    axes[1].plot(history.history['loss'], label='Training Loss', linewidth=2)
    axes[1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Loss', fontsize=12)
    axes[1].set_title('Model Loss over Epochs', fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Training history plot saved to: {save_path}")
    plt.show()


def setup_callbacks(model_save_path="../models/fault_detector_best.h5"):
    """
    Sets up training callbacks for model checkpointing and early stopping.
    
    Parameters:
    -----------
    model_save_path : str
        Path to save the best model
    
    Returns:
    --------
    list
        List of callback objects
    """
    
    callbacks = [
        # Save the best model based on validation loss
        ModelCheckpoint(
            filepath=model_save_path,
            monitor='val_loss',
            mode='min',
            save_best_only=True,
            verbose=1,
            save_weights_only=False
        ),
        
        # Early stopping if validation loss doesn't improve for 5 epochs
        EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate if validation loss plateaus
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    return callbacks


def train_model(dataset_dir="../dataset/", 
                model_save_dir="../models/",
                num_epochs=20,
                batch_size=32,
                num_classes=3):
    """
    Main training function that orchestrates the entire training pipeline.
    
    Parameters:
    -----------
    dataset_dir : str
        Path to the dataset directory
    model_save_dir : str
        Directory to save trained models
    num_epochs : int
        Number of training epochs (default: 20)
    batch_size : int
        Batch size for training (default: 32)
    num_classes : int
        Number of classes to classify (default: 3)
    """
    
    print("="*80)
    print("🚀 Starting Transmission Line Fault Detection Model Training")
    print("="*80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Dataset Directory: {dataset_dir}")
    print(f"Model Save Directory: {model_save_dir}")
    print(f"Number of Epochs: {num_epochs}")
    print(f"Batch Size: {batch_size}")
    print(f"Number of Classes: {num_classes}")
    print("="*80 + "\n")
    
    # ============= Step 1: Load Data Generators =============
    print("Step 1: Loading data generators...")
    train_generator, validation_generator = get_data_generators(
        data_dir=dataset_dir,
        image_size=(224, 224),
        batch_size=batch_size
    )
    
    print(f"✓ Training samples: {train_generator.samples}")
    print(f"✓ Validation samples: {validation_generator.samples}")
    print(f"✓ Class distribution: {train_generator.class_indices}\n")
    
    # ============= Step 2: Build Model =============
    print("Step 2: Building Transfer Learning Model (MobileNetV2)...")
    model = build_transfer_learning_model(
        num_classes=num_classes,
        image_size=(224, 224, 3),
        learning_rate=0.0001
    )
    
    print(f"✓ Model built successfully!")
    print(f"✓ Total parameters: {model.count_params():,}\n")
    
    # ============= Step 3: Setup Callbacks =============
    print("Step 3: Setting up training callbacks...")
    model_save_path = os.path.join(model_save_dir, "fault_detector_best.h5")
    callbacks = setup_callbacks(model_save_path=model_save_path)
    print(f"✓ Callbacks configured\n")
    
    # ============= Step 4: Train Model =============
    print("Step 4: Starting model training...")
    print("-" * 80)
    
    history = model.fit(
        train_generator,
        epochs=num_epochs,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    print("-" * 80)
    print("✓ Training completed!\n")
    
    # ============= Step 5: Plot Training History =============
    print("Step 5: Plotting and saving training history...")
    plot_training_history(
        history, 
        save_path=os.path.join(model_save_dir, "../training_history.png")
    )
    
    # ============= Step 6: Model Evaluation =============
    print("\nStep 6: Evaluating model on validation set...")
    val_loss, val_accuracy, val_precision, val_recall = model.evaluate(validation_generator)
    
    print(f"\n{'='*80}")
    print("📊 TRAINING SUMMARY")
    print(f"{'='*80}")
    print(f"Final Validation Loss: {val_loss:.4f}")
    print(f"Final Validation Accuracy: {val_accuracy*100:.2f}%")
    print(f"Final Validation Precision: {val_precision*100:.2f}%")
    print(f"Final Validation Recall: {val_recall*100:.2f}%")
    print(f"Best Model Saved: {model_save_path}")
    print(f"{'='*80}\n")
    
    return model, history


if __name__ == "__main__":
    # Default paths (relative to script location)
    dataset_path = os.path.join(os.path.dirname(__file__), "../dataset/")
    model_path = os.path.join(os.path.dirname(__file__), "../models/")
    
    # Ensure output directory exists
    os.makedirs(model_path, exist_ok=True)
    
    # Train the model
    trained_model, training_history = train_model(
        dataset_dir=dataset_path,
        model_save_dir=model_path,
        num_epochs=20,
        batch_size=32,
        num_classes=3
    )
    
    print("\n✅ Training pipeline completed successfully!")
