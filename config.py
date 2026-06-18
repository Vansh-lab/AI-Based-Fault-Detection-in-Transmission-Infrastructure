"""
Configuration file for Transmission Line Fault Detection System
Centralized configuration for easy customization
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT PATHS
# ============================================================================
PROJECT_ROOT = Path(__file__).parent
DATASET_DIR = PROJECT_ROOT / "dataset"
MODELS_DIR = PROJECT_ROOT / "models"
SRC_DIR = PROJECT_ROOT / "src"
APP_DIR = PROJECT_ROOT / "app"

TRAIN_DIR = DATASET_DIR / "train"
VAL_DIR = DATASET_DIR / "val"
TEST_DIR = DATASET_DIR / "test"

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
MODEL_NAME = "fault_detector_best.h5"
MODEL_PATH = MODELS_DIR / MODEL_NAME

# Image configuration
IMAGE_SIZE = (224, 224)
IMAGE_CHANNELS = 3
INPUT_SHAPE = (224, 224, 3)

# Classes
CLASS_NAMES = ['Normal', 'Rusty_Tower', 'Damaged_Insulator']
NUM_CLASSES = len(CLASS_NAMES)

# Fault detection classes (for alert)
FAULT_CLASSES = ['Rusty_Tower', 'Damaged_Insulator']
NORMAL_CLASS = 'Normal'

# ============================================================================
# DATA AUGMENTATION CONFIGURATION
# ============================================================================
BATCH_SIZE = 32
ROTATION_RANGE = 20
ZOOM_RANGE = 0.15
HORIZONTAL_FLIP = True
WIDTH_SHIFT_RANGE = 0.2
HEIGHT_SHIFT_RANGE = 0.1

# ============================================================================
# MODEL TRAINING CONFIGURATION
# ============================================================================
NUM_EPOCHS = 20
LEARNING_RATE = 0.0001
OPTIMIZER = 'adam'
LOSS_FUNCTION = 'categorical_crossentropy'

# Callbacks configuration
EARLY_STOPPING_PATIENCE = 5
EARLY_STOPPING_MONITOR = 'val_loss'
EARLY_STOPPING_MODE = 'min'

REDUCE_LR_FACTOR = 0.5
REDUCE_LR_PATIENCE = 3
REDUCE_LR_MIN = 1e-7

# ============================================================================
# GRAD-CAM CONFIGURATION
# ============================================================================
GRAD_CAM_LAYER = 'block_16_expand_relu'  # For MobileNetV2
GRAD_CAM_COLORMAP = 'jet'
GRAD_CAM_ALPHA = 0.4

# ============================================================================
# STREAMLIT APP CONFIGURATION
# ============================================================================
APP_TITLE = "⚡ AI-Powered Transmission Line Fault Detector"
APP_ICON = "⚡"
APP_LAYOUT = "wide"

# Confidence thresholds
CONFIDENCE_THRESHOLD = 0.5
WARNING_THRESHOLD = 0.7  # Show warning if confidence > this

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================
TRAINING_HISTORY_PLOT = PROJECT_ROOT / "training_history.png"
GRAD_CAM_OUTPUT = PROJECT_ROOT / "grad_cam_output.png"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        MODELS_DIR,
        TRAIN_DIR,
        VAL_DIR,
        TEST_DIR,
        SRC_DIR,
        APP_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory ready: {directory}")


def print_config():
    """Print current configuration"""
    print("\n" + "="*80)
    print("PROJECT CONFIGURATION")
    print("="*80)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Model Path: {MODEL_PATH}")
    print(f"Dataset Dir: {DATASET_DIR}")
    print(f"\nModel Config:")
    print(f"  - Input Size: {IMAGE_SIZE}")
    print(f"  - Classes: {CLASS_NAMES}")
    print(f"\nTraining Config:")
    print(f"  - Epochs: {NUM_EPOCHS}")
    print(f"  - Batch Size: {BATCH_SIZE}")
    print(f"  - Learning Rate: {LEARNING_RATE}")
    print(f"  - Early Stopping Patience: {EARLY_STOPPING_PATIENCE}")
    print("="*80 + "\n")


if __name__ == "__main__":
    create_directories()
    print_config()
