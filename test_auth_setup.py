"""
Test script to verify authentication setup
Run this to check if everything is configured correctly
"""

import sys

print("="*70)
print("AUTHENTICATION SETUP VERIFICATION")
print("="*70)
print()

# Check 1: Required packages
print("✓ Checking required packages...")
try:
    import flask
    print("  ✓ Flask installed")
except ImportError:
    print("  ✗ Flask not installed - run: pip install flask")
    sys.exit(1)

try:
    import jwt
    print("  ✓ PyJWT installed")
except ImportError:
    print("  ✗ PyJWT not installed - run: pip install pyjwt")
    sys.exit(1)

try:
    import requests
    print("  ✓ Requests installed")
except ImportError:
    print("  ✗ Requests not installed - run: pip install requests")
    sys.exit(1)

print()

# Check 2: Configuration file
print("✓ Checking Supabase configuration...")
try:
    from supabase_config import SUPABASE_URL, SUPABASE_KEY
    
    if SUPABASE_URL == "YOUR_SUPABASE_URL" or SUPABASE_KEY == "YOUR_SUPABASE_ANON_KEY":
        print("  ⚠ WARNING: Supabase credentials not configured!")
        print("  → Please update supabase_config.py with your actual credentials")
        print("  → See SUPABASE_SETUP_GUIDE.txt for instructions")
        print()
    elif not SUPABASE_URL or not SUPABASE_KEY:
        print("  ✗ Supabase credentials are empty")
        print("  → Please update supabase_config.py")
        sys.exit(1)
    else:
        print(f"  ✓ Supabase URL configured: {SUPABASE_URL[:30]}...")
        print(f"  ✓ Supabase Key configured: {SUPABASE_KEY[:20]}...")
        
        # Test connection
        print()
        print("✓ Testing Supabase connection...")
        try:
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/",
                headers={'apikey': SUPABASE_KEY}
            )
            if response.status_code in [200, 404]:  # 404 is ok, means API is reachable
                print("  ✓ Successfully connected to Supabase!")
            else:
                print(f"  ⚠ Unexpected response: {response.status_code}")
                print("  → Check your credentials in supabase_config.py")
        except Exception as e:
            print(f"  ✗ Connection failed: {e}")
            print("  → Check your internet connection and credentials")
            
except ImportError:
    print("  ✗ supabase_config.py not found!")
    print("  → Make sure the file exists in the project directory")
    sys.exit(1)

print()

# Check 3: Required files
print("✓ Checking required files...")
import os

required_files = [
    'app.py',
    'templates/index.html',
    'templates/login.html',
    'templates/signup.html',
    'supabase_config.py'
]

all_files_exist = True
for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING!")
        all_files_exist = False

if not all_files_exist:
    print()
    print("  Some required files are missing!")
    sys.exit(1)

print()

# Check 4: Dataset file
print("✓ Checking dataset...")
if os.path.exists('final_dataset_hinglish.csv'):
    print("  ✓ Dataset file found")
else:
    print("  ⚠ Dataset file not found - detection features may not work")

print()

# Summary
print("="*70)
print("SETUP VERIFICATION COMPLETE")
print("="*70)
print()

if SUPABASE_URL == "YOUR_SUPABASE_URL" or SUPABASE_KEY == "YOUR_SUPABASE_ANON_KEY":
    print("⚠ NEXT STEPS:")
    print("1. Follow SUPABASE_SETUP_GUIDE.txt to get your credentials")
    print("2. Update supabase_config.py with your actual Supabase URL and Key")
    print("3. Run this script again to verify")
    print("4. Start the app with: python app.py")
else:
    print("✓ Everything looks good!")
    print()
    print("READY TO START:")
    print("1. Run: python app.py")
    print("2. Open: http://127.0.0.1:5000")
    print("3. Sign up for a new account")
    print("4. Start detecting cyberbullying!")

print()
print("="*70)
