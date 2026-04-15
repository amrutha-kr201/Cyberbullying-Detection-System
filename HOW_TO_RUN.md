# 🚀 How to Run the Project

## Quick Start

### Option 1: Use the Launcher (Recommended)

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Or directly:**
```bash
python run.py
```

This will show you a menu:
```
╔═══════════════════════════════════════════════════════════════╗
║        🛡️  CYBERBULLYING DETECTION SYSTEM 🛡️                 ║
╚═══════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────┐
│                      SELECT MODE                              │
├───────────────────────────────────────────────────────────────┤
│  1. 💻 Terminal Mode (CLI)                                    │
│  2. 🌐 Website Mode (Web Interface)                           │
│  3. ❌ Exit                                                    │
└───────────────────────────────────────────────────────────────┘
```

---

## Mode 1: Terminal Mode (CLI)

### What is it?
- Command-line interface
- No browser needed
- Quick and simple
- Perfect for testing

### How to run:
```bash
python main.py
```

### Features:
```
1. Check with Dataset - Test 10 random samples
2. Check with Custom Text - Enter your own text
3. Check with Image - Provide image file path
4. Exit
```

### Example Usage:

**Check Text:**
```
Enter your choice (1-4): 2
Enter text to check: You are stupid and worthless
```

**Output:**
```
⚠️  CYBERBULLYING DETECTED
Confidence: 95.60%
```

**Check Image:**
```
Enter your choice (1-4): 3
Enter image path: C:\Users\navee\image.png
```

**Output:**
```
Extracted Text: "You are ugly"
⚠️  CYBERBULLYING DETECTED
Confidence: 87.32%
```

### Results:
- Saved to `results/detection_results_YYYYMMDD.txt`
- Includes timestamp, text, result, confidence

---

## Mode 2: Website Mode (Web Interface)

### What is it?
- Full web application
- Beautiful UI
- User authentication
- Admin dashboard

### How to run:
```bash
python app.py
```

### Access:
- **Main Site:** http://127.0.0.1:5000
- **User Login:** http://127.0.0.1:5000/login
- **Admin Login:** http://127.0.0.1:5000/admin/login

### User Features:

#### 1. Sign Up
- Go to http://127.0.0.1:5000
- Click "Sign Up"
- Enter name and Gmail
- Create account

#### 2. Login
- Enter name and Gmail
- Access detection features

#### 3. Detection Methods

**📝 Check Text:**
- Enter text in textarea
- Click "Analyze Text"
- See result with confidence

**📸 Check Image:**
- Upload image (drag & drop or click)
- Click "Analyze Image"
- See extracted text and result

**📊 Test Dataset:**
- Click "Run Test"
- See 10 random samples tested
- View accuracy statistics

### Admin Features:

#### Access Admin Dashboard:
1. Go to http://127.0.0.1:5000/admin/login
2. Login:
   - Username: `admin`
   - Password: `Admin@3117`

#### Dashboard Features:

**📊 Statistics:**
- Total Users
- Total Detections
- Cyberbullying Found
- Safe Content

**👥 Users Tab:**
- View all registered users
- Search users
- Delete users
- View user details

**🔍 Detection History Tab:**
- View all detections
- Filter by text or user
- See results and confidence
- Color-coded (red=cyberbullying, green=safe)

**📈 Analytics Tab:**
- Cyberbullying rate
- Safe content rate
- Total detections breakdown
- Daily activity stats

---

## Comparison: Terminal vs Website

| Feature | Terminal Mode | Website Mode |
|---------|--------------|--------------|
| **Interface** | Command-line | Web browser |
| **Authentication** | None | Required |
| **User Management** | No | Yes |
| **Admin Dashboard** | No | Yes |
| **Image Upload** | File path | Drag & drop |
| **Results Display** | Text output | Beautiful UI |
| **Multi-user** | No | Yes |
| **History Tracking** | File only | File + Database |
| **Best For** | Quick testing | Production use |

---

## When to Use Each Mode

### Use Terminal Mode When:
- ✅ Quick testing
- ✅ No need for authentication
- ✅ Single user
- ✅ Command-line preference
- ✅ Automated scripts

### Use Website Mode When:
- ✅ Multiple users
- ✅ Need authentication
- ✅ Want admin dashboard
- ✅ Better user experience
- ✅ Production deployment
- ✅ Sharing with others

---

## Switching Between Modes

You can run both modes, but not simultaneously on the same port.

**To switch:**
1. Stop current mode (Ctrl+C)
2. Run the other mode
3. Or use the launcher (run.py) to switch easily

---

## Troubleshooting

### Issue: Port 5000 already in use (Website Mode)

**Solution 1:** Stop the other process
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

**Solution 2:** Change port in app.py
```python
app.run(debug=False, host='0.0.0.0', port=8000)
```

### Issue: Tesseract not found

**Solution:** Install Tesseract OCR
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Mac: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

### Issue: Module not found

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Dataset file not found

**Solution:** Make sure `final_dataset_hinglish.csv` is in the project directory

---

## Running Both Modes (Advanced)

If you want to run both simultaneously:

### Terminal Mode:
```bash
python main.py
```
(Runs in terminal, no port needed)

### Website Mode on Different Port:
Edit `app.py` line 685:
```python
app.run(debug=False, host='0.0.0.0', port=8000)
```

Then run:
```bash
python app.py
```

Access website at: http://127.0.0.1:8000

---

## Keyboard Shortcuts

### Terminal Mode:
- `Ctrl+C` - Exit program
- `1-4` - Menu selection

### Website Mode:
- `Ctrl+C` - Stop server
- `F5` - Refresh page
- `Ctrl+Shift+R` - Hard refresh

---

## Tips & Best Practices

### Terminal Mode:
1. Use absolute paths for images
2. Results auto-save to `results/` folder
3. Check results file for history
4. Good for batch processing

### Website Mode:
1. Sign up before using
2. Admin login is separate
3. Results saved per user
4. Use admin dashboard for monitoring
5. Logout when done

---

## Examples

### Terminal Mode Example Session:
```bash
$ python main.py

╔═══════════════════════════════════════════════════════════════╗
║        🛡️  CYBERBULLYING DETECTION SYSTEM 🛡️                 ║
╚═══════════════════════════════════════════════════════════════╝

1. Check with Dataset
2. Check with Custom Text
3. Check with Image
4. Exit

Enter your choice (1-4): 2
Enter text to check: Have a great day!

✓ SAFE
Confidence: 86.55%

Result saved to: results/detection_results_20260415.txt
```

### Website Mode Example:
```bash
$ python app.py

======================================================================
Starting Cyberbullying Detection Web Server...
======================================================================

Open your browser and go to: http://127.0.0.1:5000

Press Ctrl+C to stop the server
======================================================================

 * Running on http://0.0.0.0:5000
```

Then open browser and use the web interface!

---

## Summary

**Quick Start:**
```bash
python run.py
```

**Terminal Mode:**
```bash
python main.py
```

**Website Mode:**
```bash
python app.py
```

Choose the mode that fits your needs! 🚀
