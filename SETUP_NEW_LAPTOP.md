# 💻 Setup on New Laptop

## Quick Setup Guide

### Prerequisites Check

Before starting, verify you have:
- [ ] Python 3.8 or higher
- [ ] Git installed
- [ ] Internet connection

---

## Windows Setup

### Step 1: Install Tesseract OCR

1. **Download Tesseract:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download: `tesseract-ocr-w64-setup-5.3.3.20231005.exe`
   - Run installer
   - Install to: `C:\Program Files\Tesseract-OCR\`
   - ✅ Check "Add to PATH" during installation

2. **Verify Installation:**
   ```bash
   tesseract --version
   ```
   Should show: `tesseract 5.x.x`

### Step 2: Clone Repository

```bash
git clone https://github.com/amrutha-kr201/Cyberbullying-Detection-System.git
cd Cyberbullying-Detection-System
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Application

**Option A: Use Supabase (Recommended)**
1. Copy `supabase_config.example.py` to `supabase_config.py`
2. Add your Supabase credentials:
   ```python
   SUPABASE_URL = "https://frsoirtfooinbdlclhjg.supabase.co"
   SUPABASE_KEY = "your-key-here"
   ```

**Option B: Skip Supabase**
- Authentication will work without Supabase
- Users stored in local `users.json` file

### Step 5: Run Application

```bash
python app.py
```

Open browser: http://127.0.0.1:5000

---

## Mac Setup

### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Tesseract

```bash
brew install tesseract
```

Verify:
```bash
tesseract --version
```

### Step 3: Clone Repository

```bash
git clone https://github.com/amrutha-kr201/Cyberbullying-Detection-System.git
cd Cyberbullying-Detection-System
```

### Step 4: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 5: Configure & Run

Same as Windows Step 4 & 5

---

## Linux Setup

### Step 1: Install Tesseract

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Fedora:**
```bash
sudo dnf install tesseract
```

**Arch:**
```bash
sudo pacman -S tesseract
```

Verify:
```bash
tesseract --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/amrutha-kr201/Cyberbullying-Detection-System.git
cd Cyberbullying-Detection-System
```

### Step 3: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 4: Configure & Run

Same as Windows Step 4 & 5

---

## Troubleshooting

### Issue: "tesseract is not recognized"

**Windows:**
1. Find Tesseract installation path (usually `C:\Program Files\Tesseract-OCR\`)
2. Add to PATH:
   - Search "Environment Variables"
   - Edit "Path" variable
   - Add: `C:\Program Files\Tesseract-OCR\`
   - Restart terminal

**Mac/Linux:**
```bash
which tesseract
```
Should show path. If not, reinstall.

### Issue: "pytesseract.pytesseract.TesseractNotFoundError"

**Fix in app.py:**
```python
# Update line 125 with your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
# OR
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # Mac
# OR
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Linux
```

### Issue: "ModuleNotFoundError"

```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Port 5000 already in use"

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

Or change port in app.py:
```python
app.run(debug=False, host='0.0.0.0', port=8000)  # Use port 8000
```

---

## One-Command Setup (Advanced)

### Windows PowerShell Script

Create `setup.ps1`:
```powershell
# Check Python
python --version

# Clone repo
git clone https://github.com/amrutha-kr201/Cyberbullying-Detection-System.git
cd Cyberbullying-Detection-System

# Install dependencies
pip install -r requirements.txt

# Create config
Copy-Item supabase_config.example.py supabase_config.py

Write-Host "Setup complete! Edit supabase_config.py and run: python app.py"
```

Run:
```bash
powershell -ExecutionPolicy Bypass -File setup.ps1
```

### Mac/Linux Bash Script

Create `setup.sh`:
```bash
#!/bin/bash

# Check Python
python3 --version

# Install Tesseract
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install tesseract
else
    sudo apt-get update && sudo apt-get install -y tesseract-ocr
fi

# Clone repo
git clone https://github.com/amrutha-kr201/Cyberbullying-Detection-System.git
cd Cyberbullying-Detection-System

# Install dependencies
pip3 install -r requirements.txt

# Create config
cp supabase_config.example.py supabase_config.py

echo "Setup complete! Edit supabase_config.py and run: python3 app.py"
```

Run:
```bash
chmod +x setup.sh
./setup.sh
```

---

## Verification Checklist

After setup, verify everything works:

- [ ] Python installed: `python --version`
- [ ] Tesseract installed: `tesseract --version`
- [ ] Dependencies installed: `pip list | grep Flask`
- [ ] Repository cloned: `ls` shows project files
- [ ] Config created: `supabase_config.py` exists
- [ ] App runs: `python app.py` starts server
- [ ] Browser works: http://127.0.0.1:5000 loads
- [ ] Login works: Can sign up and login
- [ ] Text detection works: Can analyze text
- [ ] Image detection works: Can upload and analyze images

---

## Alternative: Use Docker (No Tesseract Install Needed!)

If you don't want to install Tesseract on every machine, use Docker:

### Create Dockerfile:
```dockerfile
FROM python:3.11-slim

# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
```

### Build and Run:
```bash
docker build -t cyberbullying-detection .
docker run -p 5000:5000 cyberbullying-detection
```

Now you can run on **any laptop with Docker** - no Tesseract installation needed!

---

## Summary

**For Local Development:**
- ✅ Must install Tesseract on each laptop
- ✅ Must install Python dependencies
- ✅ Must configure Supabase (optional)

**For Production/Sharing:**
- ✅ Deploy once to Render/Railway
- ✅ Access from any device via URL
- ✅ No installation needed for users

**Recommended:** Deploy to cloud and share the URL! 🚀
