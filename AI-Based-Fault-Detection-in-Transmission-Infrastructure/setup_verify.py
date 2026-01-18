"""
Setup and Verification Script for Transmission Line Fault Detection System
Verifies all components and prepares the project
"""

import os
import sys
from pathlib import Path
import importlib.util

def check_python_version():
    """Verify Python version is 3.7+"""
    print("✓ Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (Need 3.7+)")
        return False

def check_required_packages():
    """Check if required packages are installed"""
    print("\n✓ Checking required packages...")
    
    required_packages = [
        'tensorflow',
        'keras',
        'cv2',  # opencv-python
        'numpy',
        'matplotlib',
        'seaborn',
        'streamlit',
        'PIL',  # pillow
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                from PIL import Image
            else:
                importlib.import_module(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (MISSING)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n  Install missing packages with:")
        print(f"  pip install -r requirements.txt")
        return False
    
    return True

def check_directory_structure():
    """Verify directory structure"""
    print("\n✓ Checking directory structure...")
    
    base_dir = Path(__file__).parent
    required_dirs = {
        'src': ['data_loader.py', 'model_builder.py', 'train.py', 'grad_cam.py', '__init__.py'],
        'app': ['main.py'],
        'dataset': ['train', 'val', 'test'],
        'models': [],
    }
    
    all_ok = True
    
    for dir_name, files in required_dirs.items():
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
            
            for file_name in files:
                file_path = dir_path / file_name
                if file_path.exists():
                    print(f"    ✓ {file_name}")
                else:
                    print(f"    ✗ {file_name} (MISSING)")
                    all_ok = False
        else:
            print(f"  ✗ {dir_name}/ (MISSING)")
            all_ok = False
    
    return all_ok

def check_configuration_files():
    """Verify configuration files"""
    print("\n✓ Checking configuration files...")
    
    base_dir = Path(__file__).parent
    config_files = [
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'config.py',
        '.gitignore',
    ]
    
    all_ok = True
    
    for config_file in config_files:
        file_path = base_dir / config_file
        if file_path.exists():
            file_size = file_path.stat().st_size
            print(f"  ✓ {config_file} ({file_size} bytes)")
        else:
            print(f"  ✗ {config_file} (MISSING)")
            all_ok = False
    
    return all_ok

def check_dataset_preparation():
    """Check if dataset needs preparation"""
    print("\n✓ Checking dataset status...")
    
    base_dir = Path(__file__).parent
    dataset_dir = base_dir / 'dataset'
    
    subdirs = ['train', 'val', 'test']
    total_images = 0
    
    for subdir in subdirs:
        sub_path = dataset_dir / subdir
        if sub_path.exists():
            # Count all image files
            image_count = len(list(sub_path.glob('**/*.jpg'))) + \
                         len(list(sub_path.glob('**/*.jpeg'))) + \
                         len(list(sub_path.glob('**/*.png')))
            print(f"  {subdir}/: {image_count} images")
            total_images += image_count
        else:
            print(f"  {subdir}/: (empty)")
    
    if total_images == 0:
        print("\n  ⚠️  No dataset images found!")
        print("  Next steps:")
        print("  1. Create subdirectories: Normal/, Rusty_Tower/, Damaged_Insulator/")
        print("  2. Place training images in dataset/train/")
        print("  3. Place validation images in dataset/val/")
        print("  4. Run: python src/train.py")
        return False
    else:
        print(f"\n  ✓ Total images found: {total_images}")
        return True

def check_model_availability():
    """Check if trained model exists"""
    print("\n✓ Checking trained model...")
    
    base_dir = Path(__file__).parent
    model_path = base_dir / 'models' / 'fault_detector_best.h5'
    
    if model_path.exists():
        model_size = model_path.stat().st_size / (1024**2)  # Convert to MB
        print(f"  ✓ Model found: {model_path.name} ({model_size:.2f} MB)")
        return True
    else:
        print(f"  ✗ Model not found!")
        print("  Next step: Run 'python src/train.py' to train the model")
        return False

def verify_code_quality():
    """Basic syntax check for Python files"""
    print("\n✓ Checking Python code quality...")
    
    base_dir = Path(__file__).parent
    python_files = [
        base_dir / 'src' / 'data_loader.py',
        base_dir / 'src' / 'model_builder.py',
        base_dir / 'src' / 'train.py',
        base_dir / 'src' / 'grad_cam.py',
        base_dir / 'app' / 'main.py',
    ]
    
    all_ok = True
    
    for py_file in python_files:
        if py_file.exists():
            try:
                with open(py_file, 'r') as f:
                    compile(f.read(), py_file.name, 'exec')
                print(f"  ✓ {py_file.name}")
            except SyntaxError as e:
                print(f"  ✗ {py_file.name} - Syntax Error: {e}")
                all_ok = False
        else:
            print(f"  ✗ {py_file.name} (not found)")
            all_ok = False
    
    return all_ok

def print_summary(checks_passed):
    """Print verification summary"""
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    
    passed = sum([1 for v in checks_passed.values() if v])
    total = len(checks_passed)
    
    print(f"\nChecks passed: {passed}/{total}\n")
    
    for check_name, status in checks_passed.items():
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {check_name}")
    
    print("\n" + "="*80)
    
    if passed == total:
        print("\n✅ ALL CHECKS PASSED! System is ready to use.")
        print("\nNext steps:")
        print("1. Add your dataset to dataset/train/ and dataset/val/")
        print("2. Run: python src/train.py")
        print("3. Run: streamlit run app/main.py")
        return True
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return False

def main():
    """Run all verification checks"""
    print("\n" + "="*80)
    print("TRANSMISSION LINE FAULT DETECTION SYSTEM")
    print("Setup Verification")
    print("="*80 + "\n")
    
    checks_passed = {
        'Python Version': check_python_version(),
        'Required Packages': check_required_packages(),
        'Directory Structure': check_directory_structure(),
        'Configuration Files': check_configuration_files(),
        'Code Quality': verify_code_quality(),
        'Dataset Status': check_dataset_preparation(),
        'Model Availability': check_model_availability(),
    }
    
    success = print_summary(checks_passed)
    
    print("\nFor detailed information, see:")
    print("  - README.md (Project overview)")
    print("  - QUICKSTART.md (Quick start guide)")
    print("  - config.py (Configuration options)")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to exit...")
    sys.exit(exit_code)
