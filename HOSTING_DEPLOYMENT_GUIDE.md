# 🚀 DEPLOYMENT GUIDE - Host Your Transmission Line Fault Detection System

## Quick Options

You have multiple hosting options available:

### Option 1: Run Locally (Easiest - Development)
Perfect for testing and development on your machine.

**Steps:**
```bash
cd AI-Based-Fault-Detection-in-Transmission-Infrastructure
pip install -r requirements.txt
streamlit run app/main.py
```

**Result:** App runs at http://localhost:8501
**Best for:** Development, testing, single user

---

### Option 2: Streamlit Cloud (FREE - Recommended for Easy Deployment)
Deploy directly to Streamlit's cloud platform with zero infrastructure setup.

**Pros:**
- ✅ Completely FREE
- ✅ Easy deployment (3 clicks)
- ✅ Built-in sharing
- ✅ Auto SSL/HTTPS
- ✅ Custom domain support
- ✅ Team collaboration
- ✅ GitHub integration

**Steps:**

1. **Create GitHub Repository**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/transmission-fault-detection.git
git push -u origin main
```

2. **Create Streamlit Cloud Account**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "Deploy an app"

3. **Connect Your Repository**
   - Select repository: `YOUR-USERNAME/transmission-fault-detection`
   - Select branch: `main`
   - Set main file path: `app/main.py`

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app is live! 🎉

**Result:** App runs at: `https://your-username-app-name.streamlit.app`

---

### Option 3: Docker Container (Professional - Production)
Package your app in a Docker container for deployment anywhere.

**Create Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "app/main.py"]
```

**Save as:** `Dockerfile` (in project root)

**Build & Run:**
```bash
docker build -t transmission-fault-detector .
docker run -p 8501:8501 transmission-fault-detector
```

**Push to Docker Hub:**
```bash
docker tag transmission-fault-detector YOUR-USERNAME/transmission-fault-detector
docker login
docker push YOUR-USERNAME/transmission-fault-detector
```

---

### Option 4: AWS EC2 (Scalable)
Deploy on Amazon's cloud with full control.

**Steps:**

1. **Launch EC2 Instance**
   - Instance type: t3.small or larger
   - OS: Ubuntu 22.04
   - Security group: Allow port 8501, 443

2. **SSH and Setup**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip

# Install Python & dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv git

# Clone repository
git clone https://github.com/YOUR-USERNAME/transmission-fault-detection.git
cd transmission-fault-detection

# Install requirements
pip install -r requirements.txt

# Run with PM2 (keeps app running)
sudo npm install -g pm2
pm2 start "streamlit run app/main.py" --name transmission-detector
pm2 startup
pm2 save
```

3. **Setup Reverse Proxy (Nginx)**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

### Option 5: Heroku (Easy & Free Tier Available)
Simple cloud deployment with minimal setup.

**Steps:**

1. **Create Heroku Account**
   - Go to https://www.heroku.com
   - Sign up for free account

2. **Install Heroku CLI**
```bash
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
# Or use chocolatey
choco install heroku-cli
```

3. **Create Procfile**
```
web: sh setup.sh && streamlit run app/main.py
```

4. **Create setup.sh**
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

5. **Deploy**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

**Result:** App at `https://your-app-name.herokuapp.com`

---

### Option 6: Google Cloud Run (Serverless - Pay per Use)
Automatic scaling, pay only for what you use.

**Steps:**

1. **Create Dockerfile** (same as Docker section above)

2. **Deploy to Cloud Run**
```bash
gcloud run deploy transmission-detector \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501
```

**Result:** App at `https://transmission-detector-xxxxx.run.app`

---

## 📊 Comparison Table

| Option | Cost | Setup Time | Best For | Scalability |
|--------|------|-----------|----------|-------------|
| **Local** | Free | 5 min | Development | Single user |
| **Streamlit Cloud** | Free | 15 min | Sharing | 3 concurrent users |
| **Docker** | Varies | 30 min | Production | Excellent |
| **AWS EC2** | $10-30/mo | 45 min | Enterprise | Excellent |
| **Heroku** | Free-50/mo | 20 min | Small teams | Good |
| **Google Cloud** | Pay-per-use | 30 min | Scalable | Excellent |

---

## 🏆 RECOMMENDED: Streamlit Cloud

**Why?**
- ✅ Takes 15 minutes to set up
- ✅ Completely FREE for public apps
- ✅ Built for Streamlit apps
- ✅ GitHub integration
- ✅ Easy to share with team
- ✅ Automatic HTTPS
- ✅ Custom domain support

**Complete Process:**

### Step 1: Prepare Git Repository
```bash
# In project directory
git init
git add .
git commit -m "Transmission Line Fault Detection System"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/transmission-fault-detection.git
git push -u origin main
```

### Step 2: Create Streamlit Account
- Visit https://share.streamlit.io
- Click "Sign up with GitHub"
- Authorize Streamlit to access your GitHub

### Step 3: Deploy App
- Click "New app"
- Select repository: `YOUR-USERNAME/transmission-fault-detection`
- Select branch: `main`
- Set file path: `app/main.py`
- Click "Deploy"

### Step 4: Wait for Deployment
```
✓ Installing dependencies... (1-2 min)
✓ Building app... (30 sec)
✓ App is live! (5 sec)
```

### Result
Your app will be available at:
```
https://your-username-transmission-fault-detection.streamlit.app
```

Share this link with your team!

---

## 🔧 Local Development Setup

If you want to run locally while developing:

### Windows Users:

**Using Batch Script:**
```bash
# Run this file
run_app.bat
```

**Or manually:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
```

### Mac/Linux Users:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

### Access the App
Open browser to: **http://localhost:8501**

---

## 🔐 Security Considerations

### Before Deploying to Production

**Sensitive Data:**
- ✓ No hardcoded API keys
- ✓ No credential storage
- ✓ No user data retention
- ✓ SSL/HTTPS enabled

**Configuration:**
```python
# In app/main.py (already done)
import os
model_path = os.getenv('MODEL_PATH', 'models/fault_detector_best.h5')
```

**Database (if needed):**
```python
# Use environment variables
db_url = os.getenv('DATABASE_URL')
```

---

## 📈 Performance Tips

### For High Traffic:

1. **Enable Caching**
```python
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(...)
```
✓ Already implemented

2. **Limit Concurrent Users**
- Streamlit Cloud: 3 concurrent by default
- AWS/Docker: Use load balancer

3. **Optimize Images**
- Use JPG instead of PNG
- Resize before uploading
- Compress images

4. **Database Optimization**
- Use connection pooling
- Add indexes
- Archive old data

---

## 🆘 Troubleshooting Deployments

### "Module not found" Error
```bash
# Ensure all packages in requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
# Redeploy
```

### App is Slow
```bash
# Check resource usage
streamlit run app/main.py --logger.level=debug

# Increase memory limit (Docker)
docker run -m 4g transmission-detector

# Use AWS larger instance
# t3.small → t3.medium
```

### Port Already in Use
```bash
# Change port
streamlit run app/main.py --server.port 8502
```

### SSL Certificate Issues
```bash
# Most platforms handle automatically (AWS, Heroku, Cloud Run)
# For self-hosted: Use Let's Encrypt
sudo apt-get install certbot
sudo certbot certonly --standalone -d your-domain.com
```

---

## 📊 Monitoring & Maintenance

### For Production Deployments

**Logging:**
```bash
# AWS CloudWatch
# Google Cloud Logging
# Heroku logs: heroku logs -f
# Streamlit Cloud: Built-in analytics
```

**Uptime Monitoring:**
- Uptime.com
- Pingdom
- AWS CloudWatch

**Performance Monitoring:**
- New Relic
- Datadog
- AWS CloudWatch

---

## 🎯 Next Steps

### Immediate (This Week)
1. Choose hosting option
2. Follow deployment steps
3. Test with team
4. Gather feedback

### Short-term (Next 2-4 Weeks)
1. Configure custom domain
2. Set up monitoring
3. Implement analytics
4. Add team management

### Long-term (1-3 Months)
1. Scale to handle more users
2. Integrate with existing systems
3. Add advanced features
4. Implement CI/CD pipeline

---

## 🚀 TL;DR - Just Deploy It

**Fastest way (5 minutes):**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run locally to verify
streamlit run app/main.py

# 3. Push to GitHub
git add . && git commit -m "Deploy" && git push

# 4. Go to https://share.streamlit.io
# 5. Click "Deploy app"
# 6. Done! 🎉
```

**Your app is now live and shareable!**

---

## 📞 Support

For Streamlit Cloud issues: https://discuss.streamlit.io
For AWS issues: https://aws.amazon.com/support
For Heroku issues: https://help.heroku.com

---

**Choose your hosting option above and get started! Your system is production-ready.** 🚀
