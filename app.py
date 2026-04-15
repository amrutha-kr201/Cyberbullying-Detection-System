from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from PIL import Image
import pytesseract
import os
from datetime import datetime
import warnings
import requests
import jwt
import json
from functools import wraps
warnings.filterwarnings('ignore')

# Import Supabase config
try:
    from supabase_config import SUPABASE_URL, SUPABASE_KEY
except ImportError:
    print("WARNING: supabase_config.py not found or not configured!")
    SUPABASE_URL = None
    SUPABASE_KEY = None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())

# Create necessary folders
os.makedirs('uploads', exist_ok=True)
os.makedirs('results', exist_ok=True)

# Simple user database (stored in file)
USERS_FILE = 'users.json'

# Admin credentials (change these!)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@3117')

def load_users():
    """Load users from file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def user_exists(email):
    """Check if user exists"""
    users = load_users()
    return email.lower() in users

def register_user(name, email):
    """Register a new user"""
    users = load_users()
    users[email.lower()] = {
        'name': name,
        'email': email,
        'registered_at': datetime.now().isoformat()
    }
    save_users(users)

def get_user(email):
    """Get user by email"""
    users = load_users()
    return users.get(email.lower())

def is_admin():
    """Check if current user is admin"""
    return session.get('is_admin', False)

def load_detections():
    """Load all detections from results file"""
    detections = []
    results_file = f"results/web_results_{datetime.now().strftime('%Y%m%d')}.txt"
    
    if not os.path.exists(results_file):
        return detections
    
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            content = f.read()
            entries = content.split('='*70)
            
            for entry in entries:
                if not entry.strip():
                    continue
                
                lines = entry.strip().split('\n')
                detection = {}
                
                for line in lines:
                    if line.startswith('Timestamp:'):
                        detection['timestamp'] = line.replace('Timestamp:', '').strip()
                    elif line.startswith('User:'):
                        user_info = line.replace('User:', '').strip()
                        if '(' in user_info:
                            name = user_info.split('(')[0].strip()
                            email = user_info.split('(')[1].replace(')', '').strip()
                            detection['user_name'] = name
                            detection['user_email'] = email
                    elif line.startswith('Source:'):
                        detection['source'] = line.replace('Source:', '').strip()
                    elif line.startswith('Text:'):
                        detection['text'] = line.replace('Text:', '').strip()
                    elif line.startswith('Result:'):
                        detection['result'] = line.replace('Result:', '').strip()
                    elif line.startswith('Confidence:'):
                        detection['confidence'] = line.replace('Confidence:', '').strip()
                
                if detection and 'timestamp' in detection:
                    detections.append(detection)
    
    except Exception as e:
        print(f"Error loading detections: {e}")
    
    return detections

# Setup Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Train model on startup
print("Loading and training model...")
df = pd.read_csv('final_dataset_hinglish.csv', on_bad_lines='skip')
df = df[['Unnamed: 0', 'label']].copy()
df['label'] = df['label'].replace(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(
    df['Unnamed: 0'], df['label'], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

print("Model trained successfully!")

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Supabase Auth Helper Functions
def supabase_signup(email, password, name):
    """Sign up a new user with Supabase"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return {'error': 'Supabase not configured'}, 500
    
    url = f"{SUPABASE_URL}/auth/v1/signup"
    headers = {
        'apikey': SUPABASE_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'email': email,
        'password': password,
        'data': {
            'name': name
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json(), response.status_code
    except Exception as e:
        return {'error': str(e)}, 500

def supabase_login(email, password):
    """Login user with Supabase"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return {'error': 'Supabase not configured'}, 500
    
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {
        'apikey': SUPABASE_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'email': email,
        'password': password
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json(), response.status_code
    except Exception as e:
        return {'error': str(e)}, 500

def save_detection_history(user_id, text, result, confidence, source_type):
    """Save detection history to Supabase database"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return
    
    url = f"{SUPABASE_URL}/rest/v1/detection_history"
    headers = {
        'apikey': SUPABASE_KEY,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    data = {
        'user_id': user_id,
        'text': text[:500],  # Limit text length
        'result': result,
        'confidence': confidence,
        'source_type': source_type,
        'created_at': datetime.now().isoformat()
    }
    
    try:
        requests.post(url, json=data, headers=headers)
    except Exception as e:
        print(f"Failed to save history: {e}")


def save_result(text, result, confidence, source_type):
    """Save result to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"results/web_results_{datetime.now().strftime('%Y%m%d')}.txt"
    
    user_info = ""
    if 'user' in session:
        user_info = f"User: {session['user']['name']} ({session['user']['email']})\n"
    
    with open(filename, 'a', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(user_info)
        f.write(f"Source: {source_type}\n")
        f.write(f"Text: {text[:200]}...\n" if len(text) > 200 else f"Text: {text}\n")
        f.write(f"Result: {result}\n")
        f.write(f"Confidence: {confidence:.2%}\n")
        f.write("="*70 + "\n\n")

# Authentication Routes
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/api/signup', methods=['POST'])
def api_signup():
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        
        if not email or not name:
            return jsonify({'error': 'Name and email are required'}), 400
        
        # Validate email is Gmail
        if not email.lower().endswith('@gmail.com'):
            return jsonify({'error': 'Please use a Gmail address'}), 400
        
        # Check if user already exists
        if user_exists(email):
            return jsonify({'error': 'This email is already registered. Please login instead.'}), 400
        
        # Register new user
        register_user(name, email)
        
        # Store user in session
        session['user'] = {
            'email': email,
            'name': name
        }
        
        return jsonify({'message': 'Account created successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        
        if not email or not name:
            return jsonify({'error': 'Name and email are required'}), 400
        
        # Validate email is Gmail
        if not email.lower().endswith('@gmail.com'):
            return jsonify({'error': 'Please use a Gmail address'}), 400
        
        # Check if user exists
        if not user_exists(email):
            return jsonify({'error': 'User not found. Please sign up first.'}), 404
        
        # Get user data
        user_data = get_user(email)
        
        # Verify name matches
        if user_data['name'].lower() != name.lower():
            return jsonify({'error': 'Name does not match our records'}), 401
        
        # Store user in session
        session['user'] = {
            'email': email,
            'name': user_data['name']
        }
        
        return jsonify({'message': 'Login successful'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/check_auth')
def check_auth():
    # If admin is logged in, return not authenticated for user pages
    if is_admin():
        return jsonify({'authenticated': False}), 401
    
    if 'user' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'email': session['user']['email'],
                'name': session['user'].get('name', '')
            }
        }), 200
    else:
        return jsonify({'authenticated': False}), 401


@app.route('/')
def index():
    # Check if user is logged in, if not redirect to login
    if 'user' not in session:
        return redirect(url_for('login_page'))
    
    # If admin is logged in, redirect to admin dashboard
    if is_admin():
        return redirect(url_for('admin_dashboard'))
    
    return render_template('index.html')

@app.route('/check_text', methods=['POST'])
@login_required
def check_text():
    # Block admin from using detection features
    if is_admin():
        return jsonify({'error': 'Admin cannot use detection features'}), 403
    
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Please enter some text'}), 400
        
        # Predict
        text_vec = vectorizer.transform([text])
        prediction = model.predict(text_vec)[0]
        probability = model.predict_proba(text_vec)[0]
        
        if prediction == 1:
            result = "CYBERBULLYING DETECTED"
            result_type = "danger"
            conf = probability[1]
        else:
            result = "SAFE"
            result_type = "success"
            conf = probability[0]
        
        # Save result
        save_result(text, result, conf, "Text Input")
        
        return jsonify({
            'result': result,
            'result_type': result_type,
            'confidence': f"{conf:.2%}",
            'text': text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check_image', methods=['POST'])
@login_required
def check_image():
    # Block admin from using detection features
    if is_admin():
        return jsonify({'error': 'Admin cannot use detection features'}), 403
    
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Save uploaded file
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from image
        img = Image.open(filepath)
        configs = ['--psm 6', '--psm 3', '--psm 11']
        best_text = ""
        
        for config in configs:
            text = pytesseract.image_to_string(img, config=config).strip()
            if len(text) > len(best_text):
                best_text = text
        
        if not best_text:
            return jsonify({'error': 'No text found in image'}), 400
        
        # Predict
        text_vec = vectorizer.transform([best_text])
        prediction = model.predict(text_vec)[0]
        probability = model.predict_proba(text_vec)[0]
        
        if prediction == 1:
            result = "CYBERBULLYING DETECTED"
            result_type = "danger"
            conf = probability[1]
        else:
            result = "SAFE"
            result_type = "success"
            conf = probability[0]
        
        # Save result
        save_result(best_text, result, conf, "Image Upload")
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'result': result,
            'result_type': result_type,
            'confidence': f"{conf:.2%}",
            'text': best_text[:200] + "..." if len(best_text) > 200 else best_text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check_dataset', methods=['GET'])
@login_required
def check_dataset():
    # Block admin from using detection features
    if is_admin():
        return jsonify({'error': 'Admin cannot use detection features'}), 403
    
    try:
        # Get 10 random samples
        random_samples = df.sample(n=10, random_state=None)
        results = []
        correct = 0
        
        for idx, row in random_samples.iterrows():
            text = row['Unnamed: 0']
            actual_label = row['label']
            
            text_vec = vectorizer.transform([text])
            prediction = model.predict(text_vec)[0]
            probability = model.predict_proba(text_vec)[0]
            
            actual = "CYBERBULLYING" if actual_label == 1 else "SAFE"
            predicted = "CYBERBULLYING" if prediction == 1 else "SAFE"
            conf = probability[1] if prediction == 1 else probability[0]
            
            is_correct = actual_label == prediction
            correct += is_correct
            
            results.append({
                'text': text[:100] + "..." if len(text) > 100 else text,
                'actual': actual,
                'predicted': predicted,
                'confidence': f"{conf:.2%}",
                'correct': bool(is_correct)  # Convert to Python bool
            })
        
        return jsonify({
            'results': results,
            'accuracy': f"{correct}/10 ({correct*10}%)"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin Routes
@app.route('/admin/login')
def admin_login_page():
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_api():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Check admin credentials
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            session['admin_user'] = username
            return jsonify({'message': 'Admin login successful'}), 200
        else:
            return jsonify({'error': 'Invalid admin credentials'}), 401
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('admin_login_page'))
    return render_template('admin.html')

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('is_admin', None)
    session.pop('admin_user', None)
    return jsonify({'message': 'Admin logged out successfully'}), 200

@app.route('/admin/api/dashboard')
def admin_api_dashboard():
    if not is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        # Load users
        users = load_users()
        users_list = [
            {
                'name': user_data['name'],
                'email': user_data['email'],
                'registered_at': user_data['registered_at']
            }
            for email, user_data in users.items()
        ]
        
        # Load detections
        detections = load_detections()
        
        # Calculate stats
        total_users = len(users)
        total_detections = len(detections)
        cyberbullying_count = sum(1 for d in detections if 'CYBERBULLYING' in d.get('result', ''))
        safe_count = total_detections - cyberbullying_count
        
        # Debug logging
        print(f"DEBUG: Total detections: {total_detections}")
        print(f"DEBUG: Cyberbullying count: {cyberbullying_count}")
        print(f"DEBUG: Safe count: {safe_count}")
        for d in detections:
            print(f"DEBUG: Detection result: '{d.get('result', 'NO RESULT')}'")
        
        # Analytics
        detection_rate = round((cyberbullying_count / total_detections * 100) if total_detections > 0 else 0, 1)
        safe_rate = round((safe_count / total_detections * 100) if total_detections > 0 else 0, 1)
        
        # Most active user
        user_detection_counts = {}
        for det in detections:
            user_email = det.get('user_email', 'Unknown')
            user_detection_counts[user_email] = user_detection_counts.get(user_email, 0) + 1
        
        most_active_user = None
        most_active_count = 0
        if user_detection_counts:
            most_active_email = max(user_detection_counts, key=user_detection_counts.get)
            most_active_count = user_detection_counts[most_active_email]
            user_data = users.get(most_active_email)
            if user_data:
                most_active_user = user_data['name']
        
        # Count by source
        text_detections = sum(1 for d in detections if d.get('source') == 'Text Input')
        image_detections = sum(1 for d in detections if d.get('source') == 'Image Upload')
        
        # Daily stats (last 7 days)
        daily_stats = []
        from collections import defaultdict
        daily_counts = defaultdict(lambda: {'total': 0, 'cyberbullying': 0, 'safe': 0})
        
        for det in detections:
            try:
                timestamp = det.get('timestamp', '')
                date = timestamp.split(' ')[0] if timestamp else 'Unknown'
                daily_counts[date]['total'] += 1
                if 'CYBERBULLYING' in det.get('result', ''):
                    daily_counts[date]['cyberbullying'] += 1
                else:
                    daily_counts[date]['safe'] += 1
            except:
                pass
        
        for date, counts in sorted(daily_counts.items(), reverse=True)[:7]:
            daily_stats.append({
                'date': date,
                'total': counts['total'],
                'cyberbullying': counts['cyberbullying'],
                'safe': counts['safe']
            })
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'total_detections': total_detections,
                'cyberbullying_count': cyberbullying_count,
                'safe_count': safe_count
            },
            'users': users_list,
            'detections': detections,
            'analytics': {
                'detection_rate': detection_rate,
                'safe_rate': safe_rate,
                'most_active_user': most_active_user,
                'most_active_count': most_active_count,
                'text_detections': text_detections,
                'image_detections': image_detections,
                'daily_stats': daily_stats
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/delete_user', methods=['POST'])
def admin_delete_user():
    if not is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email required'}), 400
        
        # Don't allow deleting admin
        if email.lower() == ADMIN_EMAIL.lower():
            return jsonify({'error': 'Cannot delete admin user'}), 400
        
        users = load_users()
        if email.lower() in users:
            del users[email.lower()]
            save_users(users)
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("Starting Cyberbullying Detection Web Server...")
    print("="*70)
    print("\nOpen your browser and go to: http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
