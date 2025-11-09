#!/bin/bash
# Quick setup script for cloning and running the project

echo "🚀 Gold Price Prediction - Quick Setup"
echo "======================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Setup
echo "📦 Setting up environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run setup script
echo "🔧 Running setup script..."
python setup_deployment.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Train models (if not already done):"
echo "      jupyter notebook GoldSense_Train_Local.ipynb"
echo ""
echo "   2. Run the webapp:"
echo "      cd webapp && python app.py"
echo ""
echo "   3. Open browser: http://localhost:5001"
echo ""
echo "For deployment to AWS, see: AWS_DEPLOYMENT_GUIDE.md"
