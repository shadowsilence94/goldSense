# Next Steps - Deployment Guide

## ✅ All Fixes Complete!

Your project is now ready to push to GitHub and deploy to AWS. Follow these steps:

---

## Step 1: Commit Changes to Git

```bash
# Check current status
git status

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Fix visualizations and add AWS deployment support

- Fixed .gitignore to allow PNG visualizations
- Added setup_deployment.py for automated setup
- Created comprehensive AWS deployment guide
- Updated GitHub Actions for AWS EB/ECS deployment
- Enhanced webapp to handle multiple visualization paths
- Added troubleshooting documentation
- All 11 visualizations now tracked in results/
"

# Push to GitHub
git push origin main
```

---

## Step 2: Verify on GitHub

After pushing, check on GitHub:

✅ Visit: https://github.com/YOUR_USERNAME/ML_gold_preditct_project
✅ Check: results/ folder has all PNG files
✅ Check: README.md displays correctly
✅ Check: AWS_DEPLOYMENT_GUIDE.md is accessible

---

## Step 3: Setup GitHub Secrets for AWS

Before deploying, configure these secrets in your GitHub repository:

### Navigate to:
Repository → Settings → Secrets and variables → Actions → New repository secret

### Add These Secrets:

**Required for Elastic Beanstalk Deployment:**
```
Name: AWS_ACCESS_KEY_ID
Value: Your AWS Access Key

Name: AWS_SECRET_ACCESS_KEY
Value: Your AWS Secret Key

Name: AWS_REGION
Value: us-east-1 (or your preferred region)

Name: EB_APPLICATION_NAME
Value: gold-price-prediction

Name: EB_ENVIRONMENT_NAME
Value: gold-price-env
```

**Optional - For ECS Deployment:**
```
Name: ECR_REPOSITORY
Value: gold-price-prediction

Name: ECS_CLUSTER
Value: gold-price-cluster

Name: ECS_SERVICE
Value: gold-price-service
```

### How to Get AWS Keys:

1. Login to AWS Console
2. Go to: IAM → Users → Your User → Security Credentials
3. Create Access Key → CLI
4. Copy Access Key ID and Secret Access Key
5. **IMPORTANT**: Save these securely, you can't view secret key again

---

## Step 4: Test Locally Before Deploying

```bash
# Ensure you're in project root
cd /path/to/ML_gold_preditct_project

# Run setup
python setup_deployment.py

# Start webapp
cd webapp
python app.py

# Open browser: http://localhost:5001

# Test all features:
# ✅ Predictions tab works
# ✅ Model Performance tab shows metrics
# ✅ Visualizations tab shows all 11 images
# ✅ DailyClosePrice.png displays
```

---

## Step 5: Deploy to AWS (Choose One Option)

### Option A: AWS Elastic Beanstalk (Recommended - Easiest)

```bash
# Install EB CLI
pip install awsebcli

# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Key, Region (us-east-1), Format (json)

# Navigate to webapp folder
cd webapp

# Initialize EB
eb init -p python-3.9 gold-price-prediction --region us-east-1

# Create environment and deploy
eb create gold-price-env

# Wait 5-10 minutes for deployment...

# Open your deployed app
eb open

# Check logs if needed
eb logs

# Get app URL
eb status
```

### Option B: Deploy via GitHub Actions

```bash
# Just push to main branch
git push origin main

# GitHub Actions will automatically:
# 1. Run tests
# 2. Build application
# 3. Deploy to AWS

# Check progress:
# Go to: GitHub → Actions tab
# Monitor the deployment workflow
```

### Option C: AWS ECS with Fargate

See detailed steps in: [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md#option-2-aws-ecs-with-fargate)

### Option D: AWS EC2 with Docker

See detailed steps in: [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md#option-3-aws-ec2-with-docker)

---

## Step 6: Verify Deployment

### Once deployed, test these endpoints:

```bash
# Replace YOUR-APP-URL with your actual URL

# 1. Health check
curl https://YOUR-APP-URL/health

# Should return:
# {"status":"healthy","models_loaded":true,"timestamp":"..."}

# 2. Test prediction API
curl -X POST https://YOUR-APP-URL/api/predict \
  -H "Content-Type: application/json" \
  -d '{"type":"day"}'

# 3. Check visualizations
curl https://YOUR-APP-URL/api/available_plots

# 4. View in browser
# Open: https://YOUR-APP-URL
```

### Checklist:
- [ ] Website loads
- [ ] All three tabs work (Predictions, Performance, Visualizations)
- [ ] DailyClosePrice.png shows in Visualizations tab
- [ ] Predictions work (Next Day, Week, Month)
- [ ] Model Performance metrics display
- [ ] No errors in browser console

---

## Step 7: Update README with Your Deployment URL

```bash
# Edit README.md
# Find line 8:
**Web App**: https://your-app.elasticbeanstalk.com

# Replace with your actual URL:
**Web App**: https://gold-price-env.us-east-1.elasticbeanstalk.com

# Commit and push
git add README.md
git commit -m "Update README with deployment URL"
git push origin main
```

---

## Common Deployment Issues & Solutions

### Issue 1: Models Not Loading in Deployment

**Solution:**
```bash
# Ensure models are committed
git add models/*.pkl models/*.h5
git commit -m "Add trained models"
git push

# If models are large (>100MB), use Git LFS
git lfs install
git lfs track "models/*.pkl"
git lfs track "models/*.h5"
git add .gitattributes
git commit -m "Setup Git LFS for models"
git add models/*.pkl models/*.h5
git commit -m "Add models via LFS"
git push
```

### Issue 2: Visualizations Not Showing

**Solution:**
```bash
# Ensure all PNGs are committed
git add results/*.png
git commit -m "Add visualizations"
git push

# Redeploy
eb deploy  # For Elastic Beanstalk
# Or push to trigger GitHub Actions
```

### Issue 3: EB Deploy Fails

**Solution:**
```bash
# Check logs
eb logs

# Common fixes:
# 1. Memory issue - upgrade instance type
eb scale 1 -i t3.medium

# 2. Dependencies issue - verify requirements.txt
cd webapp
pip install -r requirements.txt

# 3. Timeout - increase timeout in .ebextensions
# Edit: webapp/.ebextensions/01_python.config
# Add command timeout settings
```

### Issue 4: GitHub Actions Fails

**Solution:**
1. Check Actions tab for error details
2. Verify GitHub Secrets are set correctly
3. Check if AWS credentials are valid:
   ```bash
   aws sts get-caller-identity
   ```
4. Ensure models directory is not empty
5. Check workflow logs for specific errors

---

## Monitoring Your Deployment

### AWS CloudWatch Logs

```bash
# For Elastic Beanstalk
eb logs --stream

# For ECS
aws logs tail /ecs/gold-price --follow

# For EC2
ssh -i your-key.pem ubuntu@your-ip
docker logs -f gold-app
```

### Set Up Alarms (Optional)

1. Go to: AWS Console → CloudWatch → Alarms
2. Create alarm for:
   - High CPU usage (> 80%)
   - High memory usage (> 80%)
   - HTTP 5xx errors
   - Health check failures

---

## Scaling Your Application

### Elastic Beanstalk Auto Scaling

```bash
# Scale to 2-4 instances
eb scale 4

# Or configure in console:
# EB Console → Configuration → Capacity
# Set: Min=2, Max=4
```

### Manual Scaling for ECS

```bash
aws ecs update-service \
  --cluster gold-price-cluster \
  --service gold-price-service \
  --desired-count 3
```

---

## Cost Management

### Current Setup Costs (Estimates):

**Elastic Beanstalk:**
- t3.medium EC2: ~$30/month
- Application Load Balancer: ~$20/month
- **Total: ~$50/month**

**Optimization Tips:**
- Use t3.micro for testing: ~$8/month
- Enable auto-scaling to save costs during low traffic
- Use Savings Plans for long-term savings
- Set up AWS Budget alerts

---

## Update Your Application

### For Future Updates:

```bash
# 1. Make changes locally
# 2. Test locally
cd webapp && python app.py

# 3. Commit and push
git add .
git commit -m "Description of changes"
git push origin main

# 4. Deploy
eb deploy  # For EB

# Or just push to main for automatic GitHub Actions deployment
```

---

## Support & Resources

### Documentation:
- [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md) - Full AWS guide
- [README.md](README.md) - Project overview
- [FIXES_SUMMARY.md](FIXES_SUMMARY.md) - What was fixed

### AWS Resources:
- [Elastic Beanstalk Docs](https://docs.aws.amazon.com/elasticbeanstalk/)
- [ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS CLI Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/index.html)

### Get Help:
1. Check troubleshooting section in README.md
2. Review AWS CloudWatch logs
3. Check GitHub Issues tab
4. AWS Support (if you have support plan)

---

## Success Checklist

Before considering deployment complete:

- [ ] All code committed and pushed to GitHub
- [ ] All 11 visualizations show on GitHub in results/
- [ ] GitHub Actions CI/CD configured with secrets
- [ ] AWS credentials configured
- [ ] Application deployed to AWS
- [ ] Health check endpoint returns "healthy"
- [ ] Web interface accessible and all tabs work
- [ ] DailyClosePrice.png displays correctly
- [ ] Predictions API works
- [ ] Model Performance metrics display
- [ ] Monitoring/logging configured
- [ ] Auto-scaling enabled (optional)
- [ ] Custom domain configured (optional)
- [ ] README updated with deployment URL

---

## 🎉 Congratulations!

Once all steps are complete, your Gold Price Prediction application will be:
- ✅ Running on AWS
- ✅ Accessible via public URL
- ✅ Showing all visualizations correctly
- ✅ Making accurate predictions
- ✅ Auto-deploying on git push

**Share your deployed URL and get feedback! 🚀**

---

**Need Help?** 
- Review: [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md)
- Check: README.md troubleshooting section
- AWS Logs: `eb logs` or CloudWatch

**Ready to Deploy?** Start with Step 1! ⬆️
