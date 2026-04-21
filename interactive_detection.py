import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from PIL import Image
import pytesseract
import os
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("Interactive Cyberbullying Detection System")
print("="*70)

# Train model
print("\n[1/2] Training model...")
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
print("✓ Model trained successfully!")

# Setup Tesseract
print("\n[2/2] Setting up OCR...")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
print("✓ OCR ready!")

def check_text(text):
    """Check if text contains cyberbullying"""
    if not text.strip():
        return None, None
    
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0]
    
    if prediction == 1:
        result = "⚠️  CYBERBULLYING DETECTED"
        conf = probability[1]
    else:
        result = "✓ SAFE"
        conf = probability[0]
    
    return result, conf

def process_image(image_path):
    """Extract text from image and check for cyberbullying"""
    try:
        if not os.path.exists(image_path):
            print(f"\n❌ Error: File not found: {image_path}")
            return
        
        print(f"\n📸 Processing image: {os.path.basename(image_path)}")
        print("-"*70)
        
        img = Image.open(image_path)
        print(f"✓ Image loaded: {img.size[0]}x{img.size[1]} pixels")
        
        # Extract text with multiple configurations
        print("✓ Extracting text...")
        configs = ['--psm 6', '--psm 3', '--psm 11']
        best_text = ""
        
        for config in configs:
            text = pytesseract.image_to_string(img, config=config).strip()
            if len(text) > len(best_text):
                best_text = text
        
        if best_text:
            print(f"\n📝 Extracted Text:")
            print(f"   \"{best_text[:150]}...\"" if len(best_text) > 150 else f"   \"{best_text}\"")
            
            result, conf = check_text(best_text)
            if result:
                print(f"\n🔍 Analysis Result:")
                print(f"   {result}")
                print(f"   Confidence: {conf:.2%}")
        else:
            print("\n⚠️  No text found in image")
            print("   Try an image with clear, readable text")
            
    except Exception as e:
        print(f"\n❌ Error processing image: {str(e)}")

# Main interactive loop
print("\n" + "="*70)
print("Interactive Mode - Choose an option:")
print("="*70)

while True:
    print("\n" + "="*70)
    print("What would you like to do?")
    print("="*70)
    print("1. Check image (provide image path)")
    print("2. Check text (type or paste text)")
    print("3. Exit")
    print("-"*70)
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == '1':
        print("\n📁 Enter image path:")
        print("   Examples:")
        print("   - C:\\Users\\navee\\Downloads\\screenshot.png")
        print("   - screenshot.png (if in current folder)")
        print("   - Drag and drop image here")
        print()
        
        image_path = input("Image path: ").strip().strip('"').strip("'")
        
        if image_path:
            process_image(image_path)
        else:
            print("❌ No path provided")
    
    elif choice == '2':
        print("\n📝 Enter text to check:")
        user_text = input("> ").strip()
        
        if user_text:
            result, conf = check_text(user_text)
            if result:
                print(f"\n🔍 Analysis Result:")
                print(f"   {result}")
                print(f"   Confidence: {conf:.2%}")
        else:
            print("❌ No text provided")
    
    elif choice == '3':
        print("\n👋 Thank you for using Cyberbullying Detection System!")
        print("="*70)
        break
    
    else:
        print("\n❌ Invalid choice. Please enter 1, 2, or 3")

print("\n✓ Program ended")
