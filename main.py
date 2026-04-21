import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from PIL import Image, ImageFilter, ImageEnhance
import PIL.ImageOps
import pytesseract
import easyocr
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─── Threat Keywords (always 99% cyberbullying) ───────────────────────────────
THREAT_KEYWORDS = [
    'i will kill you', 'kill you', 'i will hurt you', 'i will find you',
    'you will die', 'gonna kill', 'going to kill', 'murder you',
    'kill yourself', 'kys', 'go die', 'end your life',
    'you should die', 'i will destroy you', 'beat you up',
    'rape you', 'stab you', 'shoot you', 'bomb you',
    'you are worthless', 'you are nothing', 'nobody likes you',
    'everyone hates you', 'you deserve to die', 'wish you were dead',
    'i hate you', 'you are ugly', 'you are stupid and worthless',
    # Harassment / bullying terms
    'harassment', 'harassing', 'harass',
    'bully', 'bullying', 'cyberbullying', 'cyberbully',
    'sexual harassment', 'sexual abuse', 'molest',
    'inappropriate', 'mobbing',
]

HARASSMENT_KEYWORDS = [
    'harassment', 'harassing', 'harass',
    'bully', 'bullying', 'cyberbullying',
    'sexual', 'molest', 'inappropriate', 'mobbing',
    'victim', 'abuse', 'abusive',
]

def check_threat_keywords(text):
    text_lower = text.lower()
    for keyword in THREAT_KEYWORDS:
        if keyword in text_lower:
            return True, keyword
    for keyword in HARASSMENT_KEYWORDS:
        if keyword in text_lower:
            return True, keyword
    return False, None

def fuzzy_threat_check(text):
    """Catches garbled OCR - e.g. 'ILL YO!' from 'KILL YOU'."""
    import re
    letters_only = ' '.join(re.sub(r'[^a-zA-Z\s]', '', text).lower().split())

    for keyword in THREAT_KEYWORDS:
        keyword_letters = re.sub(r'[^a-zA-Z\s]', '', keyword).lower()
        if keyword_letters in letters_only:
            return True, keyword

    danger_fragments = {
        'ill yo': 'kill you',
        'kill': 'kill',
        'murder': 'murder',
        'die': 'die',
        'death': 'death',
        'hurt': 'hurt',
        'rape': 'rape',
        'stab': 'stab',
        'shoot': 'shoot',
        'bomb': 'bomb',
        'attack': 'attack',
        'destroy': 'destroy',
        'hate': 'hate',
        'ugly': 'ugly',
        'stupid': 'stupid',
        'worthless': 'worthless',
        'loser': 'loser',
        'idiot': 'idiot',
        'kys': 'kill yourself',
        # Harassment / bullying
        'harassment': 'harassment',
        'harassing': 'harassing',
        'harass': 'harassment',
        'bully': 'bullying',
        'bullying': 'bullying',
        'cyberbullying': 'cyberbullying',
        'cyberbully': 'cyberbullying',
        'sexual': 'sexual harassment',
        'molest': 'molestation',
        'inappropriate': 'inappropriate behavior',
        'mobbing': 'mobbing',
        'victim': 'victim',
        'abuse': 'abuse',
    }
    for fragment, label in danger_fragments.items():
        if fragment in letters_only:
            return True, label
    return False, None

# ─── Setup ────────────────────────────────────────────────────────────────────
os.makedirs('results', exist_ok=True)

print("="*70)
print("        CYBERBULLYING DETECTION SYSTEM")
print("="*70)

print("\n⏳ Loading and training model...")
df = pd.read_csv('final_dataset_hinglish.csv', on_bad_lines='skip')
df = df[['Unnamed: 0', 'label']].copy()
df['label'] = df['label'].replace(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(
    df['Unnamed: 0'], df['label'], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test_vec))
print(f"✓ Model trained! Accuracy: {accuracy:.2%} | Dataset: {len(df)} samples")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize EasyOCR once
print("⏳ Loading EasyOCR model (first time may take a moment)...")
ocr_reader = easyocr.Reader(['en'], verbose=False)
print("✓ EasyOCR ready!")

# ─── Helpers ──────────────────────────────────────────────────────────────────
def save_result(text, result, confidence, source_type, source_info=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename  = f"results/detection_results_{datetime.now().strftime('%Y%m%d')}.txt"
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

def predict_text(text):
    """Predict with keyword override for serious threats."""
    is_threat, matched = check_threat_keywords(text)
    if is_threat:
        return 1, 0.99, f"Threat keyword detected: '{matched}'"
    is_threat, matched = fuzzy_threat_check(text)
    if is_threat:
        return 1, 0.97, f"Threat word detected: '{matched}'"
    vec  = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]
    conf = prob[1] if pred == 1 else prob[0]
    return pred, conf, None

def extract_text_from_image(image_path):
    """Extract text using EasyOCR (primary) with Tesseract as fallback."""
    print("✓ Extracting text with EasyOCR...")

    # --- EasyOCR (primary) ---
    try:
        results = ocr_reader.readtext(image_path)
        if results:
            easy_text = ' '.join([text for (_, text, conf) in results if conf > 0.1])
            if easy_text.strip():
                print(f"✓ EasyOCR extracted {len(results)} text regions")
                return easy_text.strip()
    except Exception as e:
        print(f"⚠️  EasyOCR failed: {e}, trying Tesseract...")

    # --- Tesseract fallback ---
    print("✓ Trying Tesseract fallback...")
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    gray = img.convert('L')
    texts = []
    for pil_img in [gray, PIL.ImageOps.invert(gray),
                    ImageEnhance.Contrast(gray).enhance(3.0)]:
        for psm in ['--psm 6', '--psm 3', '--psm 11']:
            t = pytesseract.image_to_string(pil_img, config=psm).strip()
            if t:
                texts.append(t)
    return max(texts, key=len) if texts else ""

# ─── Menu Options ─────────────────────────────────────────────────────────────
def check_with_dataset():
    print("\n" + "="*70)
    print("OPTION 1: Check with Dataset Samples")
    print("="*70)
    print("\nTesting on 10 random samples from the dataset:")
    print("-"*70)

    samples = df.sample(n=10, random_state=None)
    correct = 0

    for i, (_, row) in enumerate(samples.iterrows(), 1):
        text  = row['Unnamed: 0']
        actual_label = row['label']
        pred, conf, _ = predict_text(text)

        actual    = "CYBERBULLYING" if actual_label == 1 else "SAFE"
        predicted = "⚠️  CYBERBULLYING" if pred == 1 else "✓ SAFE"
        is_correct = actual_label == pred
        correct   += is_correct

        display = text[:60] + "..." if len(text) > 60 else text
        print(f"\n{i}. \"{display}\"")
        print(f"   Actual: {actual}")
        print(f"   Predicted: {predicted} (Confidence: {conf:.2%}) {'✓' if is_correct else '✗'}")

    print(f"\n{'='*70}")
    print(f"Results: {correct}/10 correct ({correct*10}%)")
    print("="*70)

def check_with_custom_text():
    print("\n" + "="*70)
    print("OPTION 2: Check with Custom Text")
    print("="*70)
    print("\n📝 Enter text to check (or 'back' to return):")

    while True:
        user_text = input("\n> ").strip()
        if user_text.lower() == 'back':
            break
        if not user_text:
            print("❌ Please enter some text")
            continue

        pred, conf, keyword_info = predict_text(user_text)
        result = "⚠️  CYBERBULLYING DETECTED" if pred == 1 else "✓ SAFE"

        print(f"\n🔍 Result: {result}")
        print(f"   Confidence: {conf:.2%}")
        if keyword_info:
            print(f"   ⚠️  {keyword_info}")

        filename = save_result(user_text, result, conf, "Custom Text")
        print(f"💾 Saved to: {filename}")
        print("\nEnter another text (or 'back' to return):")

def check_with_image():
    print("\n" + "="*70)
    print("OPTION 3: Check with Image")
    print("="*70)
    print("\n📁 Enter full image path (or 'back' to return):")
    print("   Example: C:\\Users\\navee\\Downloads\\image.jpg")

    while True:
        image_path = input("\n📸 Path: ").strip().strip('"').strip("'")
        if image_path.lower() == 'back':
            break
        if not image_path:
            print("❌ No path provided")
            continue
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            continue

        try:
            print(f"\n⏳ Processing: {os.path.basename(image_path)}")
            best_text = extract_text_from_image(image_path)

            if not best_text:
                print("\n⚠️  No text found in image. Try a clearer image.")
                continue

            print(f"\n📝 Extracted Text:\n   \"{best_text[:300]}\"")

            pred, conf, keyword_info = predict_text(best_text)
            result = "⚠️  CYBERBULLYING DETECTED" if pred == 1 else "✓ SAFE"

            print(f"\n🔍 Result: {result}")
            print(f"   Confidence: {conf:.2%}")
            if keyword_info:
                print(f"   ⚠️  {keyword_info}")

            filename = save_result(best_text, result, conf, "Image", os.path.basename(image_path))
            print(f"💾 Saved to: {filename}")
            print("\nCheck another image? (or 'back' to return)")

        except Exception as e:
            print(f"\n❌ Error: {e}")

# ─── Main Loop ────────────────────────────────────────────────────────────────
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

    if   choice == '1': check_with_dataset()
    elif choice == '2': check_with_custom_text()
    elif choice == '3': check_with_image()
    elif choice == '4':
        print("\n✓ Thank you for using Cyberbullying Detection System!\n")
        break
    else:
        print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4")
