import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from PIL import Image
import pytesseract
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Create results folder if it doesn't exist
if not os.path.exists('results'):
    os.makedirs('results')

print("="*70)
print("        CYBERBULLYING DETECTION SYSTEM")
print("="*70)

# Train model
print("\n⏳ Loading and training model...")
df = pd.read_csv('final_dataset_hinglish.csv', on_bad_lines='skip')
df = df[['Unnamed: 0', 'label']].copy()
df['label'] = df['label'].replace(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(
    df['Unnamed: 0'], df['label'], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)

print(f"✓ Model trained successfully!")
print(f"✓ Accuracy: {accuracy:.2%}")
print(f"✓ Dataset: {len(df)} samples")

# Setup Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def save_result(text, result, confidence, source_type, source_info=""):
    """Save result to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"results/detection_results_{datetime.now().strftime('%Y%m%d')}.txt"
    
    with open(filename, 'a', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Source: {source_type}\n")
        if source_info:
            f.write(f"Info: {source_info}\n")
        f.write(f"Text: {text[:200]}...\n" if len(text) > 200 else f"Text: {text}\n")
        f.write(f"Result: {result}\n")
        f.write(f"Confidence: {confidence:.2%}\n")
        f.write("="*70 + "\n\n")
    
    return filename

def check_with_dataset():
    """Option 1: Check with dataset samples"""
    print("\n" + "="*70)
    print("OPTION 1: Check with Dataset Samples")
    print("="*70)
    
    print("\nTesting on 10 random samples from the dataset:")
    print("-"*70)
    
    random_samples = df.sample(n=10, random_state=None)
    correct = 0
    
    for i, (idx, row) in enumerate(random_samples.iterrows(), 1):
        text = row['Unnamed: 0']
        actual_label = row['label']
        
        text_vec = vectorizer.transform([text])
        prediction = model.predict(text_vec)[0]
        probability = model.predict_proba(text_vec)[0]
        
        actual = "CYBERBULLYING" if actual_label == 1 else "SAFE"
        predicted = "⚠️  CYBERBULLYING" if prediction == 1 else "✓ SAFE"
        conf = probability[1] if prediction == 1 else probability[0]
        
        is_correct = actual_label == prediction
        correct += is_correct
        status = "✓" if is_correct else "✗"
        
        display_text = text[:60] + "..." if len(text) > 60 else text
        
        print(f"\n{i}. \"{display_text}\"")
        print(f"   Actual: {actual}")
        print(f"   Predicted: {predicted} (Confidence: {conf:.2%}) {status}")
    
    print(f"\n{'='*70}")
    print(f"Results: {correct}/10 correct ({correct*10}%)")
    print("="*70)
    
    # Save summary to file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"results/dataset_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("DATASET TESTING RESULTS\n")
        f.write("="*70 + "\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Accuracy: {correct}/10 correct ({correct*10}%)\n")
        f.write("="*70 + "\n\n")
        
        for i, (idx, row) in enumerate(random_samples.iterrows(), 1):
            text = row['Unnamed: 0']
            actual_label = row['label']
            
            text_vec = vectorizer.transform([text])
            prediction = model.predict(text_vec)[0]
            probability = model.predict_proba(text_vec)[0]
            
            actual = "CYBERBULLYING" if actual_label == 1 else "SAFE"
            predicted = "CYBERBULLYING" if prediction == 1 else "SAFE"
            conf = probability[1] if prediction == 1 else probability[0]
            
            is_correct = actual_label == prediction
            status = "CORRECT" if is_correct else "WRONG"
            
            f.write(f"Sample {i}:\n")
            f.write(f"Text: {text[:100]}...\n" if len(text) > 100 else f"Text: {text}\n")
            f.write(f"Actual: {actual}\n")
            f.write(f"Predicted: {predicted} (Confidence: {conf:.2%})\n")
            f.write(f"Status: {status}\n")
            f.write("-"*70 + "\n\n")
    
    print(f"\n💾 Results saved to: {filename}")

def check_with_custom_text():
    """Option 2: Check with custom text"""
    print("\n" + "="*70)
    print("OPTION 2: Check with Custom Text")
    print("="*70)
    
    print("\n📝 Enter text to check (or 'back' to return to menu):")
    
    while True:
        user_text = input("\n> ").strip()
        
        if user_text.lower() == 'back':
            break
        
        if user_text:
            text_vec = vectorizer.transform([user_text])
            prediction = model.predict(text_vec)[0]
            probability = model.predict_proba(text_vec)[0]
            
            if prediction == 1:
                result = "⚠️  CYBERBULLYING DETECTED"
                conf = probability[1]
            else:
                result = "✓ SAFE"
                conf = probability[0]
            
            print(f"\n🔍 Result: {result}")
            print(f"   Confidence: {conf:.2%}")
            
            # Save result
            filename = save_result(user_text, result, conf, "Custom Text")
            print(f"💾 Result saved to: {filename}")
            
            print("\nEnter another text (or 'back' to return):")
        else:
            print("❌ Please enter some text")

def check_with_image():
    """Option 3: Check with image"""
    print("\n" + "="*70)
    print("OPTION 3: Check with Image")
    print("="*70)
    
    print("\n📁 How to provide image path:")
    print("   • Type the full path: C:\\Users\\navee\\Downloads\\image.png")
    print("   • Or just filename if in current folder: image.png")
    print("   • Or drag and drop the image file here")
    print("   • Type 'back' to return to menu")
    
    while True:
        print("\n📸 Enter image path:")
        image_path = input("> ").strip().strip('"').strip("'")
        
        if image_path.lower() == 'back':
            break
        
        if not image_path:
            print("❌ No path provided")
            continue
        
        try:
            if not os.path.exists(image_path):
                print(f"❌ File not found: {image_path}")
                print("   Please check the path and try again")
                continue
            
            print(f"\n⏳ Processing: {os.path.basename(image_path)}")
            
            img = Image.open(image_path)
            print(f"✓ Image loaded: {img.size[0]}x{img.size[1]} pixels")
            
            # Extract text
            print("✓ Extracting text...")
            configs = ['--psm 6', '--psm 3', '--psm 11']
            best_text = ""
            
            for config in configs:
                text = pytesseract.image_to_string(img, config=config).strip()
                if len(text) > len(best_text):
                    best_text = text
            
            if best_text:
                print(f"\n📝 Extracted Text:")
                print(f"   \"{best_text[:100]}...\"" if len(best_text) > 100 else f"   \"{best_text}\"")
                
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
                
                print(f"\n🔍 Result: {result}")
                print(f"   Confidence: {conf:.2%}")
                
                # Save result
                filename = save_result(best_text, result, conf, "Image", os.path.basename(image_path))
                print(f"💾 Result saved to: {filename}")
            else:
                print("\n⚠️  No text found in image")
                print("   Try an image with clear, readable text")
            
            print("\nCheck another image? (or 'back' to return)")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("   Please try another image")

# Main menu loop
while True:
    print("\n" + "="*70)
    print("What would you like to do?")
    print("="*70)
    print("1. Check with Dataset")
    print("2. Check with Custom Text")
    print("3. Check with Image")
    print("4. Exit")
    print("-"*70)
    
    choice = input("Enter your choice (1/2/3/4): ").strip()
    
    if choice == '1':
        check_with_dataset()
    
    elif choice == '2':
        check_with_custom_text()
    
    elif choice == '3':
        check_with_image()
    
    elif choice == '4':
        print("\n" + "="*70)
        print("Thank you for using Cyberbullying Detection System!")
        print("="*70)
        break
    
    else:
        print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4")

print("\n✓ Program ended\n")
