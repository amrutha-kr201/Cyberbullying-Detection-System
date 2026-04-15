# 🛡️ Cyberbullying Detection System

An AI-powered web application that detects cyberbullying in text and images using Machine Learning.

## ✨ Features

### User Features
- 📝 **Text Detection** - Analyze text for cyberbullying content
- 📸 **Image Detection** - Extract and analyze text from images using OCR
- 📊 **Dataset Testing** - Test the model on random dataset samples
- 👤 **User Authentication** - Secure login with name and Gmail
- 💾 **Results Tracking** - All detections are saved automatically

### Admin Features
- 📊 **Dashboard** - Comprehensive admin dashboard
- 👥 **User Management** - View, search, and delete users
- 🔍 **Detection History** - Monitor all detection attempts
- 📈 **Analytics** - View statistics and trends
  - Cyberbullying rate
  - Safe content rate
  - Daily activity stats
  - Text vs Image detection breakdown

## 🚀 Technology Stack

- **Backend**: Flask (Python)
- **Machine Learning**: Scikit-learn (Logistic Regression + TF-IDF)
- **OCR**: Tesseract
- **Authentication**: Session-based with separate admin login
- **Database**: JSON file storage
- **Frontend**: HTML, CSS, JavaScript

## 📋 Requirements

- Python 3.8+
- Tesseract OCR
- Flask
- scikit-learn
- pandas
- Pillow
- pytesseract
- PyJWT

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/amrutha-kr201/Cyberbullying-Detection-System.git
cd Cyberbullying-Detection-System
```

2. **Install Python dependencies**
```bash
pip install flask scikit-learn pandas pillow pytesseract pyjwt requests
```

3. **Install Tesseract OCR**
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Mac: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

4. **Configure Supabase (Optional)**
   - Create a Supabase account at [supabase.com](https://supabase.com)
   - Create a new project
   - Copy your Project URL and API Key
   - Create `supabase_config.py`:
   ```python
   SUPABASE_URL = "your-project-url"
   SUPABASE_KEY = "your-anon-key"
   ```

5. **Update Admin Credentials**
   - Open `app.py`
   - Change `ADMIN_USERNAME` and `ADMIN_PASSWORD`

## 🎯 Usage

### Quick Start (Launcher)

**Windows:**
```bash
start.bat
```
OR
```bash
python run.py
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```
OR
```bash
python3 run.py
```

This will show a menu where you can choose:
1. **Terminal Mode** - CLI interface for quick detection
2. **Website Mode** - Full web interface with authentication

### Manual Start

#### Terminal Mode (CLI)

```bash
python main.py
```

Features:
- Interactive menu
- Quick text detection
- Image detection from file path
- Dataset testing
- Results saved to files

#### Website Mode

```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`

### User Access

1. Go to `http://127.0.0.1:5000`
2. Sign up with your name and Gmail
3. Login with your credentials
4. Use the detection features:
   - **Check Text**: Enter text to analyze
   - **Check Image**: Upload an image with text
   - **Test Dataset**: Run tests on random samples

### Admin Access

1. Go to `http://127.0.0.1:5000/admin/login`
2. Login with admin credentials:
   - Username: `admin`
   - Password: (set in app.py)
3. Access the admin dashboard to:
   - View all users
   - Monitor detection history
   - View analytics and statistics
   - Manage users

## 📊 Model Information

- **Algorithm**: Logistic Regression
- **Vectorization**: TF-IDF (1000 features)
- **Accuracy**: 90.88%
- **Dataset**: Hinglish cyberbullying dataset (18,148 samples)
- **Training Split**: 80% train, 20% test

## 🔐 Security Features

- Separate admin and user authentication
- Session-based login
- Gmail validation for users
- Protected routes
- Admin-only dashboard access
- Password-based admin login

## 📁 Project Structure

```
cyberbullying/
├── app.py                          # Main Flask application
├── supabase_config.py              # Supabase credentials (not in repo)
├── final_dataset_hinglish.csv      # Training dataset
├── users.json                      # User database (auto-generated)
├── templates/
│   ├── index.html                  # Main detection page
│   ├── login.html                  # User login page
│   ├── signup.html                 # User signup page
│   ├── admin_login.html            # Admin login page
│   └── admin.html                  # Admin dashboard
├── uploads/                        # Temporary image storage
├── results/                        # Detection results
└── README.md                       # This file
```

## 🎨 Screenshots

### User Interface
- Modern purple gradient design
- Responsive layout
- Three detection methods
- Real-time results with confidence scores

### Admin Dashboard
- Statistics overview
- User management table
- Detection history
- Analytics with charts

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👥 Authors

- Amrutha KR

## 🙏 Acknowledgments

- Dataset: Hinglish Cyberbullying Dataset
- OCR: Tesseract OCR Engine
- ML Framework: Scikit-learn
- Web Framework: Flask

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for a safer internet**
