# AI-Based Fault Detection System for Transmission Lines

## Overview
This project implements a **Deep Learning-based fault detection system** for transmission line infrastructure. It uses **Convolutional Neural Networks (CNN)** with **Transfer Learning** to classify transmission tower images into categories: Normal, Rusty_Tower, and Damaged_Insulator.

## Key Features
- **Transfer Learning**: Uses MobileNetV2 pre-trained on ImageNet for high accuracy with limited data
- **Data Augmentation**: Robust augmentation pipeline to handle limited datasets
- **Model Explainability**: Grad-CAM visualization to understand model predictions
- **Streamlit Dashboard**: Interactive web application for real-time fault detection
- **Predictive Maintenance**: Automated alerts for maintenance-required scenarios

## Project Structure
```
AI-Based-Fault-Detection-in-Transmission-Infrastructure/
├── dataset/
│   ├── train/          # Training dataset
│   ├── val/            # Validation dataset
│   └── test/           # Test dataset
├── src/
│   ├── data_loader.py  # Data augmentation pipeline
│   ├── model_builder.py # Transfer Learning model
│   ├── train.py        # Training script
│   └── grad_cam.py     # Model explainability
├── models/             # Saved trained models
├── app/
│   └── main.py         # Streamlit web application
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd AI-Based-Fault-Detection-in-Transmission-Infrastructure
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Prepare Dataset
Organize your transmission line images into:
```
dataset/
├── train/
│   ├── Normal/
│   ├── Rusty_Tower/
│   └── Damaged_Insulator/
├── val/
│   ├── Normal/
│   ├── Rusty_Tower/
│   └── Damaged_Insulator/
└── test/
    ├── Normal/
    ├── Rusty_Tower/
    └── Damaged_Insulator/
```

### 2. Train the Model
```bash
python src/train.py
```

This will:
- Load and augment training data
- Build MobileNetV2 transfer learning model
- Train for 20 epochs with callbacks
- Save the best model to `models/fault_detector_best.h5`
- Generate training history plots

### 3. Run the Streamlit Dashboard
```bash
streamlit run app/main.py
```

The dashboard allows you to:
- Upload transmission line images
- Get real-time fault predictions with confidence scores
- View Grad-CAM heatmaps for model explainability
- Receive maintenance alerts

## Technical Details

### Model Architecture
- **Base Model**: MobileNetV2 (ImageNet pre-trained)
- **Input Size**: 224 x 224 x 3
- **Custom Head**:
  - GlobalAveragePooling2D
  - Dense(128, ReLU, Dropout 0.5)
  - Dense(3, Softmax) for classification

### Data Augmentation
- **Training**: Rotation (20°), Zoom (0.15), Horizontal Flip, Width Shift, Rescaling (1/255)
- **Validation/Test**: Rescaling only (1/255)

### Training Configuration
- **Optimizer**: Adam (learning_rate=0.0001)
- **Loss**: Categorical Crossentropy
- **Batch Size**: 32
- **Epochs**: 20
- **Early Stopping**: Patience=5 on validation loss

## Classes
1. **Normal**: Tower in good condition
2. **Rusty_Tower**: Tower showing rust and corrosion
3. **Damaged_Insulator**: Tower with damaged insulators

## Model Explainability
The Grad-CAM (Gradient-weighted Class Activation Mapping) visualization shows:
- Which regions of the image the model focused on
- Heatmap overlays highlighting detected faults
- Enhanced interpretability for maintenance decisions

## Performance Metrics
After training, the system generates:
- Training and validation accuracy curves
- Loss reduction graphs
- Confusion matrices (optional)

## Future Enhancements
- Real-time video feed analysis
- Multi-camera fusion
- Anomaly detection using autoencoders
- Integration with IoT sensors
- Cloud deployment with AWS/GCP

## License
MIT License

## Author
AI Engineering Team
