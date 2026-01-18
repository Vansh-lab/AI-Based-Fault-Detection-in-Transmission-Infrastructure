#!/usr/bin/env python
"""
Complete Setup Script for Transmission Line Fault Detection System
Initializes all directories, validates setup, and prepares environment.
"""

import os
import sys
from pathlib import Path


def create_directory_structure():
    """Create complete directory structure for the project."""
    
    print("\n" + "="*80)
    print("📁 CREATING DIRECTORY STRUCTURE")
    print("="*80)
    
    base_path = Path(__file__).parent
    
    directories = [
        'dataset/train',
        'dataset/val',
        'dataset/test',
        'models',
        'logs',
        'results',
        'checkpoints'
    ]
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_path}")
    
    print("\n✓ Directory structure created successfully!")
    return base_path


def create_class_subdirectories(base_path):
    """Create class subdirectories for data organization."""
    
    print("\n" + "="*80)
    print("📂 CREATING CLASS SUBDIRECTORIES")
    print("="*80)
    
    class_names = ['Normal', 'Rusty_Structure', 'Damaged_Insulator']
    
    for split in ['train', 'val', 'test']:
        for class_name in class_names:
            class_dir = base_path / 'dataset' / split / class_name
            class_dir.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {class_dir}")
    
    print("\n✓ Class directories created successfully!")


def create_data_organization_guide(base_path):
    """Create a guide for organizing the dataset."""
    
    guide_content = """# Dataset Organization Guide

## Directory Structure

Your training data should be organized as follows:

```
dataset/
├── train/
│   ├── Normal/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── Rusty_Structure/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── Damaged_Insulator/
│       ├── image1.jpg
│       ├── image2.jpg
│       └── ...
├── val/
│   ├── Normal/
│   ├── Rusty_Structure/
│   └── Damaged_Insulator/
└── test/
    ├── Normal/
    ├── Rusty_Structure/
    └── Damaged_Insulator/
```

## Requirements

- **Minimum images per class**: 30+ images per split (train/val)
- **Recommended**: 100+ images per class for better training
- **File formats**: JPG, JPEG, PNG
- **Image size**: Any size (will be resized to 224x224 during training)
- **Class balance**: Try to have roughly equal images per class

## Class Definitions

1. **Normal**: Transmission towers in perfect/good condition
2. **Rusty_Structure**: Towers with rust, corrosion, or structural damage
3. **Damaged_Insulator**: Towers with damaged insulators or broken components

## Data Split Recommendation

- **Training (70%)**: Used to train the model
- **Validation (15%)**: Used to evaluate during training
- **Test (15%)**: Used for final evaluation after training

## Steps to Prepare Data

1. Collect drone images of transmission towers
2. Manually classify them into the three categories
3. Distribute images across train/val/test folders
4. Organize into class subdirectories as shown above
5. Run: `python setup_verify.py` to validate the setup

---

For more details, see README.md
"""
    
    guide_file = base_path / 'DATASET_GUIDE.md'
    with open(guide_file, 'w') as f:
        f.write(guide_content)
    
    print(f"\n✓ Dataset organization guide created: {guide_file}")


def check_dependencies():
    """Check if required packages are installed."""
    
    print("\n" + "="*80)
    print("🔍 CHECKING DEPENDENCIES")
    print("="*80)
    
    required_packages = [
        'tensorflow',
        'keras',
        'cv2',
        'numpy',
        'matplotlib',
        'streamlit',
        'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                import PIL
            else:
                __import__(package)
            print(f"✓ {package}: Installed")
        except ImportError:
            print(f"✗ {package}: NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n⚠️  Missing packages detected!")
        print("\nTo install missing dependencies, run:")
        print("pip install -r requirements.txt")
    else:
        print("\n✓ All required packages are installed!")
    
    return len(missing_packages) == 0


def create_sample_config(base_path):
    """Create a sample configuration file."""
    
    config_content = """# Configuration File for Fault Detection System

[Dataset]
dataset_dir = dataset/
image_size = 224
batch_size = 32
validation_split = 0.2

[Model]
architecture = MobileNetV2
num_classes = 3
learning_rate = 0.0001
dropout_rate = 0.5

[Training]
num_epochs = 20
early_stopping_patience = 5
learning_rate_reduce_patience = 3
save_best_only = True

[Classes]
class_0 = Normal
class_1 = Rusty_Structure
class_2 = Damaged_Insulator

[Output]
model_save_path = models/fault_detector_best.h5
training_history_path = training_history.png
logs_dir = logs/
"""
    
    config_file = base_path / 'config.ini'
    if not config_file.exists():
        with open(config_file, 'w') as f:
            f.write(config_content)
        print(f"\n✓ Configuration file created: {config_file}")
    else:
        print(f"\n✓ Configuration file already exists: {config_file}")


def print_setup_summary(base_path):
    """Print a comprehensive setup summary."""
    
    print("\n" + "="*80)
    print("✅ SETUP COMPLETE!")
    print("="*80)
    
    print(f"\nProject Root: {base_path}")
    print("\nProject Structure:")
    print("""
    AI-Based-Fault-Detection-in-Transmission-Infrastructure/
    ├── dataset/
    │   ├── train/  (add your training images here)
    │   ├── val/    (add your validation images here)
    │   └── test/   (add your test images here)
    ├── models/     (trained models saved here)
    ├── src/        (source code)
    │   ├── data_loader.py
    │   ├── model_builder.py
    │   ├── train.py
    │   └── grad_cam.py
    ├── app/        (web application)
    │   └── main.py
    ├── requirements.txt
    ├── run_training.bat  (Windows)
    ├── run_app.bat       (Windows)
    └── README.md
    """)
    
    print("\n" + "-"*80)
    print("🚀 NEXT STEPS:")
    print("-"*80)
    print("\n1. PREPARE DATA:")
    print("   - Organize your transmission tower images into:")
    print("     dataset/train/Normal/")
    print("     dataset/train/Rusty_Structure/")
    print("     dataset/train/Damaged_Insulator/")
    print("   - Similarly organize validation and test images")
    print("   - See DATASET_GUIDE.md for detailed instructions")
    
    print("\n2. INSTALL DEPENDENCIES:")
    print("   - Open PowerShell/Terminal")
    print("   - Run: pip install -r requirements.txt")
    
    print("\n3. VERIFY SETUP:")
    print("   - Run: python setup_verify.py")
    print("   - This will validate your data organization")
    
    print("\n4. TRAIN THE MODEL:")
    print("   - Run: python src/train.py")
    print("   - Or use: run_training.bat (Windows)")
    
    print("\n5. LAUNCH DASHBOARD:")
    print("   - Run: streamlit run app/main.py")
    print("   - Or use: run_app.bat (Windows)")
    print("   - Open: http://localhost:8501")
    
    print("\n" + "-"*80)
    print("📚 DOCUMENTATION:")
    print("-"*80)
    print("\n- README.md: Complete project documentation")
    print("- DATASET_GUIDE.md: How to prepare your dataset")
    print("- QUICKSTART.md: Quick start guide")
    print("\n" + "="*80 + "\n")


def main():
    """Main setup function."""
    
    print("\n" + "="*80)
    print("🔧 TRANSMISSION LINE FAULT DETECTION - SETUP")
    print("="*80)
    
    try:
        # Create directory structure
        base_path = create_directory_structure()
        
        # Create class subdirectories
        create_class_subdirectories(base_path)
        
        # Create data organization guide
        create_data_organization_guide(base_path)
        
        # Create sample configuration
        create_sample_config(base_path)
        
        # Check dependencies
        deps_ok = check_dependencies()
        
        # Print summary
        print_setup_summary(base_path)
        
        if not deps_ok:
            sys.exit(1)
        else:
            print("✅ Setup completed successfully!")
            return 0
    
    except Exception as e:
        print(f"\n❌ Setup failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
