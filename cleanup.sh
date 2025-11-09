#!/bin/bash
# Cleanup script - Remove unnecessary files before deployment

echo "🧹 Cleaning up unnecessary files..."
echo ""

# Remove redundant documentation files
echo "📝 Removing redundant documentation..."
rm -f CLEANUP_COMPLETE.md
rm -f COLAB_SETUP_GUIDE.md
rm -f CRITICAL_FIX_DATA_LEAKAGE.txt
rm -f DEPLOYMENT_GUIDE.md
rm -f DEPLOYMENT_SUMMARY.md
rm -f FINAL_FIX_LAGGED_FEATURES.txt
rm -f FINAL_SUMMARY.txt
rm -f FIXES_APPLIED.md
rm -f FIXES_SUMMARY.md
rm -f GoldPrice_Production_README.md
rm -f IMPROVEMENTS_SUMMARY.txt
rm -f ISSUES_FIXED_COMPLETE.md
rm -f LOCAL_NOTEBOOK_APPROACH.md
rm -f ML_PROJECT_UPGRADE.md
rm -f ML_PROJECT_UPGRADE_FINAL.md
rm -f MODEL_IMPROVEMENTS_FINAL.txt
rm -f NOTEBOOK_CLEANUP_SUMMARY.md
rm -f NOTEBOOK_FIXES_APPLIED.md
rm -f NOTEBOOK_IMPROVEMENTS_COMPLETE.md
rm -f PRACTICAL_IMPROVEMENTS.txt
rm -f PRODUCTION_NOTEBOOK_SUMMARY.txt
rm -f PROJECT_COMPLETE_SUMMARY.txt
rm -f QUICK_COMMANDS.md
rm -f QUICK_FIX_REFERENCE.md
rm -f QUICK_REFERENCE_ML_PROJECT.txt
rm -f QUICK_REFERENCE_OLD.txt
rm -f QUICK_START_GUIDE.md
rm -f QUICK_START_IMPROVED.md
rm -f TIMESERIESPLIT_IMPLEMENTATION.md
rm -f TIME_SERIES_SPLIT_GUIDE.txt
rm -f TRAINING_IMPROVEMENTS.txt
rm -f VISUALIZATION_UPDATE.md
rm -f WHY_NEGATIVE_R2_AND_FIX.md
rm -f ADDITIONAL_FIXES.md

echo "  ✓ Removed 35 redundant documentation files"

# Remove backup/redundant notebooks
echo ""
echo "📓 Removing redundant notebooks..."
rm -f ML_Project_colab_BACKUP.ipynb
rm -f ML_Project_colab_CLEAN.ipynb
rm -f ML_Project_colab.ipynb
rm -f "ML_Project (1).ipynb"

echo "  ✓ Removed 4 redundant notebooks"

# Remove redundant scripts
echo ""
echo "🔧 Removing redundant scripts..."
rm -f enhanced_features.py
rm -f export_models.py
rm -f prepare_deployment.py
rm -f run_webapp.sh
rm -f run_webapp_simple.sh
rm -f train_model.py
rm -f update_data.py

echo "  ✓ Removed 7 redundant scripts"

# Remove old deployment files
echo ""
echo "📦 Removing old deployment configs..."
rm -f app.yaml.bak 2>/dev/null
rm -f .elasticbeanstalk/config.yml 2>/dev/null

echo "  ✓ Cleaned deployment configs"

# Keep only essential files
echo ""
echo "✅ Keeping essential files:"
echo "  📄 README.md - Main documentation"
echo "  📄 DIGITALOCEAN_DEPLOYMENT.md - Deployment guide"
echo "  📄 AWS_DEPLOYMENT_GUIDE.md - Alternative deployment"
echo "  📄 DEPLOYMENT_NEXT_STEPS.md - Deployment steps"
echo "  📄 READY_TO_DEPLOY.md - Quick start"
echo "  📄 FINAL_CHANGES_DO.md - Recent changes"
echo ""
echo "  📓 GoldSense_Train_Local.ipynb - Training notebook"
echo "  📓 GoldSense_Train_Combined_colab.ipynb - Colab version"
echo "  📓 ML_Project.ipynb - Original project"
echo "  📓 Data_Cleaning_Feature_Engineering.ipynb - Data prep"
echo ""
echo "  🔧 setup_deployment.py - Setup script"
echo "  🔧 verify_deployment_ready.py - Verification"
echo "  🔧 quick_setup.sh - Quick setup"
echo "  🔧 test_webapp.py - Testing"

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Summary:"
echo "  • Removed: ~50 redundant files"
echo "  • Kept: ~15 essential files"
echo "  • Project is now clean and ready for deployment"
