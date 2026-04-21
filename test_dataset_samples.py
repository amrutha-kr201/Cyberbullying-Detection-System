import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("Testing Model on Samples FROM the Training Dataset")
print("="*70)

# Load dataset
print("\nLoading dataset...")
CSV_FILE = 'final_dataset_hinglish.csv'
TEXT_COLUMN = 'Unnamed: 0'
LABEL_COLUMN = 'label'

df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
df = df[[TEXT_COLUMN, LABEL_COLUMN]].copy()
df[LABEL_COLUMN] = df[LABEL_COLUMN].replace(-1, 1)

print(f"✓ Dataset loaded: {len(df)} samples")

# Train model
print("\nTraining model...")
X_train, X_test, y_train, y_test = train_test_split(
    df[TEXT_COLUMN], df[LABEL_COLUMN], 
    test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print(f"✓ Model trained - Accuracy: {accuracy:.2%}")

print("\n" + "="*70)
print("Testing on 15 RANDOM Samples from the Dataset")
print("="*70)

# Get random samples
random_samples = df.sample(n=15, random_state=42)

correct_count = 0
for i, (idx, row) in enumerate(random_samples.iterrows(), 1):
    text = row[TEXT_COLUMN]
    actual_label = row[LABEL_COLUMN]
    
    # Predict
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0]
    
    # Format output
    actual = "CYBERBULLYING" if actual_label == 1 else "SAFE"
    predicted = "⚠️  CYBERBULLYING" if prediction == 1 else "✓ SAFE"
    conf = probability[1] if prediction == 1 else probability[0]
    
    # Check if correct
    is_correct = actual_label == prediction
    correct_count += is_correct
    status = "✓ CORRECT" if is_correct else "✗ WRONG"
    
    # Truncate long text
    display_text = text[:70] + "..." if len(text) > 70 else text
    
    print(f"\n{i}. \"{display_text}\"")
    print(f"   Actual Label: {actual}")
    print(f"   Prediction: {predicted} (Confidence: {conf:.2%})")
    print(f"   Status: {status}")

print("\n" + "="*70)
print(f"Results: {correct_count}/15 correct ({correct_count/15*100:.1f}%)")
print("="*70)

print("\n" + "="*70)
print("Testing on 5 CYBERBULLYING Samples from Dataset")
print("="*70)

# Get cyberbullying samples
cyber_samples = df[df[LABEL_COLUMN] == 1].sample(n=5, random_state=10)

for i, (idx, row) in enumerate(cyber_samples.iterrows(), 1):
    text = row[TEXT_COLUMN]
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0]
    
    predicted = "⚠️  CYBERBULLYING" if prediction == 1 else "✓ SAFE"
    conf = probability[1] if prediction == 1 else probability[0]
    
    display_text = text[:70] + "..." if len(text) > 70 else text
    
    print(f"\n{i}. \"{display_text}\"")
    print(f"   Prediction: {predicted} (Confidence: {conf:.2%})")

print("\n" + "="*70)
print("Testing on 5 SAFE Samples from Dataset")
print("="*70)

# Get safe samples
safe_samples = df[df[LABEL_COLUMN] == 0].sample(n=5, random_state=10)

for i, (idx, row) in enumerate(safe_samples.iterrows(), 1):
    text = row[TEXT_COLUMN]
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0]
    
    predicted = "⚠️  CYBERBULLYING" if prediction == 1 else "✓ SAFE"
    conf = probability[1] if prediction == 1 else probability[0]
    
    display_text = text[:70] + "..." if len(text) > 70 else text
    
    print(f"\n{i}. \"{display_text}\"")
    print(f"   Prediction: {predicted} (Confidence: {conf:.2%})")

print("\n" + "="*70)
print("✓ COMPLETED!")
print("="*70)
