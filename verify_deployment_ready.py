#!/usr/bin/env python3
"""
Pre-deployment verification script
Checks if everything is ready for deployment
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)

def check_item(condition, success_msg, fail_msg):
    if condition:
        print(f"✅ {success_msg}")
        return True
    else:
        print(f"❌ {fail_msg}")
        return False

def main():
    print("\n🔍 Gold Price Prediction - Pre-Deployment Verification\n")
    
    project_root = Path(__file__).parent
    all_checks_passed = True
    
    # Check 1: Project Structure
    print_header("1. Project Structure")
    
    required_dirs = {
        'webapp': 'Web application directory',
        'models': 'Models directory',
        'results': 'Visualizations directory'
    }
    
    for dir_name, description in required_dirs.items():
        dir_path = project_root / dir_name
        passed = check_item(
            dir_path.exists() and dir_path.is_dir(),
            f"{description}: {dir_name}/",
            f"Missing: {dir_name}/ directory"
        )
        all_checks_passed = all_checks_passed and passed
    
    # Check 2: Visualizations
    print_header("2. Visualizations")
    
    results_dir = project_root / 'results'
    if results_dir.exists():
        png_files = list(results_dir.glob('*.png'))
        passed = check_item(
            len(png_files) >= 8,
            f"Found {len(png_files)} visualization files",
            f"Only {len(png_files)} visualizations (need at least 8)"
        )
        all_checks_passed = all_checks_passed and passed
        
        # Check for DailyClosePrice.png specifically
        daily_close = results_dir / 'DailyClosePrice.png'
        passed = check_item(
            daily_close.exists(),
            "DailyClosePrice.png present",
            "DailyClosePrice.png missing"
        )
        all_checks_passed = all_checks_passed and passed
        
        if png_files:
            print(f"\n  Visualizations found:")
            for png in sorted(png_files)[:5]:
                print(f"    • {png.name}")
            if len(png_files) > 5:
                print(f"    ... and {len(png_files) - 5} more")
    
    # Check 3: Models
    print_header("3. Trained Models")
    
    models_dir = project_root / 'models'
    if models_dir.exists():
        required_models = [
            'scaler_X.pkl',
            'scaler_y.pkl',
            'feature_names.pkl'
        ]
        
        model_files = list(models_dir.glob('*.pkl')) + list(models_dir.glob('*.h5'))
        
        if len(model_files) == 0:
            print("❌ No trained models found")
            print("   📝 Run: jupyter notebook GoldSense_Train_Local.ipynb")
            all_checks_passed = False
        else:
            print(f"✅ Found {len(model_files)} model files")
            for model_file in model_files:
                size_mb = model_file.stat().st_size / (1024 * 1024)
                print(f"    • {model_file.name} ({size_mb:.2f} MB)")
    
    # Check 4: Key Files
    print_header("4. Configuration Files")
    
    key_files = {
        'webapp/app.py': 'Flask application',
        'webapp/templates/index.html': 'Web interface',
        'requirements.txt': 'Dependencies',
        'Dockerfile': 'Docker configuration',
        'setup_deployment.py': 'Setup script',
        'AWS_DEPLOYMENT_GUIDE.md': 'AWS guide',
        '.gitignore': 'Git ignore rules',
        '.gitattributes': 'Git LFS config'
    }
    
    for file_path, description in key_files.items():
        full_path = project_root / file_path
        passed = check_item(
            full_path.exists(),
            f"{description}: {file_path}",
            f"Missing: {file_path}"
        )
        all_checks_passed = all_checks_passed and passed
    
    # Check 5: AWS EB Configuration
    print_header("5. AWS Elastic Beanstalk Config")
    
    eb_dir = project_root / 'webapp' / '.ebextensions'
    if eb_dir.exists():
        eb_configs = list(eb_dir.glob('*.config'))
        passed = check_item(
            len(eb_configs) >= 2,
            f"Found {len(eb_configs)} EB configuration files",
            "EB configuration incomplete"
        )
        all_checks_passed = all_checks_passed and passed
    else:
        print("❌ .ebextensions directory missing")
        all_checks_passed = False
    
    # Check 6: GitHub Actions
    print_header("6. CI/CD Configuration")
    
    workflow_file = project_root / '.github' / 'workflows' / 'deploy.yml'
    passed = check_item(
        workflow_file.exists(),
        "GitHub Actions workflow configured",
        "GitHub Actions workflow missing"
    )
    all_checks_passed = all_checks_passed and passed
    
    # Check 7: Dependencies
    print_header("7. Python Dependencies")
    
    req_file = project_root / 'requirements.txt'
    if req_file.exists():
        with open(req_file) as f:
            requirements = f.read()
            
        critical_deps = ['flask', 'pandas', 'numpy', 'scikit-learn', 'yfinance']
        missing = [dep for dep in critical_deps if dep not in requirements.lower()]
        
        if missing:
            print(f"❌ Missing dependencies: {', '.join(missing)}")
            all_checks_passed = False
        else:
            print(f"✅ All critical dependencies present")
    
    # Check 8: Git Status
    print_header("8. Git Repository")
    
    git_dir = project_root / '.git'
    if git_dir.exists():
        print("✅ Git repository initialized")
        
        # Check if there are uncommitted changes
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            
            if result.stdout.strip():
                print("⚠️  You have uncommitted changes")
                print("   Run: git add . && git commit -m 'Your message'")
            else:
                print("✅ All changes committed")
        except:
            print("⚠️  Could not check git status")
    else:
        print("❌ Not a git repository")
        all_checks_passed = False
    
    # Final Summary
    print_header("Summary")
    
    if all_checks_passed:
        print("🎉 All checks passed! You're ready to deploy!")
        print("\n📋 Next steps:")
        print("   1. Commit and push to GitHub: git push origin main")
        print("   2. Follow: DEPLOYMENT_NEXT_STEPS.md")
        print("   3. Deploy to AWS: eb create gold-price-env")
        print("\n💡 Quick start:")
        print("   See: AWS_DEPLOYMENT_GUIDE.md")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n🔧 Quick fixes:")
        print("   • Missing visualizations: python setup_deployment.py")
        print("   • Missing models: Run training notebook")
        print("   • Missing files: Check git status")
        return 1

if __name__ == '__main__':
    sys.exit(main())
