"""
Inference and Testing Script
Quick testing of the trained model on single images or a directory
"""

import os
import sys
from pathlib import Path
import numpy as np
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from grad_cam import visualize_prediction_with_gradcam, overlay_heatmap_on_image
except ImportError:
    visualize_prediction_with_gradcam = None
    print("⚠️ Grad-CAM module not available")

# Configuration
MODEL_PATH = Path(__file__).parent / "models" / "fault_detector_best.h5"
CLASS_NAMES = ['Normal', 'Rusty_Tower', 'Damaged_Insulator']
IMAGE_SIZE = (224, 224)

def load_model():
    """Load the trained model"""
    if not MODEL_PATH.exists():
        print(f"❌ Model not found at {MODEL_PATH}")
        print("Please train the model first: python src/train.py")
        return None
    
    try:
        model = tf.keras.models.load_model(str(MODEL_PATH))
        print(f"✓ Model loaded successfully from {MODEL_PATH}")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def predict_image(model, image_path):
    """Predict on a single image"""
    try:
        # Load and preprocess image
        img = Image.open(image_path).convert('RGB')
        img_resized = img.resize(IMAGE_SIZE)
        img_array = np.array(img_resized) / 255.0
        
        # Get prediction
        predictions = model.predict(img_array[np.newaxis, ...], verbose=0)
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        
        return {
            'class': CLASS_NAMES[class_idx],
            'confidence': confidence,
            'all_scores': {CLASS_NAMES[i]: float(predictions[0][i]) for i in range(len(CLASS_NAMES))}
        }
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return None

def test_single_image(model, image_path):
    """Test and visualize a single image"""
    print(f"\n{'='*80}")
    print(f"Testing: {image_path}")
    print(f"{'='*80}")
    
    if not Path(image_path).exists():
        print(f"❌ File not found: {image_path}")
        return
    
    result = predict_image(model, image_path)
    
    if result:
        print(f"\n✓ Prediction Results:")
        print(f"  Class: {result['class']}")
        print(f"  Confidence: {result['confidence']*100:.2f}%")
        print(f"\n  All Scores:")
        for class_name, score in result['all_scores'].items():
            bar_length = int(score * 50)
            bar = '█' * bar_length + '░' * (50 - bar_length)
            print(f"    {class_name:20s} [{bar}] {score*100:6.2f}%")
        
        # Check for maintenance alert
        if result['class'] in ['Rusty_Tower', 'Damaged_Insulator']:
            print(f"\n  ⚠️  MAINTENANCE REQUIRED")
        else:
            print(f"\n  ✅ NO FAULT DETECTED")

def test_directory(model, directory_path):
    """Test all images in a directory"""
    print(f"\n{'='*80}")
    print(f"Testing Directory: {directory_path}")
    print(f"{'='*80}")
    
    dir_path = Path(directory_path)
    if not dir_path.exists():
        print(f"❌ Directory not found: {directory_path}")
        return
    
    # Find all image files
    image_extensions = {'.jpg', '.jpeg', '.png'}
    image_files = [f for f in dir_path.rglob('*') 
                   if f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"❌ No images found in {directory_path}")
        return
    
    print(f"\nFound {len(image_files)} images\n")
    
    results = []
    for idx, image_file in enumerate(image_files, 1):
        print(f"[{idx}/{len(image_files)}] {image_file.name}...", end=" ")
        
        result = predict_image(model, str(image_file))
        if result:
            results.append({
                'file': image_file.name,
                'class': result['class'],
                'confidence': result['confidence']
            })
            print(f"✓ {result['class']} ({result['confidence']*100:.1f}%)")
        else:
            print("✗ Error")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    
    class_counts = {}
    for result in results:
        class_name = result['class']
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
    
    print("\nPredictions:")
    for class_name, count in sorted(class_counts.items()):
        print(f"  {class_name}: {count} images")
    
    avg_confidence = np.mean([r['confidence'] for r in results])
    print(f"\nAverage Confidence: {avg_confidence*100:.2f}%")
    
    fault_count = sum(1 for r in results if r['class'] in ['Rusty_Tower', 'Damaged_Insulator'])
    print(f"Faults Detected: {fault_count}/{len(results)}")

def interactive_mode(model):
    """Interactive testing mode"""
    print(f"\n{'='*80}")
    print("INTERACTIVE TESTING MODE")
    print(f"{'='*80}")
    print("\nCommands:")
    print("  1 = Test single image")
    print("  2 = Test directory")
    print("  3 = Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == '1':
                image_path = input("Enter image path: ").strip()
                test_single_image(model, image_path)
            
            elif choice == '2':
                dir_path = input("Enter directory path: ").strip()
                test_directory(model, dir_path)
            
            elif choice == '3':
                print("Exiting...")
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function"""
    print("\n" + "="*80)
    print("TRANSMISSION LINE FAULT DETECTION - INFERENCE SCRIPT")
    print("="*80)
    
    # Load model
    model = load_model()
    if model is None:
        return 1
    
    # Check command line arguments
    if len(sys.argv) > 1:
        # Test mode from command line
        path = sys.argv[1]
        
        if Path(path).is_file():
            test_single_image(model, path)
        elif Path(path).is_dir():
            test_directory(model, path)
        else:
            print(f"❌ Path not found: {path}")
            return 1
    else:
        # Interactive mode
        interactive_mode(model)
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        input("\nPress Enter to exit...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
