"""
Model Evaluation Script
Evaluates the trained model on the test dataset and generates performance metrics.
"""

import os
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from data_loader import get_test_generator


def evaluate_model(model_path="models/fault_detector_best.h5", 
                   data_dir="dataset/",
                   batch_size=32,
                   class_names=None):
    """
    Evaluates the trained model on test dataset.
    
    Parameters:
    -----------
    model_path : str
        Path to the saved model
    data_dir : str
        Path to dataset directory
    batch_size : int
        Batch size for evaluation
    class_names : list
        List of class names
    
    Returns:
    --------
    dict
        Dictionary containing evaluation metrics
    """
    
    # Default class names
    if class_names is None:
        class_names = ['Normal', 'Rusty_Structure', 'Damaged_Insulator']
    
    print("="*80)
    print("🔬 MODEL EVALUATION ON TEST DATASET")
    print("="*80 + "\n")
    
    # ============= Step 1: Load Model =============
    print("Step 1: Loading trained model...")
    if not os.path.exists(model_path):
        print(f"❌ Model not found at: {model_path}")
        print("Please train the model first using: python src/train.py")
        return None
    
    try:
        model = load_model(model_path)
        print(f"✓ Model loaded successfully from: {model_path}\n")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return None
    
    # ============= Step 2: Load Test Generator =============
    print("Step 2: Loading test dataset...")
    try:
        test_generator = get_test_generator(
            data_dir=data_dir,
            image_size=(224, 224),
            batch_size=batch_size
        )
        print(f"✓ Test dataset loaded successfully")
        print(f"✓ Total test samples: {test_generator.samples}")
        print(f"✓ Number of batches: {len(test_generator)}\n")
    except Exception as e:
        print(f"❌ Error loading test dataset: {str(e)}")
        print(f"Make sure test images are organized in: {data_dir}test/[class_name]/")
        return None
    
    # ============= Step 3: Evaluate Model =============
    print("Step 3: Evaluating model...")
    print("-" * 80)
    
    try:
        # Evaluate on test set
        results = model.evaluate(test_generator, verbose=1)
        
        print("-" * 80)
        print("✓ Evaluation completed!\n")
        
        # Parse results (assuming model has loss, accuracy, precision, recall)
        if len(results) >= 2:
            test_loss = results[0]
            test_accuracy = results[1]
            test_precision = results[2] if len(results) > 2 else None
            test_recall = results[3] if len(results) > 3 else None
        else:
            test_loss = results[0]
            test_accuracy = results[1]
            test_precision = None
            test_recall = None
        
    except Exception as e:
        print(f"❌ Error during evaluation: {str(e)}")
        return None
    
    # ============= Step 4: Get Predictions & True Labels =============
    print("Step 4: Generating predictions on test set...")
    
    try:
        # Get predictions
        predictions = model.predict(test_generator, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)
        
        # Get true labels
        true_labels = test_generator.classes
        
        print(f"✓ Generated predictions for {len(true_labels)} samples\n")
        
    except Exception as e:
        print(f"❌ Error generating predictions: {str(e)}")
        return None
    
    # ============= Step 5: Classification Report =============
    print("="*80)
    print("📊 CLASSIFICATION REPORT")
    print("="*80 + "\n")
    
    try:
        class_report = classification_report(
            true_labels,
            predicted_classes,
            target_names=class_names,
            digits=4
        )
        print(class_report)
    except Exception as e:
        print(f"Error generating classification report: {str(e)}")
    
    # ============= Step 6: Confusion Matrix =============
    print("\n" + "="*80)
    print("🔍 CONFUSION MATRIX")
    print("="*80 + "\n")
    
    try:
        cm = confusion_matrix(true_labels, predicted_classes)
        
        # Print confusion matrix
        print("Confusion Matrix:")
        print(cm)
        print()
        
        # Plot and save confusion matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names,
            cbar_kws={'label': 'Count'}
        )
        plt.title('Confusion Matrix - Test Set', fontsize=14, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        
        # Save confusion matrix plot
        cm_path = "models/confusion_matrix.png"
        os.makedirs(os.path.dirname(cm_path), exist_ok=True)
        plt.savefig(cm_path, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrix plot saved to: {cm_path}\n")
        plt.close()
        
    except Exception as e:
        print(f"Error creating confusion matrix: {str(e)}\n")
    
    # ============= Step 7: Final Results Summary =============
    print("="*80)
    print("✅ TEST SET EVALUATION RESULTS")
    print("="*80)
    print(f"Test Loss:       {test_loss:.4f}")
    print(f"Test Accuracy:   {test_accuracy*100:.2f}%")
    if test_precision:
        print(f"Test Precision:  {test_precision*100:.2f}%")
    if test_recall:
        print(f"Test Recall:     {test_recall*100:.2f}%")
    print("="*80 + "\n")
    
    # Prepare evaluation metrics dictionary
    eval_metrics = {
        'test_loss': test_loss,
        'test_accuracy': test_accuracy,
        'test_precision': test_precision,
        'test_recall': test_recall,
        'confusion_matrix': cm if 'cm' in locals() else None,
        'predicted_classes': predicted_classes,
        'true_labels': true_labels,
        'class_names': class_names
    }
    
    return eval_metrics


def print_per_class_accuracy(eval_metrics):
    """
    Print accuracy for each class.
    
    Parameters:
    -----------
    eval_metrics : dict
        Evaluation metrics from evaluate_model()
    """
    
    if eval_metrics is None:
        return
    
    print("\n" + "="*80)
    print("📈 PER-CLASS ACCURACY")
    print("="*80)
    
    true_labels = eval_metrics['true_labels']
    predicted_classes = eval_metrics['predicted_classes']
    class_names = eval_metrics['class_names']
    
    for class_idx, class_name in enumerate(class_names):
        class_mask = true_labels == class_idx
        if class_mask.sum() > 0:
            class_accuracy = (predicted_classes[class_mask] == class_idx).mean()
            class_samples = class_mask.sum()
            print(f"{class_name:20s}: {class_accuracy*100:6.2f}% ({class_samples} samples)")
    
    print("="*80 + "\n")


if __name__ == "__main__":
    print("\n")
    
    # Evaluate the model
    eval_metrics = evaluate_model(
        model_path="models/fault_detector_best.h5",
        data_dir="dataset/",
        batch_size=32,
        class_names=['Normal', 'Rusty_Structure', 'Damaged_Insulator']
    )
    
    # Print per-class accuracy if evaluation was successful
    if eval_metrics:
        print_per_class_accuracy(eval_metrics)
        print("✅ Model evaluation completed successfully!")
    else:
        print("❌ Model evaluation failed. Check the errors above.")
