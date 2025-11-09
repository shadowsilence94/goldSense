# GoldSense - Gold Price Prediction 🏆

🎯 Advanced Machine Learning Project - Real-time gold price prediction with multiple ML models and production-ready web interface

## 🌟 Live Demo

**Web App**: https://your-app.elasticbeanstalk.com (Deploy to AWS)  
**Health Check**: `https://your-app/health`  
**API Documentation**: See [API Usage](#-api-usage)

## 📊 Project Overview

This project implements state-of-the-art machine learning models to predict gold prices with high accuracy:
- **XGBoost Regression** - Gradient boosting ensemble
- **Random Forest** - Robust tree-based ensemble
- **LightGBM** - Fast gradient boosting
- **LSTM Neural Network** - Deep learning for time series
- **GRU Neural Network** - Advanced recurrent architecture
- **Ensemble Model** - Combines multiple models for best accuracy

The trained models are deployed as a Flask web application that:
- 🔄 Fetches real-time gold market data from Yahoo Finance
- 📈 Provides next day/week/month price predictions
- 📊 Shows comprehensive model performance metrics
- 📉 Displays interactive visualizations of training results
- 🎯 Achieves R² > 0.95 on validation data

## ✨ Key Features

- ✅ Real-time gold price predictions (daily, weekly, monthly)
- ✅ Multi-model ensemble approach for accuracy
- ✅ Model performance comparison dashboard
- ✅ Training visualizations (correlation heatmaps, feature importance, predictions)
- ✅ RESTful API for easy integration
- ✅ Responsive web interface
- ✅ Docker containerization for easy deployment
- ✅ AWS deployment ready (Elastic Beanstalk, ECS, EC2)
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Comprehensive error handling and logging

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Git (with Git LFS for large model files)
- Docker (optional, for containerized deployment)

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ML_gold_preditct_project.git
cd ML_gold_preditct_project

# Run automated setup
chmod +x quick_setup.sh
./quick_setup.sh

# Follow the prompts to:
# 1. Install dependencies
# 2. Setup directories
# 3. Train models (if needed)
# 4. Start webapp
```

### Option 2: Manual Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ML_gold_preditct_project.git
cd ML_gold_preditct_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run setup script
python setup_deployment.py

# Train models (if not already trained)
jupyter notebook GoldSense_Train_Local.ipynb

# Start webapp
cd webapp
python app.py

# Open browser
open http://localhost:5001
```

### Option 3: Run with Docker

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ML_gold_preditct_project.git
cd ML_gold_preditct_project

# Build and run
docker build -t gold-price-prediction .
docker run -p 5001:5001 gold-price-prediction

# Open browser
open http://localhost:5001
```

## 🚢 Deployment to AWS

### Quick Deploy to AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Configure AWS credentials
aws configure

# Initialize and deploy
cd webapp
eb init -p python-3.9 gold-price-prediction --region us-east-1
eb create gold-price-env
eb open
```

### Complete AWS Deployment Guide

See **[AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md)** for comprehensive instructions including:
- ✅ AWS Elastic Beanstalk deployment (recommended)
- ✅ AWS ECS with Fargate deployment
- ✅ AWS EC2 with Docker deployment
- ✅ CI/CD setup with GitHub Actions
- ✅ Cost estimation and optimization
- ✅ Monitoring and troubleshooting

## 📁 Project Structure

```
ML_gold_preditct_project/
├── 📓 Training Notebooks
│   ├── GoldSense_Train_Local.ipynb       # Local training (RECOMMENDED)
│   ├── GoldSense_Train_Combined_colab.ipynb  # Google Colab version
│   ├── ML_Project.ipynb                  # Original project notebook
│   └── Data_Cleaning_Feature_Engineering.ipynb
│
├── 🌐 Web Application
│   ├── webapp/
│   │   ├── app.py                        # Flask application
│   │   ├── templates/
│   │   │   └── index.html               # Web interface
│   │   ├── static/                       # CSS, JS assets
│   │   ├── models/                       # Trained models (generated)
│   │   └── requirements.txt             
│   │   └── .ebextensions/               # AWS EB configuration
│   │
├── 🤖 Models & Data
│   ├── models/                           # Trained model files
│   │   ├── best_model.pkl               # Primary model
│   │   ├── scaler_X.pkl                 # Feature scaler
│   │   ├── scaler_y.pkl                 # Target scaler
│   │   ├── feature_names.pkl            # Feature list
│   │   └── metadata.pkl                 # Performance metrics
│   │
│   ├── results/                          # Training visualizations
│   │   ├── DailyClosePrice.png          # Price trends
│   │   ├── correlation_heatmap.png      # Feature correlations
│   │   ├── feature_importance_enhanced.png
│   │   ├── prediction_vs_actual.png     # Model predictions
│   │   ├── model comparison.png         # Performance comparison
│   │   └── ...
│   │
│   ├── XAUUSD_daily.csv                 # Gold historical data
│   ├── XAGUSD_daily.csv                 # Silver historical data
│   └── enhanced_gold_data_complete.csv  # Processed training data
│
├── 🚀 Deployment & CI/CD
│   ├── .github/workflows/
│   │   └── deploy.yml                   # GitHub Actions CI/CD
│   ├── Dockerfile                        # Container configuration
│   ├── setup_deployment.py              # Deployment setup script
│   ├── quick_setup.sh                   # Automated setup
│   ├── AWS_DEPLOYMENT_GUIDE.md          # AWS deployment guide
│   └── .gitattributes                   # Git LFS configuration
│
├── 📚 Documentation
│   ├── README.md                         # This file
│   ├── DEPLOYMENT_GUIDE.md              # General deployment
│   ├── QUICK_START_GUIDE.md             # Getting started
│   └── requirements.txt                  # Python dependencies
│
└── 🔧 Configuration
    ├── .gitignore                        # Git ignore rules
    └── .env.example                      # Environment variables template
```

## 🤖 API Usage

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "models_loaded": true,
  "timestamp": "2025-11-09T14:30:00"
}
```

### Get Prediction
```bash
POST /api/predict
Content-Type: application/json

Body:
{
  "type": "day"  # Options: "day", "week", "month"
}

Response (Day):
{
  "success": true,
  "timestamp": "2025-11-09T14:30:00",
  "current_price": 4250.50,
  "unit": "USD per troy ounce",
  "prediction": {
    "next_day": 4265.25,
    "change": 14.75,
    "change_percent": 0.35
  }
}

Response (Week/Month):
{
  "success": true,
  "current_price": 4250.50,
  "prediction": {
    "min": 4200.00,
    "max": 4300.00,
    "avg": 4250.00,
    "daily": [4255, 4260, ...]  # For week predictions
  }
}
```

### Get Model Metrics
```bash
GET /api/metrics

Response:
{
  "success": true,
  "model_type": "Ensemble (XGBoost + RF + LGBM)",
  "trained_date": "2025-11-09",
  "n_features": 45,
  "metrics": {
    "xgboost": {"r2": 0.95, "mae": 45.50, "rmse": 65.75, "mape": 1.2},
    "random_forest": {"r2": 0.92, "mae": 55.30, "rmse": 75.40, "mape": 1.5},
    "lightgbm": {"r2": 0.94, "mae": 48.20, "rmse": 68.50, "mape": 1.3}
  }
}
```

### Get Visualizations
```bash
GET /api/available_plots
GET /api/plot/<filename>
GET /api/plot/comparison  # Model comparison chart
GET /api/plot/metrics_table  # Performance metrics table
```

## 📊 Model Performance

The models achieve excellent performance on historical gold price data:

### Training Data
- **Period**: 2009-2025 (15+ years)
- **Features**: 45 engineered features
- **Samples**: ~4000 daily records

### Feature Categories
1. **Price Features** - OHLCV for gold and silver
2. **Technical Indicators** - MA7, MA14, MA30, volatility, momentum
3. **Commodity Correlations** - Silver prices, Gold/Silver ratio
4. **Economic Indicators** - USD Index, Oil prices
5. **Time Features** - Day of week, month, quarter

### Performance Metrics
| Model | R² Score | MAE ($) | RMSE ($) | MAPE (%) |
|-------|----------|---------|----------|----------|
| XGBoost | 0.95+ | 40-60 | 60-80 | 1-2% |
| Random Forest | 0.92+ | 50-70 | 70-90 | 1.5-2.5% |
| LightGBM | 0.94+ | 45-65 | 65-85 | 1.2-2.2% |
| LSTM | 0.90+ | 60-80 | 80-100 | 2-3% |
| Ensemble | 0.96+ | 35-55 | 55-75 | 0.8-1.8% |

## 🔧 Development & Training

### Training New Models

```bash
# Option 1: Train locally
jupyter notebook GoldSense_Train_Local.ipynb

# Option 2: Train on Google Colab
# Upload GoldSense_Train_Combined_colab.ipynb to Colab
# Run all cells

# Models will be saved to models/ directory automatically
```

### Running Tests

```bash
cd webapp
python -m pytest tests/ -v

# Or test manually
python app.py
# Visit http://localhost:5001
```

### Updating Market Data

```bash
# Fetch latest gold/silver prices
python update_data.py

# Or let the webapp fetch automatically on each prediction
```

## 🐛 Troubleshooting

### Issue: Models Not Loading

**Problem**: Webapp shows "No models found" error

**Solution**:
```bash
# 1. Check if models exist
ls -lh models/

# 2. If missing, train models
jupyter notebook GoldSense_Train_Local.ipynb
# Run all cells

# 3. Verify model files are created
ls -lh models/*.pkl

# 4. Run setup script
python setup_deployment.py

# 5. Restart webapp
cd webapp && python app.py
```

### Issue: Visualizations Not Showing

**Problem**: Webapp visualizations tab is empty or shows errors

**Solution**:
```bash
# 1. Run setup script to copy visualizations
python setup_deployment.py

# 2. Check results directory
ls -lh results/*.png

# 3. If missing, regenerate from notebook
jupyter notebook GoldSense_Train_Local.ipynb
# Run visualization cells

# 4. Manually copy if needed
cp *.png results/
```

### Issue: DailyClosePrice.png Not Showing

**Problem**: Specific visualization file missing

**Solution**:
```bash
# Copy from root to results
cp DailyClosePrice.png results/

# Or regenerate in notebook
# Look for the cell that creates this plot and rerun it
```

### Issue: GitHub Clone Missing Files

**Problem**: After cloning, models and visualizations are missing

**Solution**:
```bash
# 1. Ensure Git LFS is installed
git lfs install

# 2. Pull LFS files
git lfs pull

# 3. If files are still missing, they need to be trained/generated
python setup_deployment.py
jupyter notebook GoldSense_Train_Local.ipynb
```

### Issue: Docker Build Fails

**Problem**: Docker build error or container won't start

**Solution**:
```bash
# 1. Rebuild without cache
docker build --no-cache -t gold-price-prediction .

# 2. Check Dockerfile and requirements.txt
# 3. Ensure models directory exists
mkdir -p models results

# 4. Run with verbose logging
docker run -p 5001:5001 gold-price-prediction
```

### Issue: AWS Deployment Fails

**Problem**: EB or ECS deployment errors

**Solution**:
```bash
# 1. Check AWS credentials
aws sts get-caller-identity

# 2. Verify required secrets in GitHub
# Go to: Repository → Settings → Secrets

# 3. Check logs
eb logs  # For Elastic Beanstalk
aws logs tail /ecs/gold-price --follow  # For ECS

# 4. Ensure models are committed
git lfs track "models/*.pkl"
git add models/*.pkl
git commit -m "Add trained models"
git push
```

## 🌐 Technologies Used

### Backend
- **Flask** - Web framework
- **Gunicorn** - WSGI server for production

### Machine Learning
- **Scikit-learn** - ML algorithms and preprocessing
- **XGBoost** - Gradient boosting
- **LightGBM** - Fast gradient boosting
- **TensorFlow/Keras** - Deep learning (LSTM, GRU)

### Data Processing
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **yfinance** - Market data fetching

### Visualization
- **Matplotlib** - Plotting
- **Seaborn** - Statistical visualization

### Deployment
- **Docker** - Containerization
- **AWS Elastic Beanstalk/ECS** - Cloud hosting
- **GitHub Actions** - CI/CD pipeline

## 📈 Future Enhancements

- [ ] Real-time WebSocket updates for live prices
- [ ] Add more economic indicators (inflation, interest rates, GDP)
- [ ] Sentiment analysis from financial news and social media
- [ ] Automated model retraining with new data
- [ ] Multi-currency support (EUR, GBP, JPY)
- [ ] Historical prediction accuracy dashboard
- [ ] Email/SMS alerts for price movements
- [ ] Mobile app (React Native)
- [ ] GraphQL API for flexible queries
- [ ] A/B testing framework for model comparison

## 📝 License

Educational use only - University Machine Learning Project

## 🤝 Contributing

This is a university assignment. For suggestions or issues, please open a GitHub issue.

## 📧 Contact

**Htut Ko Ko**  
GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)  
Email: your.email@university.edu

## 🙏 Acknowledgments

- **Yahoo Finance** for providing free market data API
- **Scikit-learn** and **XGBoost** communities for excellent ML libraries
- **Flask** framework for easy web development
- Course instructors and teaching assistants
- Open-source community for tools and inspiration

---

## 📚 References

1. Gold Market Analysis using Machine Learning
2. Time Series Forecasting with Ensemble Methods
3. Financial Market Prediction using LSTM Networks
4. Feature Engineering for Commodity Price Prediction

---

**⭐ If this project helped you, please star the repository!**

**📧 Questions? Open an issue or contact me directly.**

---

*Last Updated: November 2025*
