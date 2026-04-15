# 🔐 Cyberbullying Detection System - Authentication

Your Cyberbullying Detection System now includes **user authentication** powered by Supabase!

## 🎯 What's New?

- ✅ **User Registration** - Sign up with email and password
- ✅ **Secure Login** - JWT-based authentication
- ✅ **Session Management** - Stay logged in across requests
- ✅ **Protected Routes** - Only authenticated users can access detection features
- ✅ **User Profile Display** - See who's logged in
- ✅ **Logout Functionality** - Secure logout
- ✅ **Detection History** - (Optional) Track user's detection history in database

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install pyjwt
```

### 2. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Get your **Project URL** and **API Key** from Settings → API
4. Update `supabase_config.py`:

```python
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
```

### 3. Verify Setup

```bash
python test_auth_setup.py
```

### 4. Start the Application

```bash
python app.py
```

### 5. Access the System

Open your browser and go to: **http://127.0.0.1:5000**

You'll be redirected to the login page. Click **Sign Up** to create your account!

## 📖 Detailed Setup Guide

For step-by-step instructions, see **SUPABASE_SETUP_GUIDE.txt**

## 🎨 User Interface

### Login Page
- Clean, modern design with purple gradient
- Email and password fields
- Link to sign up page
- Error messages for invalid credentials

### Sign Up Page
- Full name, email, and password fields
- Password confirmation
- Minimum 6 character password requirement
- Link back to login page

### Main Page (After Login)
- User name displayed in top-right corner
- Logout button
- All detection features available:
  - 📝 Check Text
  - 📸 Check Image
  - 📊 Test Dataset

## 🔒 Security Features

- **Password Hashing** - Passwords are securely hashed by Supabase
- **JWT Tokens** - Secure token-based authentication
- **Session Management** - Server-side session storage
- **Protected Routes** - Unauthorized users are redirected to login
- **HTTPS Ready** - Designed for secure production deployment

## 🛠️ Technical Details

### Authentication Flow

```
1. User visits site → Check if logged in
2. Not logged in → Redirect to /login
3. User signs up → Account created in Supabase
4. User logs in → JWT token received
5. Token stored in session → Access granted
6. User can access all features
7. User logs out → Session cleared
```

### API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/login` | GET | Login page | No |
| `/signup` | GET | Sign up page | No |
| `/api/signup` | POST | Create account | No |
| `/api/login` | POST | Login user | No |
| `/api/logout` | POST | Logout user | Yes |
| `/api/check_auth` | GET | Check auth status | No |
| `/` | GET | Main page | Yes |
| `/check_text` | POST | Analyze text | Yes |
| `/check_image` | POST | Analyze image | Yes |
| `/check_dataset` | GET | Test dataset | Yes |

### File Structure

```
cyberbullying/
├── app.py                          # Main Flask app with auth
├── supabase_config.py              # Supabase credentials
├── templates/
│   ├── index.html                  # Main page (protected)
│   ├── login.html                  # Login page
│   └── signup.html                 # Sign up page
├── SUPABASE_SETUP_GUIDE.txt        # Detailed setup instructions
├── AUTHENTICATION_GUIDE.txt        # Quick reference
├── README_AUTHENTICATION.md        # This file
└── test_auth_setup.py              # Setup verification script
```

## 📊 Optional: Detection History Database

To track user detection history in Supabase:

1. Go to SQL Editor in Supabase dashboard
2. Run this SQL:

```sql
CREATE TABLE detection_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL,
    text TEXT NOT NULL,
    result TEXT NOT NULL,
    confidence FLOAT NOT NULL,
    source_type TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE detection_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can insert their own detection history"
ON detection_history FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own detection history"
ON detection_history FOR SELECT
USING (auth.uid() = user_id);
```

This will automatically save each detection to the database!

## 🐛 Troubleshooting

### "Supabase not configured" error
- Update `supabase_config.py` with your actual credentials
- Run `python test_auth_setup.py` to verify

### Can't create account
- Check if email is valid
- Ensure password is at least 6 characters
- Check Supabase dashboard for error logs

### Logged out automatically
- Normal behavior when server restarts
- Sessions are cleared on restart

### Login page doesn't load
- Make sure Flask app is running: `python app.py`
- Check if port 5000 is available

## 🚀 Production Deployment

Before deploying to production:

1. **Change SECRET_KEY** in `app.py` to a random secure string
2. **Use environment variables** for credentials:
   ```python
   import os
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
   SUPABASE_URL = os.environ.get('SUPABASE_URL')
   SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
   ```
3. **Enable HTTPS** for secure communication
4. **Enable email confirmation** in Supabase settings
5. **Add rate limiting** to prevent abuse
6. **Set up error logging**
7. **Add CSRF protection**

## 📚 Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [JWT Documentation](https://jwt.io/)

## 🎉 Features Summary

| Feature | Status |
|---------|--------|
| User Registration | ✅ Working |
| User Login | ✅ Working |
| Session Management | ✅ Working |
| Protected Routes | ✅ Working |
| User Info Display | ✅ Working |
| Logout | ✅ Working |
| Detection History | ✅ Optional |
| Email Confirmation | ⚠️ Configure in Supabase |
| Password Reset | ⚠️ Can be added |
| User Dashboard | ⚠️ Can be added |

## 💡 Next Steps

1. Test the authentication system thoroughly
2. Customize the UI to match your brand
3. Add email confirmation for production
4. Consider adding a user dashboard to view detection history
5. Add password reset functionality
6. Implement user profile editing

## 🤝 Support

If you need help:
1. Check **SUPABASE_SETUP_GUIDE.txt** for detailed instructions
2. Check **AUTHENTICATION_GUIDE.txt** for quick reference
3. Run `python test_auth_setup.py` to diagnose issues
4. Check Supabase dashboard for error logs

---

**Enjoy your secure Cyberbullying Detection System! 🛡️**
