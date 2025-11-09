# Models Directory

This directory contains trained machine learning models for gold price prediction.

## Required Files

The webapp needs these files to function:
- `best_model.pkl` or `best_model.h5` - Trained model
- `scaler_X.pkl` - Feature scaler
- `scaler_y.pkl` - Target scaler
- `feature_names.pkl` - List of feature names
- `metadata.pkl` - Model metadata and metrics

## How to Generate Models

Run one of these notebooks to train models:
1. **GoldSense_Train_Local.ipynb** - For local training
2. **GoldSense_Train_Combined_colab.ipynb** - For Google Colab

The notebooks will automatically save trained models to this directory.

## Git LFS for Large Models

If models exceed 100MB, use Git LFS:
```bash
git lfs track "models/*.h5"
git lfs track "models/*.pkl"
git add .gitattributes
```
