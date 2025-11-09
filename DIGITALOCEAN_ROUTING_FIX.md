# CRITICAL FIX: DigitalOcean App Platform Configuration

## The Problem

Your app is running (gunicorn starts), but DigitalOcean's router isn't forwarding HTTP requests to it. This is a **configuration issue in DigitalOcean's App Spec**, not your code.

## The Solution

You MUST manually configure the App Spec in DigitalOcean console. Follow these exact steps:

### Step 1: Access App Settings

1. Go to https://cloud.digitalocean.com/apps
2. Click on your app: **goldsense2** (or goldfsenseait-kov5n)
3. Click **Settings** tab (top menu)
4. Scroll down to **App Spec**
5. Click **Edit** button

### Step 2: Replace the Entire App Spec

Delete everything and paste this EXACT configuration:

```yaml
name: goldsense2
region: nyc
services:
- build_command: pip install -r requirements.txt
  environment_slug: python
  github:
    branch: main
    deploy_on_push: true
    repo: shadowsilence94/goldSense
  health_check:
    failure_threshold: 3
    http_path: /health
    initial_delay_seconds: 30
    period_seconds: 10
    success_threshold: 1
    timeout_seconds: 5
  http_port: 8080
  instance_count: 1
  instance_size_slug: basic-xxs
  name: web
  routes:
  - path: /
  run_command: gunicorn --bind 0.0.0.0:$PORT app:app --workers 2 --timeout 120 --log-level info --access-logfile - --error-logfile -
  source_dir: /
```

### Step 3: Key Settings to Verify

Make absolutely sure these are correct:

1. **`http_port: 8080`** - Must match the port gunicorn binds to
2. **`routes: - path: /`** - This tells DigitalOcean to route traffic to your service
3. **`run_command:`** - Must be exactly as shown above
4. **`source_dir: /`** - Run from project root

### Step 4: Save and Deploy

1. Click **Save** at the bottom
2. DigitalOcean will show a confirmation dialog
3. Click **Update and Redeploy**
4. Wait 2-3 minutes for deployment

### Step 5: Test

After deployment completes:

1. Visit: `https://your-app-name.ondigitalocean.app/health`
2. Should return JSON: `{"status": "unhealthy", "models_loaded": false, ...}`
3. Then visit: `https://your-app-name.ondigitalocean.app/`
4. Should show the Gold Price Prediction interface

## Alternative: Use DigitalOcean CLI

If the web console doesn't work:

```bash
# Install doctl
brew install doctl  # macOS
# or: snap install doctl  # Linux
# or download from: https://docs.digitalocean.com/reference/doctl/how-to/install/

# Authenticate
doctl auth init
# Paste your DigitalOcean API token when prompted

# Get your app ID
doctl apps list

# Create app spec file
cat > /tmp/app-spec.yaml << 'EOF'
name: goldsense2
region: nyc
services:
- build_command: pip install -r requirements.txt
  environment_slug: python
  github:
    branch: main
    deploy_on_push: true
    repo: shadowsilence94/goldSense
  health_check:
    failure_threshold: 3
    http_path: /health
    initial_delay_seconds: 30
    period_seconds: 10
    success_threshold: 1
    timeout_seconds: 5
  http_port: 8080
  instance_count: 1
  instance_size_slug: basic-xxs
  name: web
  routes:
  - path: /
  run_command: gunicorn --bind 0.0.0.0:$PORT app:app --workers 2 --timeout 120 --log-level info --access-logfile - --error-logfile -
  source_dir: /
EOF

# Update app (replace YOUR_APP_ID with actual ID)
doctl apps update YOUR_APP_ID --spec /tmp/app-spec.yaml
```

## Why This Fixes It

The issue is that DigitalOcean's router needs to know:
1. Which port your app listens on (`http_port: 8080`)
2. Which paths to route to your app (`routes: - path: /`)
3. How to start your app (`run_command`)

Without the correct `routes` configuration, DigitalOcean returns 404 for all requests because it doesn't know where to send them.

## After This Fix

Once configured correctly, you should see:

**In Runtime Logs:**
```
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:8080
[INFO] Booting worker with pid: 14
🌐 GET / from 10.x.x.x      ← THIS LINE PROVES REQUESTS ARE REACHING YOUR APP
📍 Home route accessed
📤 Response status: 200
```

**In Browser:**
- `/health` returns JSON
- `/debug` shows configuration
- `/` shows the web interface

## Still Not Working?

If it still doesn't work after this:

1. Go to App Settings → Components → web
2. Check if HTTP Port is set to 8080
3. Check if HTTP Routes shows "/"
4. Share a screenshot of the App Spec from the console

The issue is 100% in DigitalOcean's configuration, not your code!
