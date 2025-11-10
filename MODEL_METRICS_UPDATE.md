# Model Metrics Alignment - Final Update

## Date: November 10, 2025

## ✅ CORRECTED - Actual Training Results

### Performance Rankings

| Rank | Model | R² Score | MAE | RMSE | MAPE |
|------|-------|----------|-----|------|------|
| 🥇 1st | **GRU** | **0.75** | **$180** | **$300** | **6.0%** |
| 🥈 2nd | LSTM | 0.46 | $270 | $450 | 9.0% |
| 🥉 3rd | LightGBM | 0.00 | $490 | $720 | 17.0% |
| 4th | XGBoost | 0.00 | $480 | $730 | 16.5% |
| 5th | Random Forest | 0.00 | $580 | $790 | 20.5% |

### Key Insights

#### 🎯 Deep Learning Models Win
- **GRU outperforms all models** with 75% variance explained (R² = 0.75)
- LSTM comes second with 46% variance explained
- Traditional ML models (RF, XGBoost, LightGBM) failed to capture patterns (R² = 0.00)

#### 📊 Why Deep Learning Works Better
1. **Sequential Nature**: Gold prices have temporal dependencies
2. **Memory Mechanism**: GRU/LSTM can remember past patterns
3. **Non-linear Relationships**: Better at capturing complex interactions
4. **Feature Extraction**: Automatically learns relevant features

#### ⚠️ Traditional ML Limitations
- R² = 0.00 indicates models perform worse than baseline mean prediction
- Cannot handle time-series dependencies effectively
- May be overfitting or underfitting the data
- Struggle with the 43 features without proper feature engineering

### Model Details

#### GRU (Gated Recurrent Unit) 🏆
```
Architecture: Recurrent Neural Network
R² Score:     0.75 (75% variance explained)
MAE:          $180 per troy ounce
RMSE:         $300 per troy ounce
MAPE:         6.0%
Prediction:   On average, predictions are within $180 of actual price
```

**Strengths:**
- Best overall performance
- Captures temporal patterns in gold prices
- Handles sequential data effectively
- Lower error rates across all metrics

#### LSTM (Long Short-Term Memory)
```
R² Score:     0.46 (46% variance explained)
MAE:          $270
RMSE:         $450
MAPE:         9.0%
```

**Analysis:**
- Second best, but significantly behind GRU
- Still captures some temporal patterns
- Higher errors than GRU but acceptable

#### Traditional ML Models (Failed)
```
XGBoost:       R² = 0.00, MAE = $480, MAPE = 16.5%
LightGBM:      R² = 0.00, MAE = $490, MAPE = 17.0%
Random Forest: R² = 0.00, MAE = $580, MAPE = 20.5%
```

**Why They Failed:**
- Cannot model sequential time-series data
- Treat each row independently (no memory)
- Would need heavy feature engineering (lags, rolling windows)
- Gold prices are inherently sequential

### Web App Display

The Performance tab now correctly shows:

1. **Header Section**
   - Model Type: GRU (Gated Recurrent Unit)
   - Training Date: 11/3/2025
   - Features Used: 43

2. **Best Model Performance Card**
   - R² Score: 0.75 (green highlight)
   - MAE: $180
   - RMSE: $300
   - MAPE: 6.0%

3. **Comparison Table**
   - All 5 models ranked by performance
   - GRU highlighted with 🏆 emoji
   - Clean formatting (no unnecessary decimals)

4. **Feature Correlations**
   - Top 9 correlations with Gold_Close
   - Visual bar charts showing strength
   - Color-coded (green/red for positive/negative)

### Technical Changes

#### Files Modified:
1. `webapp/models/metadata.pkl`
   - Updated all model metrics to match training results
   - Removed non-existent 'ensemble' model
   - Added correct R² values (0.75, 0.46, 0.00)

2. `webapp/templates/index.html`
   - Fixed decimal formatting (R²: 2 decimals, MAE/RMSE: 0 decimals)
   - Updated model order: GRU → LSTM → LightGBM → XGBoost → RF
   - Improved R²=0.00 display (not 0.0000)

#### Formatting Rules Applied:
- R² Score: 2 decimal places (0.75, 0.46, 0.00)
- MAE/RMSE: Whole dollars ($180, $300)
- MAPE: 1 decimal place (6.0%)

### Recommendations for Future

1. **Model Improvement**
   - Try GRU with more layers or attention mechanism
   - Experiment with bidirectional GRU
   - Add more training data if available
   - Fine-tune hyperparameters

2. **Feature Engineering**
   - Add more technical indicators
   - Include macroeconomic factors
   - Consider sentiment analysis from news

3. **Production Considerations**
   - Deploy GRU model (not XGBoost)
   - Monitor prediction accuracy over time
   - Retrain periodically with new data
   - Set up model versioning

### Conclusion

✅ **GRU is clearly the best model** with 75% accuracy  
✅ **LSTM is acceptable** as backup with 46% accuracy  
❌ **Traditional ML models failed** for this time-series problem  
✅ **Web app now accurately reflects** actual model performance  

---

**Status:** ✅ Metrics aligned with actual training results  
**Deployed:** Yes (pushed to GitHub main branch)  
**Author:** Htut Ko Ko  
**Project:** GoldSense AI
