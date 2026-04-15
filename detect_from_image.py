import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from PIL import Image
import pytesseract
import os
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("Cyberbullying Detection from Images")
print("="*70)

# ============================================================
# STEP 1: Train the Model
# ============================================================
print("\n[1/3] Training the model...")
CSV_FILE = 'final_dataset_hinglish.csv'
TEXT_COLUMN = 'Unnamed: 0'
LABEL_COLUMN = 'label'

df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
df = df[[TEXT_COLUMN, LABEL_COLUMN]].copy()
df[LABEL_COLUMN] = df[LABEL_COLUMN].replace(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(
    df[TEXT_COLUMN], df[LABEL_COLUMN], 
    test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

print("✓ Model trained successfully!")

# ============================================================
# STEP 2: Setup Tesseract OCR
# ============================================================
print("\n[2/3] Setting up OCR...")

# Try to find Tesseract installation
tesseract_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\navee\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
]

tesseract_found = False
for path in tesseract_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        tesseract_found = True
        print(f"✓ Tesseract found at: {path}")
        break

if not tesseract_found:
    print("\n⚠️  WARNING: Tesseract OCR not found!")
    print("\nTo use image detection, please install Tesseract OCR:")
    print("1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
    print("2. Install it")
    print("3. Run this script again")
    print("\nFor now, I'll show you how to use it with manual text input...")
    
    # Manual text input mode
    print("\n" + "="*70)
    print("[3/3] Manual Text Input Mode")
    print("="*70)
    
    while True:
        print("\nEnter text to check (or 'quit' to exit):")
        user_text = input("> ")
        
        if user_text.lower() == 'quit':
            break
        
        if user_text.strip():
            text_vec = vectorizer.transform([user_text])
            prediction = model.predict(text_vec)[0]
            probability = model.predict_proba(text_vec)[0]
            
            if prediction == 1:
                result = "⚠️  CYBERBULLYING DETECTED"
                conf = probability[1]
            else:
                result = "✓ SAFE"
                conf = probability[0]
            
            print(f"\nResult: {result}")
            print(f"Confidence: {conf:.2%}")
    
    exit()

# ============================================================
# STEP 3: Process Images
# ============================================================
print("\n[3/3] Ready to process images!")
print("="*70)

def extract_text_from_image(image_path):
    """Extract text from image using OCR"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def check_cyberbullying(text):
    """Check if text contains cyberbullying"""
    if not text or text.startswith("Error"):
        return None, None, text
    
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0]
    
    if prediction == 1:
        result = "⚠️  CYBERBULLYING DETECTED"
        conf = probability[1]
    else:
        result = "✓ SAFE"
        conf = probability[0]
    
    return result, conf, text

# Check for images in current directory
print("\nLooking for images in current directory...")
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
images = [f for f in os.listdir('.') if os.path.splitext(f)[1].lower() in image_extensions]

if images:
    print(f"✓ Found {len(images)} image(s)")
    print("\nProcessing images:")
    print("-"*70)
    
    for i, img_file in enumerate(images, 1):
        print(f"\n{i}. Processing: {img_file}")
        
        # Extract text
        extracted_text = extract_text_from_image(img_file)
        
        if not extracted_text:
            print("   ⚠️  No text found in image")
            continue
        
        # Check for cyberbullying
        result, confidence, text = check_cyberbullying(extracted_text)
        
        if result:
            print(f"   Extracted Text: \"{text[:100]}...\"" if len(text) > 100 else f"   Extracted Text: \"{text}\"")
            print(f"   Result: {result}")
            print(f"   Confidence: {confidence:.2%}")
        else:
            print(f"   ⚠️  Could not process: {text}")
else:
    print("⚠️  No images found in current directory")
    print("\nTo test with an image:")
    print("1. Place an image file (jpg, png, etc.) in this folder")
    print("2. Run this script again")
    
    # Manual input mode
    print("\n" + "="*70)
    print("Manual Text Input Mode")
    print("="*70)
    print("\nYou can test by typing text manually:")
    
    while True:
        print("\nEnter text to check (or 'quit' to exit):")
        user_text = input("> ")
        
        if user_text.lower() == 'quit':
            break
        
        if user_text.strip():
            result, confidence, _ = check_cyberbullying(user_text)
            if result:
                print(f"\nResult: {result}")
                print(f"Confidence: {confidence:.2%}")

print("\n" + "="*70)
print("✓ COMPLETED!")
print("="*70)
