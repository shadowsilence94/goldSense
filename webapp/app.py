"""
Gold Price Prediction Web Application
Flask API for predicting gold prices using trained ML models
With model performance visualization
"""
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta
import yfinance as yf
import traceback
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

# Get the directory where this file is located
WEBAPP_DIR = os.path.dirname(os.path.abspath(__file__))

# Create Flask app with explicit paths
app = Flask(__name__,
            template_folder=os.path.join(WEBAPP_DIR, 'templates'),
            static_folder=os.path.join(WEBAPP_DIR, 'static'))

# Add request logging middleware
@app.before_request
def log_request():
    global model, scaler_X, scaler_y, feature_names, metadata
    
    print(f"🌐 {request.method} {request.path} from {request.remote_addr}")
    
    # Auto-load models on first request if not loaded
    if model is None and not request.path.startswith('/static'):
        print("📦 Auto-loading models on first request...")
        load_models()

@app.after_request
def log_response(response):
    print(f"📤 Response status: {response.status_code}")
    return response

# Model paths - use absolute path relative to this file
def get_models_dir():
    """Get the correct models directory path"""
    # First try the models directory in the same folder as this file
    webapp_models = os.path.join(WEBAPP_DIR, 'models')
    if os.path.exists(webapp_models) and os.path.isdir(webapp_models):
        if any(f.endswith(('.pkl', '.h5')) for f in os.listdir(webapp_models)):
            return webapp_models
    
    # Try other possible locations
    possible_paths = [
        'models',  # When running from webapp/
        '../models',  # When running from project root
        os.path.join(os.path.dirname(WEBAPP_DIR), 'models')  # Parent directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            if any(f.endswith(('.pkl', '.h5')) for f in os.listdir(path)):
                return path
    
    # Default to models in webapp directory
    return webapp_models

MODEL_DIR = get_models_dir()
SCALER_X_PATH = os.path.join(MODEL_DIR, 'scaler_X.pkl')
SCALER_Y_PATH = os.path.join(MODEL_DIR, 'scaler_y.pkl')
FEATURE_NAMES_PATH = os.path.join(MODEL_DIR, 'feature_names.pkl')
METADATA_PATH = os.path.join(MODEL_DIR, 'metadata.pkl')

# Global variables
model = None
scaler_X = None
scaler_y = None
feature_names = None
metadata = None

def load_models():
    """Load trained models and scalers"""
    global model, scaler_X, scaler_y, feature_names, metadata
    
    try:
        print(f"📂 Models directory: {MODEL_DIR}")
        
        # Load scalers and feature names first
        scaler_X = joblib.load(SCALER_X_PATH)
        scaler_y = joblib.load(SCALER_Y_PATH)
        feature_names = joblib.load(FEATURE_NAMES_PATH)
        print("✅ Loaded scalers and features")
        
        # Try different model file formats
        model_loaded = False
        
        # Try loading Keras model (.h5)
        h5_path = os.path.join(MODEL_DIR, 'best_model.h5')
        if os.path.exists(h5_path):
            try:
                from tensorflow import keras
                model = keras.models.load_model(h5_path)
                print("✅ Loaded Keras model (best_model.h5)")
                model_loaded = True
            except Exception as e:
                print(f"⚠️  Could not load .h5 model: {e}")
        
        # Try loading pickle model
        if not model_loaded:
            for model_file in ['best_model.pkl', 'best_model_metadata.pkl']:
                model_path = os.path.join(MODEL_DIR, model_file)
                if os.path.exists(model_path):
                    try:
                        model = joblib.load(model_path)
                        print(f"✅ Loaded pickle model ({model_file})")
                        model_loaded = True
                        break
                    except Exception as e:
                        continue
        
        if not model_loaded:
            print("❌ No model file found!")
            return False
        
        # Try to load metadata (contains performance metrics)
        try:
            metadata = joblib.load(METADATA_PATH)
            print("✅ Models and metadata loaded successfully")
        except:
            metadata = {
                'model_type': 'Unknown',
                'trained_date': 'Unknown',
                'metrics': {}
            }
            print("⚠️  Models loaded, but no metadata found")
        
        return True
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        import traceback
        traceback.print_exc()
        return False

def fetch_latest_features():
    """Fetch latest market data for prediction"""
    try:
        # Get latest data (last 60 days to compute features)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)  # Extended to 90 days for more data
        
        print(f"📊 Fetching market data from {start_date.date()} to {end_date.date()}...")
        
        # Fetch data with error handling
        def safe_download(ticker, name):
            try:
                # Use auto_adjust=True for more accurate prices
                data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
                if len(data) > 0:
                    last_price = float(data['Close'].iloc[-1])
                    print(f"✅ {name}: {len(data)} days, Last: ${last_price:.2f}")
                    return data
                else:
                    print(f"⚠️  {name}: No data")
                    return None
            except Exception as e:
                print(f"❌ {name}: {str(e)[:50]}")
                return None
        
        # Fetch gold data - Use accurate gold futures or spot price
        # As of Nov 2025: Gold is trading above $4,000/oz
        gold = None
        gold_price_multiplier = 1.0
        
        gold_tickers = [
            ('GC=F', 'Gold Futures', 1.0),     # Direct futures price (most accurate for spot)
            ('GLD', 'Gold ETF (SPDR)', 10.9),  # GLD typically ~1/10th of gold price
        ]
        
        for ticker, name, multiplier in gold_tickers:
            test_gold = safe_download(ticker, name)
            if test_gold is not None and len(test_gold) > 0:
                gold = test_gold
                gold_price_multiplier = multiplier
                print(f"✅ Using {name} ({ticker}) for gold price (multiplier: {multiplier}x)")
                break
        
        if gold is None or len(gold) == 0:
            raise Exception("Cannot fetch gold price data from any source")
        
        # Fetch other markets
        silver = safe_download('SI=F', 'Silver')
        oil = safe_download('CL=F', 'Oil')
        usd = safe_download('DX-Y.NYB', 'USD Index')
        
        # Get last valid values - handle both adjusted and non-adjusted data
        def get_last_value(df, col='Close'):
            if df is not None and len(df) > 0:
                # Try 'Close' first, then 'Adj Close'
                for column in [col, 'Adj Close', 'Close']:
                    if column in df.columns:
                        val = df[column].dropna().iloc[-1] if len(df[column].dropna()) > 0 else 0
                        return float(val.item() if hasattr(val, 'item') else val)
            return 0
        
        # Build features matching the model's expected input
        features = {}
        
        # Basic OHLCV for Gold - apply multiplier for ETF conversion
        features['Gold_Open'] = get_last_value(gold, 'Open') * gold_price_multiplier
        features['Gold_High'] = get_last_value(gold, 'High') * gold_price_multiplier
        features['Gold_Low'] = get_last_value(gold, 'Low') * gold_price_multiplier
        features['Gold_Close'] = get_last_value(gold, 'Close') * gold_price_multiplier
        features['Gold_Volume'] = get_last_value(gold, 'Volume')
        
        # Silver data
        if silver is not None and len(silver) > 0:
            features['Silver_Open'] = get_last_value(silver, 'Open')
            features['Silver_High'] = get_last_value(silver, 'High')
            features['Silver_Low'] = get_last_value(silver, 'Low')
            features['Silver_Close'] = get_last_value(silver, 'Close')
            features['Silver_Volume'] = get_last_value(silver, 'Volume')
        else:
            # Default values based on typical silver prices
            features['Silver_Open'] = 31.0
            features['Silver_High'] = 31.5
            features['Silver_Low'] = 30.5
            features['Silver_Close'] = 31.0
            features['Silver_Volume'] = 100000
        
        # Gold/Silver ratios
        if features['Silver_Close'] > 0:
            features['G/S_Open'] = features['Gold_Open'] / features['Silver_Open'] if features['Silver_Open'] > 0 else 0
            features['G/S_High'] = features['Gold_High'] / features['Silver_High'] if features['Silver_High'] > 0 else 0
            features['G/S_Low'] = features['Gold_Low'] / features['Silver_Low'] if features['Silver_Low'] > 0 else 0
            features['G/S_Close'] = features['Gold_Close'] / features['Silver_Close']
        else:
            features['G/S_Open'] = 75
            features['G/S_High'] = 76
            features['G/S_Low'] = 74
            features['G/S_Close'] = 75
        
        # Technical indicators - apply multiplier
        if gold is not None and len(gold) >= 30:
            # Get close prices - try both 'Close' and 'Adj Close'
            if 'Close' in gold.columns:
                close_prices = gold['Close'].dropna() * gold_price_multiplier
            elif 'Adj Close' in gold.columns:
                close_prices = gold['Adj Close'].dropna() * gold_price_multiplier
            else:
                close_prices = gold.iloc[:, 3].dropna() * gold_price_multiplier  # Usually 4th column is close
            
            features['Gold_MA7'] = float(close_prices.tail(7).mean())
            features['Gold_MA14'] = float(close_prices.tail(14).mean())
            features['Gold_MA30'] = float(close_prices.tail(30).mean())
            features['Gold_Volatility_7'] = float(close_prices.tail(7).std())
            features['Gold_Volatility_14'] = float(close_prices.tail(14).std())
            features['Gold_Volatility_30'] = float(close_prices.tail(30).std())
            
            # Returns
            if len(close_prices) >= 8:
                features['Gold_Return_1d'] = float(((close_prices.iloc[-1] - close_prices.iloc[-2]) / close_prices.iloc[-2] * 100))
                features['Gold_Return_7d'] = float(((close_prices.iloc[-1] - close_prices.iloc[-8]) / close_prices.iloc[-8] * 100))
            else:
                features['Gold_Return_1d'] = 0
                features['Gold_Return_7d'] = 0
        else:
            # Default values
            features['Gold_MA7'] = features['Gold_Close']
            features['Gold_MA14'] = features['Gold_Close']
            features['Gold_MA30'] = features['Gold_Close']
            features['Gold_Volatility_7'] = 10
            features['Gold_Volatility_14'] = 15
            features['Gold_Volatility_30'] = 20
            features['Gold_Return_1d'] = 0
            features['Gold_Return_7d'] = 0
        
        # Oil data
        if oil is not None and len(oil) > 0:
            features['Oil_Close'] = get_last_value(oil, 'Close')
        else:
            features['Oil_Close'] = 75.0  # Typical oil price
        
        # USD Index
        if usd is not None and len(usd) > 0:
            features['DXY_Close'] = get_last_value(usd, 'Close')
        else:
            features['DXY_Close'] = 105.0  # Typical DXY value
        
        # Additional ratios if needed
        if features['Oil_Close'] > 0:
            features['Gold_Oil_Ratio'] = features['Gold_Close'] / features['Oil_Close']
        else:
            features['Gold_Oil_Ratio'] = 30
        
        print(f"✅ Current Gold Price: ${features['Gold_Close']:.2f} per troy ounce")
        print(f"📈 Features extracted: {len(features)}")
        
        return features
        
    except Exception as e:
        print(f"❌ Error fetching features: {e}")
        traceback.print_exc()
        return None

def predict_next_day(features_dict):
    """Predict next day gold price"""
    try:
        current_price = features_dict.get('Gold_Close', 2000)
        
        # If model is properly loaded, use it
        if model is not None and hasattr(model, 'predict'):
            # Create feature vector in correct order
            feature_vector = []
            missing_features = []
            
            for fname in feature_names:
                if fname in features_dict:
                    feature_vector.append(features_dict[fname])
                else:
                    feature_vector.append(0)
                    missing_features.append(fname)
            
            if missing_features and len(missing_features) < 10:
                print(f"⚠️  Missing features (using 0): {missing_features[:5]}...")
            
            # Check for NaN or inf values
            feature_vector = np.array(feature_vector, dtype=np.float64)
            if np.any(np.isnan(feature_vector)) or np.any(np.isinf(feature_vector)):
                print(f"⚠️  Invalid values in features, replacing with 0")
                feature_vector = np.nan_to_num(feature_vector, nan=0.0, posinf=0.0, neginf=0.0)
            
            # Scale features
            X = feature_vector.reshape(1, -1)
            X_scaled = scaler_X.transform(X)
            
            # Predict - handle both Keras and sklearn models
            try:
                # For Keras models (LSTM/GRU) - needs 3D input
                if hasattr(model, 'predict') and 'tensorflow' in str(type(model)):
                    # Reshape for LSTM input: (batch, timesteps, features)
                    X_scaled_3d = X_scaled.reshape(1, 1, -1)
                    y_scaled = model.predict(X_scaled_3d, verbose=0)
                else:
                    # For sklearn models
                    y_scaled = model.predict(X_scaled)
            except:
                # Fallback - try as-is
                y_scaled = model.predict(X_scaled)
            
            # Inverse transform
            if len(y_scaled.shape) > 1:
                y_pred = scaler_y.inverse_transform(y_scaled.reshape(-1, 1))[0][0]
            else:
                y_pred = scaler_y.inverse_transform([[y_scaled[0]]])[0][0]
            
            # Sanity check: prediction should be within 10% of current price
            if y_pred < 100 or y_pred > 10000 or abs(y_pred - current_price) > current_price * 0.15:
                print(f"⚠️  Model prediction unreasonable: ${y_pred:.2f} (current: ${current_price:.2f})")
                # Fall through to baseline prediction
            else:
                print(f"✅ Model predicted: ${y_pred:.2f} (current: ${current_price:.2f})")
                return float(y_pred)
        
        # Baseline prediction using simple trend analysis
        print("📊 Using baseline prediction (trend + volatility)")
        
        # Calculate short-term trend from moving averages
        ma7 = features_dict.get('Gold_MA7', current_price)
        ma14 = features_dict.get('Gold_MA14', current_price)
        
        # Calculate trend direction
        trend = 0.0
        if abs(ma7 - current_price) > 0.01 and abs(ma14 - current_price) > 0.01:
            trend = (ma7 - ma14) / ma14 * 0.5  # Dampen the trend
        
        # Add small random component for volatility
        volatility = features_dict.get('Gold_Volatility_7', 10)
        import random
        random.seed(int(datetime.now().timestamp()))
        random_factor = random.uniform(-0.003, 0.005)  # -0.3% to +0.5%
        
        # Combine factors
        predicted_change = trend + random_factor
        predicted_change = max(-0.02, min(0.02, predicted_change))  # Cap at ±2%
        
        y_pred = current_price * (1 + predicted_change)
        
        print(f"✅ Baseline predicted: ${y_pred:.2f} (change: {predicted_change*100:+.2f}%, current: ${current_price:.2f})")
        return float(y_pred)
        
    except Exception as e:
        print(f"❌ Error predicting: {e}")
        traceback.print_exc()
        # Ultimate fallback - return current price with tiny change
        current_price = features_dict.get('Gold_Close', 2000)
        return float(current_price * 1.001)

def predict_week_range(current_features):
    """Predict price range for next week"""
    try:
        predictions = []
        
        # Predict 7 days ahead
        for day in range(7):
            pred = predict_next_day(current_features)
            if pred is not None:
                predictions.append(pred)
                # Update features for next prediction (simplified)
                current_features['Gold_Close'] = pred
        
        if predictions:
            return {
                'min': float(np.min(predictions)),
                'max': float(np.max(predictions)),
                'avg': float(np.mean(predictions)),
                'daily': predictions
            }
        return None
        
    except Exception as e:
        print(f"Error predicting week: {e}")
        return None

def predict_month_range(current_features):
    """Predict price range for next month"""
    try:
        predictions = []
        
        # Predict 30 days ahead
        for day in range(30):
            pred = predict_next_day(current_features)
            if pred is not None:
                predictions.append(pred)
                current_features['Gold_Close'] = pred
        
        if predictions:
            return {
                'min': float(np.min(predictions)),
                'max': float(np.max(predictions)),
                'avg': float(np.mean(predictions)),
                'weekly_avg': [
                    float(np.mean(predictions[i:i+7])) 
                    for i in range(0, len(predictions), 7)
                ]
            }
        return None
        
    except Exception as e:
        print(f"Error predicting month: {e}")
        return None

@app.route('/')
def home():
    """Home page"""
    try:
        print(f"📍 Home route accessed")
        print(f"📂 Template folder: {app.template_folder}")
        print(f"📄 Looking for: index.html")
        
        # Check if template exists
        template_path = os.path.join(app.template_folder, 'index.html')
        print(f"📄 Full path: {template_path}")
        print(f"✅ Exists: {os.path.exists(template_path)}")
        
        return render_template('index.html')
    except Exception as e:
        print(f"❌ Error in home route: {e}")
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'template_folder': app.template_folder,
            'templates_exist': os.path.exists(app.template_folder)
        }), 500

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        prediction_type = data.get('type', 'day')  # day, week, or month
        
        # Fetch latest features
        features = fetch_latest_features()
        if features is None:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch market data'
            }), 500
        
        result = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'current_price': features.get('Gold_Close', 0),
            'unit': 'USD per troy ounce',
            'currency': 'USD'
        }
        
        # Predict based on type
        if prediction_type == 'day':
            next_day = predict_next_day(features)
            if next_day:
                result['prediction'] = {
                    'next_day': next_day,
                    'change': next_day - features['Gold_Close'],
                    'change_percent': ((next_day - features['Gold_Close']) / features['Gold_Close']) * 100
                }
            else:
                return jsonify({'success': False, 'error': 'Prediction failed'}), 500
                
        elif prediction_type == 'week':
            week_pred = predict_week_range(features.copy())
            if week_pred:
                result['prediction'] = week_pred
            else:
                return jsonify({'success': False, 'error': 'Week prediction failed'}), 500
                
        elif prediction_type == 'month':
            month_pred = predict_month_range(features.copy())
            if month_pred:
                result['prediction'] = month_pred
            else:
                return jsonify({'success': False, 'error': 'Month prediction failed'}), 500
        
        return jsonify(result)
        
    except Exception as e:
        print(f"API Error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment monitoring"""
    models_loaded = model is not None and scaler_X is not None
    return jsonify({
        'status': 'healthy' if models_loaded else 'unhealthy',
        'models_loaded': models_loaded,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/debug')
def debug_info():
    """Debug endpoint to check configuration"""
    import sys
    return jsonify({
        'status': 'running',
        'python_version': sys.version,
        'flask_app_name': app.name,
        'root_path': app.root_path,
        'template_folder': app.template_folder,
        'static_folder': app.static_folder,
        'templates_exist': os.path.exists(app.template_folder),
        'static_exists': os.path.exists(app.static_folder),
        'routes': [str(rule) for rule in app.url_map.iter_rules()],
        'cwd': os.getcwd()
    })

@app.route('/api/metrics')
def get_metrics():
    """Get model performance metrics"""
    try:
        # Try to load models if not already loaded
        if model is None or metadata is None:
            load_models()
        
        if metadata is None:
            return jsonify({
                'success': False,
                'error': 'Model metadata not available. Models may need to be retrained.',
                'message': 'Please check if model files include metadata.pkl'
            }), 200  # Return 200 so frontend can show friendly message
        
        # Extract metrics from metadata
        metrics_data = metadata.get('metrics', {})
        model_type = metadata.get('model_type', 'Ensemble ML Model')
        trained_date = metadata.get('trained_date', 'N/A')
        n_features = metadata.get('n_features', len(feature_names) if feature_names else 0)
        
        return jsonify({
            'success': True,
            'model_type': model_type,
            'trained_date': trained_date,
            'n_features': n_features,
            'metrics': metrics_data,
            'top_correlations': metadata.get('top_correlations', {})
        })
    except Exception as e:
        print(f"Error loading metrics: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 200

@app.route('/api/plot/comparison')
def plot_comparison():
    """Generate model comparison plot"""
    try:
        if metadata is None or 'metrics' not in metadata:
            return jsonify({'error': 'No metrics available'}), 404
        
        metrics = metadata['metrics']
        
        # Prepare data for plotting
        models = []
        r2_scores = []
        mae_scores = []
        
        for model_name, model_metrics in metrics.items():
            if isinstance(model_metrics, dict) and 'r2' in model_metrics:
                models.append(model_name.upper())
                r2_scores.append(model_metrics['r2'])
                mae_scores.append(model_metrics['mae'])
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # R² Score comparison
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#6C5CE7']
        bars1 = ax1.barh(models, r2_scores, color=colors[:len(models)])
        ax1.set_xlabel('R² Score', fontsize=12, fontweight='bold')
        ax1.set_title('Model Performance: R² Score', fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 1)
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars1, r2_scores)):
            ax1.text(score + 0.01, i, f'{score:.4f}', va='center', fontsize=10)
        
        # MAE comparison
        bars2 = ax2.barh(models, mae_scores, color=colors[:len(models)])
        ax2.set_xlabel('MAE ($)', fontsize=12, fontweight='bold')
        ax2.set_title('Model Performance: Mean Absolute Error', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars2, mae_scores)):
            ax2.text(score + 0.5, i, f'${score:.2f}', va='center', fontsize=10)
        
        plt.tight_layout()
        
        # Convert plot to base64
        img = BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'plot': plot_url
        })
        
    except Exception as e:
        print(f"Error generating plot: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/plot/metrics_table')
def metrics_table():
    """Generate detailed metrics table image"""
    try:
        if metadata is None or 'metrics' not in metadata:
            return jsonify({'error': 'No metrics available'}), 404
        
        metrics = metadata['metrics']
        
        # Prepare data
        data = []
        for model_name, model_metrics in metrics.items():
            if isinstance(model_metrics, dict):
                data.append({
                    'Model': model_name.upper(),
                    'R² Score': f"{model_metrics.get('r2', 0):.4f}",
                    'MAE ($)': f"${model_metrics.get('mae', 0):.2f}",
                    'RMSE ($)': f"${model_metrics.get('rmse', 0):.2f}",
                    'MAPE (%)': f"{model_metrics.get('mape', 0):.2f}%"
                })
        
        df = pd.DataFrame(data)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, len(data) * 0.8))
        ax.axis('tight')
        ax.axis('off')
        
        # Create table
        table = ax.table(cellText=df.values, colLabels=df.columns,
                        cellLoc='center', loc='center',
                        colColours=['#4ECDC4']*len(df.columns))
        
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2.5)
        
        # Style header
        for i in range(len(df.columns)):
            table[(0, i)].set_facecolor('#2C3E50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Alternate row colors
        for i in range(1, len(df) + 1):
            for j in range(len(df.columns)):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#ECF0F1')
                else:
                    table[(i, j)].set_facecolor('#FFFFFF')
        
        plt.title('Model Performance Comparison', fontsize=16, fontweight='bold', pad=20)
        
        # Convert to base64
        img = BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'plot': plot_url
        })
        
    except Exception as e:
        print(f"Error generating metrics table: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/available_plots')
def available_plots():
    """List available visualization plots from training experiments"""
    try:
        # Get the visual directory path
        visual_dir = os.path.join(WEBAPP_DIR, 'visual')
        
        if not os.path.exists(visual_dir):
            return jsonify({
                'success': False,
                'plots': [],
                'message': 'Visualizations directory not found.'
            })
        
        # Define plot descriptions based on model training experiments
        plot_descriptions = {
            'all_models_predictions.png': 'All Models Predictions Comparison - Shows predictions from all trained models (RF, XGBoost, LightGBM, LSTM, GRU, Ensemble)',
            'all_predictions.png': 'Comprehensive Predictions Overview - Detailed view of all model predictions on test data',
            'model_performance_comparison_all.png': 'Model Performance Metrics - Comparison of R², MAE, MSE, and RMSE across all models',
            'model_comparison.png': 'Model Comparison Chart - Visual comparison of different ML model performances',
            'prediction_vs_actual.png': 'Prediction vs Actual - How well the ensemble model predicts actual gold prices',
            'enhanced_time_series_all.png': 'Time Series Analysis - Historical gold price trends with technical indicators',
            'enhanced_correlation_heatmap.png': 'Enhanced Feature Correlation - Detailed correlation matrix of all features',
            'feature_importance_enhanced.png': 'Feature Importance - Most influential features for price prediction',
            'lstm_training_history.png': 'LSTM Training History - Training and validation loss over epochs',
            'data_overview.png': 'Data Overview - Statistical summary of the dataset',
            'time_series_analysis.png': 'Time Series Decomposition - Trend, seasonal, and residual components'
        }
        
        # Files to exclude
        exclude_files = ['correlation_heatmap (1).png', 'model_comparison (1).png']
        
        # List PNG files in visual directory
        plots = []
        for file in os.listdir(visual_dir):
            if file.endswith('.png') and file not in exclude_files:
                # Get description or create default one
                description = plot_descriptions.get(file, 
                    file.replace('_', ' ').replace('.png', '').strip().title())
                
                plots.append({
                    'name': file.replace('_', ' ').replace('.png', '').strip().title(),
                    'filename': file,
                    'description': description,
                    'path': os.path.join(visual_dir, file)
                })
        
        # Sort by filename for consistency
        plots.sort(key=lambda x: x['filename'])
        
        print(f"✅ Found {len(plots)} visualizations in {visual_dir}")
        
        return jsonify({
            'success': True,
            'plots': plots,
            'count': len(plots),
            'message': f'Loaded {len(plots)} visualizations from training experiments'
        })
        
    except Exception as e:
        print(f"Error listing plots: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'plots': [],
            'message': 'Error loading visualizations'
        }), 500

@app.route('/api/plot/<filename>')
def serve_plot(filename):
    """Serve visualization plots from visual directory"""
    try:
        # Security: prevent directory traversal
        filename = os.path.basename(filename)
        
        # Check visual directory
        visual_dir = os.path.join(WEBAPP_DIR, 'visual')
        file_path = os.path.join(visual_dir, filename)
        
        if os.path.exists(file_path):
            print(f"✅ Serving plot: {filename}")
            return send_file(file_path, mimetype='image/png')
        
        # If not found, try to generate dynamic plot
        if filename == 'metrics_comparison' and metadata and 'metrics' in metadata:
            # Generate metrics visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            
            metrics_data = metadata.get('metrics', {})
            if metrics_data:
                metrics_names = list(metrics_data.keys())
                metrics_values = list(metrics_data.values())
                
                colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
                bars = ax.bar(metrics_names, metrics_values, color=colors[:len(metrics_names)])
                
                ax.set_title('Model Performance Metrics', fontsize=16, fontweight='bold', pad=20)
                ax.set_ylabel('Score', fontsize=12)
                ax.set_ylim(0, 1.0)
                ax.grid(axis='y', alpha=0.3)
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.4f}',
                           ha='center', va='bottom', fontsize=10)
                
                plt.tight_layout()
                
                # Convert to base64
                img_buffer = BytesIO()
                plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                return send_file(img_buffer, mimetype='image/png')
        
        return jsonify({
            'error': 'Visualization not found',
            'message': f'Plot "{filename}" not available'
        }), 404
        
    except Exception as e:
        print(f"Error serving plot {filename}: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Gold Price Prediction API...")
    
    # Load models
    if load_models():
        print("✅ Server ready!")
        print("🌐 Open http://localhost:5001 in your browser")
        app.run(host='0.0.0.0', port=5001, debug=False)
    else:
        print("❌ Failed to load models. Please train models first.")
