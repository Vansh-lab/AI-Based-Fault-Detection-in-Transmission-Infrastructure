#!/usr/bin/env python
"""
Comprehensive Testing and Inference Script
Tests the trained model on new images with Grad-CAM visualization.
"""

import os
import sys
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from model_builder import build_transfer_learning_model
from grad_cam import visualize_prediction_with_gradcam, plot_grad_cam_results


def load_model(model_path):
    """Load a trained model from disk."""
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at: {model_path}")
    
    print(f"Loading model from: {model_path}")
    model = tf.keras.models.load_model(model_path)
    print("✓ Model loaded successfully!")
    return model


def preprocess_image(image_path, image_size=(224, 224)):
    """Load and preprocess an image."""
    
    img = Image.open(image_path).convert('RGB')
    img = img.resize(image_size)
    img_array = np.array(img) / 255.0
    return img_array


def predict_single_image(image_path, model, class_names, image_size=(224, 224)):
    """Make a prediction on a single image."""
    
    # Preprocess image
    img_array = preprocess_image(image_path, image_size)
    
    # Make prediction
    prediction = model.predict(np.expand_dims(img_array, 0), verbose=0)
    
    # Get results
    class_index = np.argmax(prediction[0])
    confidence = float(prediction[0][class_index])
    predicted_class = class_names[class_index]
    
    # Get all scores
    all_scores = {class_names[i]: float(prediction[0][i]) for i in range(len(class_names))}
    
    return {
        'class': predicted_class,
        'confidence': confidence,
        'all_scores': all_scores,
        'class_index': class_index
    }


def test_directory(test_dir, model, class_names, image_size=(224, 224)):
    """Test all images in a directory."""
    
    results = []
    test_path = Path(test_dir)
    
    # Find all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.PNG', '.JPEG']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(test_path.glob(f'*{ext}'))
    
    if not image_files:
        print(f"⚠️  No images found in {test_dir}")
        return results
    
    print(f"\nTesting {len(image_files)} images from: {test_dir}")
    print("-" * 80)
    
    for i, image_file in enumerate(image_files, 1):
        try:
            prediction = predict_single_image(str(image_file), model, class_names, image_size)
            results.append({
                'file': image_file.name,
                'prediction': prediction
            })
            
            print(f"{i:3d}. {image_file.name:40s} → "
                  f"{prediction['class']:20s} ({prediction['confidence']*100:.2f}%)")
        
        except Exception as e:
            print(f"{i:3d}. {image_file.name:40s} → ERROR: {str(e)}")
    
    print("-" * 80)
    print(f"✓ Testing complete! Processed {len(results)} images\n")
    
    return results


def visualize_results(results, class_names, layer_name='block_16_expand_relu', max_images=5):
    """Visualize predictions with Grad-CAM for sample images."""
    
    if not results:
        print("⚠️  No results to visualize")
        return
    
    print(f"\nGenerating Grad-CAM visualizations (max {max_images} images)...")
    
    for i, result in enumerate(results[:max_images]):
        try:
            image_path = result['file']
            
            # Generate Grad-CAM
            grad_cam_results = visualize_prediction_with_gradcam(
                image_path,
                model=None,  # Already have prediction
                class_names=class_names,
                layer_name=layer_name
            )
            
            # Plot results
            plot_grad_cam_results(grad_cam_results)
            
        except Exception as e:
            print(f"⚠️  Could not generate Grad-CAM for {result['file']}: {str(e)}")


def calculate_statistics(results, class_names):
    """Calculate and display statistics from test results."""
    
    if not results:
        return
    
    print("\n" + "="*80)
    print("📊 TEST STATISTICS")
    print("="*80)
    
    # Count predictions per class
    class_counts = {class_name: 0 for class_name in class_names}
    confidence_scores = []
    
    for result in results:
        pred_class = result['prediction']['class']
        confidence = result['prediction']['confidence']
        
        class_counts[pred_class] += 1
        confidence_scores.append(confidence)
    
    # Display statistics
    print("\nPrediction Distribution:")
    for class_name, count in class_counts.items():
        percentage = (count / len(results)) * 100 if results else 0
        print(f"  {class_name:20s}: {count:3d} images ({percentage:5.1f}%)")
    
    print(f"\nConfidence Statistics:")
    print(f"  Average Confidence: {np.mean(confidence_scores)*100:.2f}%")
    print(f"  Min Confidence:     {np.min(confidence_scores)*100:.2f}%")
    print(f"  Max Confidence:     {np.max(confidence_scores)*100:.2f}%")
    print(f"  Std Deviation:      {np.std(confidence_scores)*100:.2f}%")
    
    print("\n" + "="*80)


def main():
    """Main inference function."""
    
    parser = argparse.ArgumentParser(
        description='Test trained fault detection model on images'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='models/fault_detector_best.h5',
        help='Path to trained model'
    )
    parser.add_argument(
        '--test-dir',
        type=str,
        default='dataset/test',
        help='Directory containing test images'
    )
    parser.add_argument(
        '--image',
        type=str,
        help='Single image to test'
    )
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Generate Grad-CAM visualizations'
    )
    
    args = parser.parse_args()
    
    # Class names
    class_names = ['Normal', 'Rusty_Structure', 'Damaged_Insulator']
    
    print("\n" + "="*80)
    print("🔬 TRANSMISSION LINE FAULT DETECTION - INFERENCE")
    print("="*80 + "\n")
    
    try:
        # Load model
        model = load_model(args.model)
        
        # Test single image or directory
        if args.image:
            # Test single image
            print(f"\nTesting image: {args.image}")
            print("-" * 80)
            
            prediction = predict_single_image(args.image, model, class_names)
            
            print(f"Predicted Class: {prediction['class']}")
            print(f"Confidence: {prediction['confidence']*100:.2f}%")
            print("\nAll Predictions:")
            for class_name, score in prediction['all_scores'].items():
                print(f"  {class_name:20s}: {score*100:6.2f}%")
            
            # Generate Grad-CAM if requested
            if args.visualize:
                print("\nGenerating Grad-CAM visualization...")
                results = visualize_prediction_with_gradcam(
                    args.image,
                    model,
                    class_names,
                    layer_name='block_16_expand_relu'
                )
                plot_grad_cam_results(results)
        
        else:
            # Test directory
            results = test_directory(args.test_dir, model, class_names)
            
            if results:
                # Calculate statistics
                calculate_statistics(results, class_names)
                
                # Generate visualizations if requested
                if args.visualize and results:
                    visualize_results(results, class_names, max_images=3)
        
        print("\n✅ Testing completed successfully!")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
