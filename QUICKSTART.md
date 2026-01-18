# QUICK START GUIDE

## 🚀 Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Your Dataset
Organize images in the following structure:
```
dataset/
├── train/
│   ├── Normal/          (transmission towers in good condition)
│   ├── Rusty_Tower/     (towers with rust/corrosion)
│   └── Damaged_Insulator/ (towers with damaged insulators)
├── val/
│   ├── Normal/
│   ├── Rusty_Tower/
│   └── Damaged_Insulator/
└── test/
    ├── Normal/
    ├── Rusty_Tower/
    └── Damaged_Insulator/
```

**Minimum dataset size: 30-50 images per class for training**

### 3. Train the Model
**Option A: Using Windows batch file**
```bash
run_training.bat
```

**Option B: Using command line**
```bash
python src/train.py
```

The training will:
- Load and augment data
- Train MobileNetV2 model for 20 epochs
- Save best model to `models/fault_detector_best.h5`
- Generate `training_history.png` plot

**Expected training time: 10-30 minutes (depending on GPU)**

### 4. Run the Web Application
**Option A: Using Windows batch file**
```bash
run_app.bat
```

**Option B: Using command line**
```bash
streamlit run app/main.py
```

The app will open at: `http://localhost:8501`

---

## 📊 How to Use the App

1. **Upload Image**: Click "Browse files" and select a JPG/PNG image
2. **View Prediction**: See the predicted class and confidence score
3. **Check Confidence Scores**: View all class probabilities
4. **Read Alert**: Check if maintenance is required
5. **View Grad-CAM**: See where the model focused its attention

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `src/data_loader.py` | Data augmentation pipeline |
| `src/model_builder.py` | MobileNetV2 transfer learning model |
| `src/train.py` | Training script with callbacks |
| `src/grad_cam.py` | Model explainability visualization |
| `app/main.py` | Streamlit web dashboard |
| `config.py` | Centralized configuration |
| `requirements.txt` | Python dependencies |

---

## 🔧 Configuration

Edit `config.py` to customize:
- Image size (default: 224×224)
- Batch size (default: 32)
- Learning rate (default: 0.0001)
- Number of epochs (default: 20)
- Class names
- Confidence thresholds

---

## 📈 Understanding Results

### Prediction Classes
- **Normal**: Transmission line in good condition
- **Rusty_Tower**: Tower showing rust/corrosion (maintenance required)
- **Damaged_Insulator**: Damaged insulators (maintenance required)

### Grad-CAM Visualization
- **Red/Warm colors**: High activation (model focused here)
- **Blue/Cool colors**: Low activation (model ignored this area)

### Maintenance Alert
- **✅ Green Alert**: No fault detected (Normal)
- **⚠️ Yellow Alert**: Fault detected (Maintenance required)

---

## 🐛 Troubleshooting

### Model not found error
```
Solution: Run training first: python src/train.py
```

### CUDA/GPU errors
```
Solution: The model works on CPU. Remove GPU-specific code if needed.
```

### Data loading errors
```
Solution: Ensure dataset folder structure matches the pattern above
```

### Out of memory error
```
Solution: Reduce batch size in config.py (try 16 or 8)
```

---

## 📚 Technical Details

**Model**: MobileNetV2 (pre-trained on ImageNet)
- Lightweight (~3.5M parameters)
- Fast inference
- Good accuracy on small datasets

**Data Augmentation**:
- Rotation: ±20°
- Zoom: 0.85-1.15x
- Horizontal flip
- Width shift: ±20%

**Training**:
- Optimizer: Adam (lr=0.0001)
- Loss: Categorical Crossentropy
- Metrics: Accuracy, Precision, Recall
- Early stopping: patience=5 epochs

---

## 💡 Tips for Best Results

1. **Use good quality images** (clear, well-lit)
2. **Balance dataset** (similar number of images per class)
3. **Use consistent image angles** (for better generalization)
4. **Train with ~100+ images** per class for optimal accuracy
5. **Monitor training curves** (training_history.png)
6. **Validate on real-world images** before deployment

---

## 🚨 Important Notes

- This system is for **decision support only**, not a replacement for human inspection
- Always verify AI predictions with professional engineers
- Regular model retraining recommended with new data
- Ensure model accuracy >90% before production use

---

## 📞 Support

For issues or improvements, refer to:
- `README.md` - Detailed project documentation
- `config.py` - Configuration parameters
- Code comments in source files

---

**Happy fault detection! ⚡**
