import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import os
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("Image Cyberbullying Detection - Test Mode")
print("="*70)

# Train model
print("\nTraining model...")
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
print("✓ Model trained!")

# Setup Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

print("\n" + "="*70)
print("Testing Your Image")
print("="*70)

# Find images
images = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if images:
    for img_file in images:
        print(f"\nProcessing: {img_file}")
        print("-"*70)
        
        try:
            img = Image.open(img_file)
            print(f"✓ Image loaded: {img.size[0]}x{img.size[1]} pixels")
            
            # Try different OCR configurations
            configs = [
                '--psm 6',  # Assume uniform block of text
                '--psm 3',  # Fully automatic page segmentation
                '--psm 11', # Sparse text
                '--psm 12', # Sparse text with OSD
            ]
            
            best_text = ""
            for config in configs:
                text = pytesseract.image_to_string(img, config=config).strip()
                if len(text) > len(best_text):
                    best_text = text
            
            if best_text:
                print(f"\n✓ Text extracted ({len(best_text)} characters):")
                print(f"   \"{best_text[:200]}...\"" if len(best_text) > 200 else f"   \"{best_text}\"")
                
                # Check for cyberbullying
                text_vec = vectorizer.transform([best_text])
                prediction = model.predict(text_vec)[0]
                probability = model.predict_proba(text_vec)[0]
                
                if prediction == 1:
                    result = "⚠️  CYBERBULLYING DETECTED"
                    conf = probability[1]
                else:
                    result = "✓ SAFE"
                    conf = probability[0]
                
                print(f"\n   Result: {result}")
                print(f"   Confidence: {conf:.2%}")
            else:
                print("\n⚠️  No text could be extracted from this image")
                print("\nPossible reasons:")
                print("   - Image doesn't contain text")
                print("   - Text is too small or blurry")
                print("   - Image is a graphic/logo")
                print("\nTips:")
                print("   - Use screenshots with clear text")
                print("   - Ensure text is readable")
                print("   - Try a different image")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

print("\n" + "="*70)
print("Manual Text Input Mode")
print("="*70)
print("\nYou can also test by typing text directly:")

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

print("\n✓ Done!")
