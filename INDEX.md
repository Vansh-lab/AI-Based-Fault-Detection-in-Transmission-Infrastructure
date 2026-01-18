# 📚 PROJECT INDEX & DOCUMENTATION GUIDE

## 🎯 START HERE

**First time?** → Read [QUICKSTART.md](QUICKSTART.md) (5 minutes)

**Want details?** → Read [README.md](README.md)

**Need help?** → Check [PROJECT_COMPLETION.md](PROJECT_COMPLETION.md)

---

## 📂 DIRECTORY MAP

### Root Files
```
.
├── QUICKSTART.md           ← START HERE! Quick setup guide
├── README.md               ← Full documentation
├── PROJECT_COMPLETION.md   ← What was built
├── requirements.txt        ← Dependencies
├── config.py               ← Configuration
└── .gitignore              ← Git settings
```

### Source Code (src/)
```
src/
├── __init__.py            ← Package initialization
├── data_loader.py         ← Data augmentation (224×224, batch=32)
├── model_builder.py       ← MobileNetV2 transfer learning
├── train.py               ← Training pipeline (20 epochs)
└── grad_cam.py            ← Model explainability
```

### Application (app/)
```
app/
└── main.py                ← Streamlit web dashboard ⚡
```

### Data (dataset/)
```
dataset/
├── train/                 ← Training images
├── val/                   ← Validation images
└── test/                  ← Test images
```

### Models (models/)
```
models/
└── fault_detector_best.h5 ← (Generated after training)
```

### Utilities
```
setup_verify.py            ← Verify installation
test_inference.py          ← Test predictions
run_training.bat           ← Windows: Launch training
run_app.bat                ← Windows: Launch web app
```

---

## 🚀 QUICK COMMANDS

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Train
```bash
python src/train.py
```

### 3. Test
```bash
python test_inference.py
```

### 4. Deploy Web App
```bash
streamlit run app/main.py
```

### 5. Verify Setup
```bash
python setup_verify.py
```

---

## 📖 DOCUMENTATION BREAKDOWN

### QUICKSTART.md
- ✓ 5-minute setup
- ✓ Dataset preparation
- ✓ Training & deployment
- ✓ Basic troubleshooting
- ✓ Key tips

**Best for:** Getting started quickly

### README.md
- ✓ Complete project overview
- ✓ Technical architecture
- ✓ Detailed configuration
- ✓ Usage examples
- ✓ Future enhancements

**Best for:** Understanding the system

### PROJECT_COMPLETION.md
- ✓ What was built
- ✓ File descriptions
- ✓ Feature checklist
- ✓ Specifications
- ✓ Workflow diagram

**Best for:** Project overview

### config.py
- ✓ All parameters
- ✓ Easy customization
- ✓ Default values
- ✓ Configuration helpers

**Best for:** Tweaking settings

---

## 🔄 TYPICAL WORKFLOW

### Day 1: Setup
1. Run: `python setup_verify.py`
2. Read: QUICKSTART.md
3. Prepare: Dataset structure

### Day 2: Training
1. Organize images in dataset/
2. Run: `python src/train.py`
3. Monitor: Check training_history.png

### Day 3: Testing
1. Run: `python test_inference.py`
2. Test on: Your images
3. Verify: Accuracy >90%

### Day 4: Deployment
1. Run: `streamlit run app/main.py`
2. Test: Upload images
3. Verify: Grad-CAM working

---

## 🎓 EACH COMPONENT EXPLAINED

### data_loader.py
```
Purpose: Load & augment data
Input: dataset/ folder
Output: Train/val generators
Config: 224×224 size, batch=32
```

### model_builder.py
```
Purpose: Create CNN model
Architecture: MobileNetV2 + Custom head
Layers: GlobalAveragePooling2D, Dense(128), Dense(3)
Compile: Adam(0.0001), Categorical Crossentropy
```

### train.py
```
Purpose: Train the model
Epochs: 20
Callbacks: Checkpoint, EarlyStopping, ReduceLR
Output: models/fault_detector_best.h5
        training_history.png
```

### grad_cam.py
```
Purpose: Explainability
Method: Gradient-weighted Class Activation Mapping
Output: Heatmap + Overlay images
Use: Understand predictions
```

### app/main.py
```
Purpose: Web dashboard
Framework: Streamlit
Features: Upload → Predict → Visualize
Interface: Browser-based (localhost:8501)
```

---

## 📊 KEY METRICS

| Metric | Value |
|--------|-------|
| **Classes** | 3 (Normal, Rusty_Tower, Damaged_Insulator) |
| **Model Size** | ~10 MB |
| **Input Size** | 224 × 224 × 3 |
| **Training Time** | 10-30 min (GPU: faster) |
| **Inference Time** | <1 sec/image |
| **Expected Accuracy** | 85-95% |

---

## 🔧 CUSTOMIZATION GUIDE

### Change Image Size
```python
# In config.py
IMAGE_SIZE = (256, 256)  # was (224, 224)
```

### Change Number of Epochs
```python
# In config.py or src/train.py
NUM_EPOCHS = 30  # was 20
```

### Change Learning Rate
```python
# In config.py
LEARNING_RATE = 0.0005  # was 0.0001
```

### Change Classes
```python
# In config.py
CLASS_NAMES = ['Class1', 'Class2', 'Class3', 'Class4']
NUM_CLASSES = 4
```

---

## ⚡ POWER FEATURES

### Grad-CAM Visualization
Shows which image regions the model focused on:
- Red = High importance
- Blue = Low importance

### Early Stopping
Prevents overfitting:
- Patience = 5 epochs
- Stops if val_loss doesn't improve

### Adaptive Learning Rate
Reduces LR if stuck:
- Factor: 0.5x
- Patience: 3 epochs

### Model Checkpointing
Saves best model:
- Metric: val_loss
- File: models/fault_detector_best.h5

---

## 🐛 COMMON ISSUES & FIXES

| Issue | Solution |
|-------|----------|
| Model not found | Run `python src/train.py` |
| Missing packages | Run `pip install -r requirements.txt` |
| No images found | Check dataset/ folder structure |
| GPU errors | Works on CPU (GPU optional) |
| Memory error | Reduce batch size in config.py |
| Slow training | Use GPU or reduce image size |

---

## 📞 FILE LOCATIONS

```
dataset/train/
  ├── Normal/         ← Good condition images
  ├── Rusty_Tower/    ← Rust/corrosion images
  └── Damaged_Insulator/  ← Damaged insulator images

models/
  └── fault_detector_best.h5  ← Trained model (after training)

app/
  └── main.py         ← Web app (run with streamlit)
```

---

## ✅ VERIFICATION CHECKLIST

Before using:
- [ ] Python 3.7+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] setup_verify.py passes all checks
- [ ] Dataset folder structure correct
- [ ] Model trained and saved

---

## 🎯 NEXT STEPS

### For Training:
1. Prepare 100+ images per class
2. Organize in dataset/train/, val/
3. Run: `python src/train.py`
4. Check: training_history.png

### For Testing:
1. Run: `python test_inference.py`
2. Upload image or directory
3. View predictions & confidence

### For Deployment:
1. Run: `streamlit run app/main.py`
2. Open: http://localhost:8501
3. Upload: Transmission line images
4. See: Predictions + Grad-CAM

---

## 💡 BEST PRACTICES

✅ **Dataset:**
- 100+ images per class
- Balanced distribution
- Good image quality
- Consistent angles

✅ **Training:**
- Monitor training_history.png
- Stop if overfitting
- Use validation set
- Save best model

✅ **Deployment:**
- Test on diverse images
- Verify >90% accuracy
- Use with human review
- Retrain regularly

---

## 📚 LEARNING RESOURCES

- [TensorFlow Docs](https://tensorflow.org)
- [Keras API](https://keras.io)
- [Streamlit Docs](https://streamlit.io)
- [OpenCV Tutorials](https://opencv.org)
- Source code comments

---

## 🎉 YOU'RE READY!

Everything is set up. Time to:

1. **Prepare** your transmission line images
2. **Train** the model on your data
3. **Test** predictions
4. **Deploy** the web app
5. **Use** for predictive maintenance

---

**Questions?** Check the documentation in this order:
1. QUICKSTART.md (fast track)
2. README.md (detailed)
3. config.py (settings)
4. Source code comments (deep dive)

**Status:** ✅ **COMPLETE & READY**

---

*Built: January 18, 2026 | Version: 1.0.0 | Status: Production Ready*
