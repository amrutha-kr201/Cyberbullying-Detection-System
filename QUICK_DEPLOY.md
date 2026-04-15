# 🚀 Quick Deploy Guide

## Easiest Method: Render (5 minutes)

### Step 1: Go to Render
Visit: https://render.com and sign up with GitHub

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub account
3. Select repository: `Cyberbullying-Detection-System`

### Step 3: Configure
- **Name:** `cyberbullying-detection`
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt && apt-get update && apt-get install -y tesseract-ocr`
- **Start Command:** `gunicorn app:app`
- **Instance Type:** Free

### Step 4: Add Environment Variables
Click "Advanced" → Add Environment Variables:

| Key | Value |
|-----|-------|
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_PASSWORD` | `Admin@3117` |
| `SUPABASE_URL` | `https://frsoirtfooinbdlclhjg.supabase.co` |
| `SUPABASE_KEY` | `your-supabase-key` |
| `SECRET_KEY` | `your-random-secret-key` |

### Step 5: Deploy!
Click "Create Web Service"

⏳ Wait 5-10 minutes for deployment...

✅ Your app will be live at: `https://cyberbullying-detection.onrender.com`

---

## Alternative: Railway (Even Easier!)

### Step 1: Go to Railway
Visit: https://railway.app and sign up with GitHub

### Step 2: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `Cyberbullying-Detection-System`
4. Railway auto-detects and deploys!

### Step 3: Add Environment Variables
Go to Variables tab and add:
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `SUPABASE_URL`
- `SUPABASE_KEY`

### Step 4: Get URL
Click "Settings" → "Generate Domain"

✅ Your app is live!

---

## Testing Your Deployment

1. Visit your deployed URL
2. You should see the login page
3. Sign up as a user
4. Test detection features
5. Access admin at: `your-url/admin/login`

---

## Troubleshooting

**Issue:** App crashes on startup
**Fix:** Check logs for missing dependencies

**Issue:** Tesseract not found
**Fix:** Make sure build command includes tesseract installation

**Issue:** 502 Bad Gateway
**Fix:** Wait a few minutes, free tier has cold starts

---

## Need Help?

Read the full guide: `DEPLOYMENT_GUIDE.md`

Or contact: amruthakr201@gmail.com
