# DigitalOcean Deployment Guide

Complete guide to deploy the Gold Price Prediction app on DigitalOcean using your $200 GitHub Student Developer Pack credit.

---

## Why DigitalOcean?

- ✅ $200 credit with GitHub Student Developer Pack
- ✅ Simple pricing ($4-12/month for this project)
- ✅ Easy to use App Platform (similar to Heroku)
- ✅ Excellent documentation and community
- ✅ Great for student projects

---

## Deployment Options

### Option 1: App Platform (Recommended - Easiest) 💰 $5-12/month
PaaS solution, automatic deployments from GitHub, zero server management.

### Option 2: Droplet + Docker 💰 $4-6/month
More control, cheapest option, requires some server management.

### Option 3: Kubernetes 💰 $12+/month
Overkill for this project, but good learning experience.

---

## Option 1: DigitalOcean App Platform (Recommended)

### Step 1: Prepare Your Repository

```bash
# Ensure everything is committed
git add .
git commit -m "Prepare for DigitalOcean deployment"
git push origin main
```

### Step 2: Create app.yaml Configuration

Create this file in your project root:

```yaml
# app.yaml
name: gold-price-prediction
region: nyc

services:
- name: web
  github:
    repo: YOUR_GITHUB_USERNAME/ML_gold_preditct_project
    branch: main
    deploy_on_push: true
  
  source_dir: /webapp
  
  run_command: gunicorn --bind 0.0.0.0:$PORT app:app
  
  envs:
  - key: PORT
    value: "8080"
  
  instance_count: 1
  instance_size_slug: basic-xxs  # $5/month - 512MB RAM, good for starting
  
  routes:
  - path: /
  
  health_check:
    http_path: /health
    initial_delay_seconds: 10
    period_seconds: 10
    timeout_seconds: 5
    success_threshold: 1
    failure_threshold: 3

  alerts:
  - rule: DEPLOYMENT_FAILED
  - rule: DOMAIN_FAILED
```

### Step 3: Update requirements.txt

Ensure your `requirements.txt` includes:

```txt
flask>=2.3.0
gunicorn>=21.2.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
xgboost>=1.7.0
lightgbm>=4.0.0
yfinance>=0.2.28
matplotlib>=3.7.0
seaborn>=0.12.0
joblib>=1.3.0
```

### Step 4: Create Procfile (Optional)

```bash
# Procfile
web: cd webapp && gunicorn --bind 0.0.0.0:$PORT app:app --workers 2 --timeout 120
```

### Step 5: Deploy via Web Interface

1. **Sign up/Login to DigitalOcean**
   - Go to: https://www.digitalocean.com/
   - Use GitHub Student Developer Pack link to activate $200 credit
   - Sign in with GitHub

2. **Create New App**
   - Click "Create" → "Apps"
   - Choose "GitHub" as source
   - Authorize DigitalOcean to access your repository
   - Select your repository: `ML_gold_preditct_project`
   - Select branch: `main`

3. **Configure App**
   - **Name**: gold-price-prediction
   - **Region**: New York (NYC) or closest to you
   - **Branch**: main
   - **Autodeploy**: Enable ✅
   - **Source Directory**: Leave empty or set to `/`
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `cd webapp && gunicorn --bind 0.0.0.0:$PORT app:app`

4. **Configure Resources**
   - **Plan**: Basic (512 MB RAM, 1 vCPU) - $5/month
   - **Instances**: 1
   
5. **Environment Variables** (if needed)
   - Click "Edit" next to Environment Variables
   - Add any required variables (none needed for basic setup)

6. **Review and Deploy**
   - Review all settings
   - Click "Create Resources"
   - Wait 5-10 minutes for deployment

7. **Access Your App**
   - You'll get a URL like: `https://gold-price-prediction-xxxxx.ondigitalocean.app`
   - Test: `https://your-app.ondigitalocean.app/health`

### Step 6: Custom Domain (Optional)

1. Go to your app → Settings → Domains
2. Click "Add Domain"
3. Enter your domain name
4. Add CNAME record to your DNS:
   ```
   Type: CNAME
   Host: www
   Value: gold-price-prediction-xxxxx.ondigitalocean.app
   ```

---

## Option 2: DigitalOcean Droplet with Docker

Cheaper ($4/month) but requires more setup.

### Step 1: Create Droplet

1. **Sign in to DigitalOcean**
2. **Create Droplet**:
   - Click "Create" → "Droplets"
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic
   - **CPU Options**: Regular (Disk: SSD)
   - **Size**: $4/month (512 MB, 1 vCPU, 10 GB SSD)
   - **Datacenter**: Choose closest region
   - **Authentication**: SSH Key (recommended) or Password
   - **Hostname**: gold-price-prediction

3. **Wait for creation** (1-2 minutes)

### Step 2: SSH into Droplet

```bash
# Use the IP address shown in your dashboard
ssh root@YOUR_DROPLET_IP

# Or with SSH key
ssh -i ~/.ssh/your_key root@YOUR_DROPLET_IP
```

### Step 3: Install Docker

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Verify installation
docker --version
```

### Step 4: Clone and Deploy

```bash
# Install Git
apt install -y git

# Clone your repository
git clone https://github.com/YOUR_USERNAME/ML_gold_preditct_project.git
cd ML_gold_preditct_project

# Build Docker image
docker build -t gold-price-app .

# Run container
docker run -d \
  -p 80:5001 \
  --name gold-app \
  --restart unless-stopped \
  gold-price-app

# Check status
docker ps
docker logs gold-app

# Test
curl http://localhost/health
```

### Step 5: Setup Nginx (Recommended)

```bash
# Install Nginx
apt install -y nginx

# Create Nginx configuration
cat > /etc/nginx/sites-available/gold-price <<'EOF'
server {
    listen 80;
    server_name YOUR_DROPLET_IP;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/gold-price /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Test
curl http://YOUR_DROPLET_IP/health
```

### Step 6: Setup SSL with Let's Encrypt (Optional)

```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Get certificate (replace with your domain)
certbot --nginx -d yourdomain.com

# Certbot will auto-configure SSL
# Test: https://yourdomain.com
```

### Step 7: Auto-Update from GitHub

```bash
# Create update script
cat > /root/update-app.sh <<'EOF'
#!/bin/bash
cd /root/ML_gold_preditct_project
git pull origin main
docker stop gold-app
docker rm gold-app
docker build -t gold-price-app .
docker run -d -p 5001:5001 --name gold-app --restart unless-stopped gold-price-app
EOF

chmod +x /root/update-app.sh

# Run when you push updates
# SSH in and run: /root/update-app.sh
```

---

## Option 3: DigitalOcean Kubernetes

For learning purposes only - overkill for this project.

### Quick Setup

```bash
# Install doctl (DigitalOcean CLI)
brew install doctl  # macOS
# or
snap install doctl  # Linux

# Authenticate
doctl auth init

# Create Kubernetes cluster
doctl kubernetes cluster create gold-cluster \
  --region nyc1 \
  --node-pool "name=worker-pool;size=s-1vcpu-2gb;count=2" \
  --auto-upgrade=true

# Takes 5-10 minutes
```

(This gets expensive - not recommended for student projects)

---

## Cost Comparison

| Option | Monthly Cost | Setup Time | Management |
|--------|--------------|------------|------------|
| **App Platform** | $5-12 | 10 mins | Zero |
| **Droplet + Docker** | $4-6 | 30 mins | Minimal |
| **Kubernetes** | $24+ | 1-2 hours | Moderate |

**Recommendation**: Use App Platform for ease, or Droplet if you want to save money and learn server management.

---

## GitHub Actions for App Platform

Create `.github/workflows/deploy-do.yml`:

```yaml
name: Deploy to DigitalOcean

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install doctl
      uses: digitalocean/action-doctl@v2
      with:
        token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
    
    - name: Trigger App Platform deployment
      run: |
        doctl apps create-deployment ${{ secrets.APP_ID }}
```

**Setup**:
1. Get API token: DigitalOcean → API → Generate New Token
2. Add to GitHub Secrets:
   - `DIGITALOCEAN_ACCESS_TOKEN`
   - `APP_ID` (from your App Platform URL)

---

## Monitoring & Logs

### App Platform

```bash
# Install doctl
brew install doctl

# View logs
doctl apps logs YOUR_APP_ID --type=RUN

# Live logs
doctl apps logs YOUR_APP_ID --type=RUN --follow
```

### Droplet

```bash
# SSH into droplet
ssh root@YOUR_DROPLET_IP

# View Docker logs
docker logs -f gold-app

# Check resource usage
docker stats gold-app

# Check Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## Scaling

### App Platform
- Go to your app → Settings → Resources
- Increase instance count or size
- Changes apply automatically

### Droplet
- Resize droplet: Droplets → More → Resize
- Or add more droplets behind a load balancer

---

## Troubleshooting

### App Platform Issues

**Build fails:**
```bash
# Check build logs in dashboard
# Common fixes:
# 1. Verify requirements.txt has all dependencies
# 2. Ensure Python 3.9+ specified
# 3. Check build command is correct
```

**App crashes:**
```bash
# Check logs
doctl apps logs YOUR_APP_ID --type=RUN

# Common issues:
# 1. Port binding (use $PORT environment variable)
# 2. Memory limit (upgrade instance size)
# 3. Missing models (commit to git)
```

### Droplet Issues

**Can't connect:**
```bash
# Check firewall
ufw status
ufw allow 80
ufw allow 443
ufw allow 22

# Check Docker
docker ps
docker logs gold-app
```

**Out of memory:**
```bash
# Add swap space
fallocate -l 1G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

---

## Best Practices

1. **Use App Platform for production** - It's worth the extra $1-2/month
2. **Enable monitoring** - Set up alerts in DigitalOcean dashboard
3. **Regular backups** - Enable automated backups ($0.80/month)
4. **Use environment variables** - Never commit secrets
5. **Setup CI/CD** - Automatic deployments from GitHub
6. **Monitor costs** - Check billing regularly

---

## Student Tips

1. **$200 credit lasts**: With $5/month plan = 40 months of hosting!
2. **Start small**: Use $4-5/month plans, upgrade if needed
3. **Learn**: Try Droplet option to learn server management
4. **Portfolio**: Great for resume - "Deployed ML app on cloud"
5. **Experiment**: With $200, you can try different setups

---

## Quick Start Commands

### App Platform (Easiest)
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to DigitalOcean"
git push origin main

# 2. Go to DO dashboard and create app
# 3. Connect GitHub repo
# 4. Deploy! ✅
```

### Droplet (Cheapest)
```bash
# 1. Create droplet on DO dashboard
# 2. SSH in
ssh root@YOUR_IP

# 3. Quick deploy
git clone YOUR_REPO
cd ML_gold_preditct_project
curl -fsSL https://get.docker.com | sh
docker build -t app .
docker run -d -p 80:5001 --restart unless-stopped app

# 4. Done! Visit http://YOUR_IP
```

---

## Next Steps After Deployment

1. ✅ Test your deployed app
2. ✅ Add custom domain (optional)
3. ✅ Setup SSL certificate
4. ✅ Configure monitoring/alerts
5. ✅ Update README with deployment URL
6. ✅ Add to your portfolio!

---

## Support Resources

- **DigitalOcean Docs**: https://docs.digitalocean.com/
- **Community Tutorials**: https://www.digitalocean.com/community/tutorials
- **App Platform Guide**: https://docs.digitalocean.com/products/app-platform/
- **Support**: https://www.digitalocean.com/support/

---

## Estimated Monthly Costs

**Development (Testing)**:
- App Platform: $5/month (Basic)
- OR Droplet: $4/month
- **Total: $4-5/month**

**Production (With backup & monitoring)**:
- App Platform: $12/month (Professional)
- Backups: $1/month
- Monitoring: Free
- **Total: $13/month**

With $200 credit:
- Dev setup: 40 months free!
- Prod setup: 15 months free!

---

**Ready to deploy? Start with App Platform - it's the easiest!**

See [DEPLOYMENT_NEXT_STEPS.md](DEPLOYMENT_NEXT_STEPS.md) for general deployment preparation.
