# AWS Deployment Guide for Gold Price Prediction

This guide will help you deploy the Gold Price Prediction web application to AWS.

## Deployment Options

### Option 1: AWS Elastic Beanstalk (Recommended for Beginners)
Easiest option with automatic scaling and load balancing.

### Option 2: AWS ECS with Fargate
Fully managed container service, good for production.

### Option 3: AWS EC2 + Docker
More control, suitable for advanced users.

---

## Option 1: AWS Elastic Beanstalk Deployment

### Prerequisites
- AWS Account
- AWS CLI installed and configured
- EB CLI installed: `pip install awsebcli`

### Step 1: Install AWS CLI and EB CLI

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (e.g., us-east-1), Output format (json)

# Install Elastic Beanstalk CLI
pip install awsebcli
```

### Step 2: Prepare Application

```bash
# Run setup script
python setup_deployment.py

# Ensure models are trained
# Run GoldSense_Train_Local.ipynb or GoldSense_Train_Combined_colab.ipynb

# Test locally first
cd webapp
python app.py
# Visit http://localhost:5001
```

### Step 3: Initialize Elastic Beanstalk

```bash
# From project root
cd webapp

# Initialize EB application
eb init -p python-3.9 gold-price-prediction --region us-east-1

# This creates .elasticbeanstalk/config.yml
```

### Step 4: Create Environment and Deploy

```bash
# Create environment and deploy
eb create gold-price-env

# Wait for deployment (5-10 minutes)

# Open application
eb open
```

### Step 5: Update Application (Future Deploys)

```bash
# Make changes, then:
eb deploy

# Check status
eb status

# View logs
eb logs
```

### Step 6: Environment Configuration

```bash
# Set environment variables if needed
eb setenv SECRET_KEY=your-secret-key

# Scale up if needed
eb scale 2
```

### Step 7: Custom Domain (Optional)

1. Go to AWS Console → Elastic Beanstalk → Your Environment
2. Configuration → Load balancer
3. Add listener on port 443 with SSL certificate
4. Update Route53 or your DNS to point to EB URL

---

## Option 2: AWS ECS with Fargate

### Step 1: Build and Push Docker Image to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name gold-price-prediction

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build Docker image
docker build -t gold-price-prediction .

# Tag image
docker tag gold-price-prediction:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/gold-price-prediction:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/gold-price-prediction:latest
```

### Step 2: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster --cluster-name gold-price-cluster
```

### Step 3: Create Task Definition

Create `ecs-task-definition.json`:

```json
{
  "family": "gold-price-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "gold-price-container",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/gold-price-prediction:latest",
      "portMappings": [
        {
          "containerPort": 5001,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/gold-price",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ecsTaskExecutionRole"
}
```

Register task:
```bash
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
```

### Step 4: Create Service

```bash
# Create service with load balancer
aws ecs create-service \
  --cluster gold-price-cluster \
  --service-name gold-price-service \
  --task-definition gold-price-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

---

## Option 3: AWS EC2 with Docker

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Choose Ubuntu 22.04 LTS
3. Instance type: t3.medium (2 vCPU, 4 GB RAM)
4. Configure Security Group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
5. Launch and download key pair

### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Exit and reconnect for group changes
exit
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### Step 3: Deploy Application

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ML_gold_preditct_project.git
cd ML_gold_preditct_project

# Build and run
docker build -t gold-price-prediction .
docker run -d -p 80:5001 --name gold-app gold-price-prediction

# Check logs
docker logs -f gold-app
```

### Step 4: Setup Nginx (Optional - for production)

```bash
# Install nginx
sudo apt install nginx -y

# Configure nginx
sudo nano /etc/nginx/sites-available/gold-price
```

Nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/gold-price /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: SSL with Let's Encrypt (Optional)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## GitHub Actions CI/CD for AWS

The project includes `.github/workflows/deploy.yml` configured for AWS deployment.

### Setup GitHub Secrets

Go to Repository → Settings → Secrets and variables → Actions

Add these secrets:

**For Elastic Beanstalk:**
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `AWS_REGION` - e.g., us-east-1
- `EB_APPLICATION_NAME` - gold-price-prediction
- `EB_ENVIRONMENT_NAME` - gold-price-env

**For ECS:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `ECR_REPOSITORY` - gold-price-prediction
- `ECS_CLUSTER` - gold-price-cluster
- `ECS_SERVICE` - gold-price-service
- `ECS_TASK_DEFINITION` - gold-price-task

---

## Monitoring and Maintenance

### CloudWatch Logs

```bash
# View logs in CloudWatch
aws logs tail /aws/elasticbeanstalk/gold-price-env/var/log/web.stdout.log --follow

# Or for ECS
aws logs tail /ecs/gold-price --follow
```

### Health Checks

The app includes `/health` endpoint:
```bash
curl https://your-app-url/health
```

### Scaling

**Elastic Beanstalk:**
```bash
eb scale 3  # Scale to 3 instances
```

**ECS:**
```bash
aws ecs update-service --cluster gold-price-cluster \
  --service gold-price-service --desired-count 3
```

---

## Cost Estimation

**Elastic Beanstalk (t3.medium):**
- EC2: ~$30/month
- Load Balancer: ~$20/month
- **Total: ~$50/month**

**ECS Fargate (1 vCPU, 2GB):**
- Compute: ~$35/month for 24/7
- **Total: ~$35-50/month**

**EC2 (t3.medium):**
- Instance: ~$30/month
- **Total: ~$30/month** (cheapest)

---

## Troubleshooting

### Models Not Loading
```bash
# Check if models exist
ls -lh models/

# Re-run training notebook if needed
# Then redeploy
```

### Memory Issues
```bash
# Increase instance size
# EB: Go to console → Configuration → Capacity → Instance type
# ECS: Update task definition with more memory
# EC2: Resize instance
```

### Slow API Responses
```bash
# Enable caching
# Use ElastiCache (Redis) for prediction caching
# Scale up instances
```

---

## Next Steps

1. **Test locally:** `cd webapp && python app.py`
2. **Setup AWS credentials:** `aws configure`
3. **Choose deployment option** (Elastic Beanstalk recommended)
4. **Deploy:** Follow steps for chosen option
5. **Setup CI/CD:** Configure GitHub Actions
6. **Monitor:** Check CloudWatch logs and metrics

## Support

For issues:
1. Check logs: `eb logs` or `docker logs`
2. Review troubleshooting section
3. Consult AWS documentation
4. Check GitHub issues

---

**Note:** Remember to update security groups, enable HTTPS, and follow AWS security best practices for production deployments.
