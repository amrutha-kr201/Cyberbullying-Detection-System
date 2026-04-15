# 🚀 Deployment Guide - Cyberbullying Detection System

This guide covers multiple deployment options for your Flask application.

---

## 📋 Table of Contents

1. [Render (Recommended - Free)](#option-1-render-recommended)
2. [Railway (Easy - Free Tier)](#option-2-railway)
3. [PythonAnywhere (Simple - Free)](#option-3-pythonanywhere)
4. [Heroku (Popular - Paid)](#option-4-heroku)
5. [AWS EC2 (Advanced)](#option-5-aws-ec2)

---

## Option 1: Render (Recommended)

**Pros:** Free tier, automatic deployments, supports Python, easy setup
**Cons:** Cold starts on free tier

### Step-by-Step:

#### 1. Prepare Your Application

Create `render.yaml` in your project root:

```yaml
services:
  - type: web
    name: cyberbullying-detection
    env: python
    buildCommand: "pip install -r requirements.txt && apt-get update && apt-get install -y tesseract-ocr"
    startCommand: "gunicorn app:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: ADMIN_USERNAME
        value: admin
      - key: ADMIN_PASSWORD
        generateValue: true
```

#### 2. Update requirements.txt

Add gunicorn:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### 3. Update app.py

Change the last line from:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

To:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

#### 4. Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name:** cyberbullying-detection
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Add Environment Variables:
   - `ADMIN_USERNAME`: admin
   - `ADMIN_PASSWORD`: your-password
   - `SUPABASE_URL`: your-supabase-url
   - `SUPABASE_KEY`: your-supabase-key
7. Click "Create Web Service"

**Your app will be live at:** `https://cyberbullying-detection.onrender.com`

---

## Option 2: Railway

**Pros:** Very easy, automatic deployments, generous free tier
**Cons:** Requires credit card for free tier

### Step-by-Step:

#### 1. Create Procfile

Create `Procfile` in project root:
```
web: gunicorn app:app
```

#### 2. Add gunicorn to requirements.txt

```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### 3. Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy
6. Add Environment Variables in Settings:
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
7. Click "Generate Domain" to get your URL

**Your app will be live at:** `https://your-app.railway.app`

---

## Option 3: PythonAnywhere

**Pros:** Free tier, Python-focused, no credit card needed
**Cons:** Limited resources, manual setup

### Step-by-Step:

#### 1. Sign Up

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free account

#### 2. Upload Your Code

1. Go to "Files" tab
2. Upload your project files or clone from GitHub:
   ```bash
   git clone https://github.com/amrutha-kr201/Cyberbullying-Detection-System.git
   ```

#### 3. Install Dependencies

1. Go to "Consoles" tab
2. Start a Bash console
3. Run:
   ```bash
   cd Cyberbullying-Detection-System
   pip3 install --user -r requirements.txt
   ```

#### 4. Install Tesseract

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### 5. Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Choose Python 3.10
5. Set source code directory: `/home/yourusername/Cyberbullying-Detection-System`
6. Edit WSGI file:
   ```python
   import sys
   path = '/home/yourusername/Cyberbullying-Detection-System'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
7. Reload the web app

**Your app will be live at:** `https://yourusername.pythonanywhere.com`

---

## Option 4: Heroku

**Pros:** Popular, well-documented, many add-ons
**Cons:** No free tier anymore (starts at $5/month)

### Step-by-Step:

#### 1. Install Heroku CLI

Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

#### 2. Create Required Files

**Procfile:**
```
web: gunicorn app:app
```

**runtime.txt:**
```
python-3.11.0
```

**Aptfile** (for Tesseract):
```
tesseract-ocr
tesseract-ocr-eng
```

#### 3. Add Buildpacks

Create `heroku.yml`:
```yaml
build:
  languages:
    - python
  packages:
    - tesseract-ocr
run:
  web: gunicorn app:app
```

#### 4. Deploy

```bash
heroku login
heroku create cyberbullying-detection
heroku buildpacks:add --index 1 heroku-community/apt
heroku buildpacks:add --index 2 heroku/python
git push heroku main
heroku config:set ADMIN_USERNAME=admin
heroku config:set ADMIN_PASSWORD=your-password
heroku config:set SUPABASE_URL=your-url
heroku config:set SUPABASE_KEY=your-key
heroku open
```

**Your app will be live at:** `https://cyberbullying-detection.herokuapp.com`

---

## Option 5: AWS EC2

**Pros:** Full control, scalable, professional
**Cons:** Complex setup, requires AWS knowledge

### Step-by-Step:

#### 1. Launch EC2 Instance

1. Go to AWS Console → EC2
2. Launch Instance:
   - **AMI:** Ubuntu 22.04 LTS
   - **Instance Type:** t2.micro (free tier)
   - **Security Group:** Allow HTTP (80), HTTPS (443), SSH (22)
3. Create and download key pair

#### 2. Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

#### 3. Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx tesseract-ocr -y
```

#### 4. Clone and Setup

```bash
git clone https://github.com/amrutha-kr201/Cyberbullying-Detection-System.git
cd Cyberbullying-Detection-System
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 5. Create Systemd Service

Create `/etc/systemd/system/cyberbullying.service`:
```ini
[Unit]
Description=Cyberbullying Detection System
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Cyberbullying-Detection-System
Environment="PATH=/home/ubuntu/Cyberbullying-Detection-System/venv/bin"
ExecStart=/home/ubuntu/Cyberbullying-Detection-System/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

#### 6. Configure Nginx

Create `/etc/nginx/sites-available/cyberbullying`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/cyberbullying /etc/nginx/sites-enabled/
sudo systemctl restart nginx
sudo systemctl enable cyberbullying
sudo systemctl start cyberbullying
```

**Your app will be live at:** `http://your-ec2-ip`

---

## 🔧 Pre-Deployment Checklist

Before deploying, make sure to:

### 1. Update app.py for Production

```python
import os

# Change debug mode
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False  # Set to False for production
    )
```

### 2. Use Environment Variables

Update app.py to use environment variables:

```python
# Admin credentials from environment
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@3117')

# Supabase from environment
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')
```

### 3. Update SECRET_KEY

```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
```

### 4. Add gunicorn to requirements.txt

```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

### 5. Test Locally

```bash
gunicorn app:app
```

Visit `http://localhost:8000` to test.

---

## 🌐 Custom Domain Setup

After deployment, you can add a custom domain:

### For Render/Railway:
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records (CNAME)

### For AWS:
1. Get Elastic IP
2. Point your domain's A record to the IP
3. Setup SSL with Let's Encrypt:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

---

## 📊 Monitoring & Maintenance

### Check Logs:

**Render/Railway:** Built-in logs in dashboard

**PythonAnywhere:** Error log in Web tab

**Heroku:**
```bash
heroku logs --tail
```

**AWS:**
```bash
sudo journalctl -u cyberbullying -f
```

### Update Deployment:

Just push to GitHub:
```bash
git add .
git commit -m "Update"
git push
```

Most platforms auto-deploy on push!

---

## 🆘 Troubleshooting

### Issue: Tesseract not found
**Solution:** Make sure Tesseract is installed in buildpack/system

### Issue: Port already in use
**Solution:** Use environment variable PORT

### Issue: Database/files not persisting
**Solution:** Use external storage (AWS S3, Supabase Storage)

### Issue: Cold starts (slow first load)
**Solution:** Upgrade to paid tier or use keep-alive service

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Render | ✅ 750 hrs/month | $7/month | Beginners |
| Railway | ✅ $5 credit | $5/month | Easy setup |
| PythonAnywhere | ✅ Limited | $5/month | Learning |
| Heroku | ❌ None | $5/month | Production |
| AWS EC2 | ✅ 750 hrs/month | Variable | Advanced |

---

## 🎯 Recommended: Render

For your project, I recommend **Render** because:
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Easy to setup
- ✅ Supports Python and Tesseract
- ✅ Good for portfolio projects

---

## 📝 Quick Start (Render)

1. Add to requirements.txt:
   ```
   gunicorn==21.2.0
   ```

2. Update app.py last line:
   ```python
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
   ```

3. Push to GitHub:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push
   ```

4. Go to render.com → New Web Service → Connect GitHub → Deploy!

**Done! Your app is live! 🚀**

---

Need help? Check the platform-specific documentation or ask for assistance!
