#!/bin/bash
# Git commit and push script for DigitalOcean deployment

echo "🚀 Preparing to commit and push to GitHub..."
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Show current status
echo "📊 Current status:"
git status --short | head -20
echo ""

# Ask for confirmation
read -p "Do you want to commit and push these changes? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted"
    exit 1
fi

echo ""
echo "📝 Adding files to git..."

# Add all changes
git add .

echo "✅ Files staged"
echo ""

# Create commit message
COMMIT_MSG="Clean up project and prepare for DigitalOcean deployment

Changes:
- Removed 50+ redundant documentation files
- Removed backup notebooks and unused scripts
- Updated GitHub Actions for DigitalOcean deployment
- Fixed visualization display issues
- Removed problematic Performance Comparison chart
- Removed CorrelationHeatmap.png and DailyClosePrice.png from UI
- Added comprehensive DigitalOcean deployment guide
- Updated CI/CD workflow for DO App Platform
- Added app.yaml for DigitalOcean configuration
- Streamlined project structure

Ready for deployment with \$200 GitHub Student Pack credit!"

echo "📝 Commit message:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$COMMIT_MSG"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Commit changes
git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
    echo "✅ Changes committed successfully"
else
    echo "❌ Commit failed"
    exit 1
fi

echo ""
echo "🌐 Pushing to GitHub..."
echo ""

# Push to remote
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ Successfully pushed to GitHub!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📋 Next Steps:"
    echo ""
    echo "1. ✅ Code is now on GitHub"
    echo ""
    echo "2. 🎓 Activate GitHub Student Developer Pack:"
    echo "   → https://education.github.com/pack"
    echo ""
    echo "3. 💰 Get DigitalOcean \$200 credit:"
    echo "   → Sign in to DigitalOcean"
    echo "   → Activate Student Pack benefit"
    echo ""
    echo "4. 🚀 Deploy to DigitalOcean:"
    echo "   → Go to: https://cloud.digitalocean.com"
    echo "   → Create → Apps → GitHub"
    echo "   → Select your repository"
    echo "   → Choose Basic plan (\$5/month)"
    echo "   → Click Deploy"
    echo ""
    echo "5. ⚙️ Optional: Setup CI/CD"
    echo "   → Get DO API token: cloud.digitalocean.com/account/api"
    echo "   → Add to GitHub Secrets:"
    echo "     • DIGITALOCEAN_ACCESS_TOKEN"
    echo "     • DO_APP_ID (from your app settings)"
    echo ""
    echo "📚 Documentation:"
    echo "   → READY_TO_DEPLOY.md - Quick start"
    echo "   → DIGITALOCEAN_DEPLOYMENT.md - Full guide"
    echo ""
    echo "💡 With your \$200 credit:"
    echo "   → Basic plan (\$5/mo) = 40 months FREE!"
    echo "   → That's over 3 years of hosting!"
    echo ""
    echo "🎉 Your project is ready for the world!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "❌ Push failed. Please check your connection and try again."
    echo ""
    echo "Common fixes:"
    echo "1. Check internet connection"
    echo "2. Verify remote: git remote -v"
    echo "3. Try: git pull origin main --rebase"
    echo "4. Then run this script again"
    exit 1
fi
